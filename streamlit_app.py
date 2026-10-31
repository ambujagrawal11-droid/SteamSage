import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DATA_PATH = ROOT / "data" / "synthetic_steam_traps.csv"

st.set_page_config(page_title="SteamSage | Steam Trap Diagnostics", page_icon="♨️", layout="wide")

st.title("♨️ SteamSage")
st.caption("Industrial steam-trap fault triage • Exasol Personal + Python + Streamlit")
st.warning(
    "Prototype using synthetic data and illustrative thresholds. Not validated for live plant use. "
    "All suspected faults require qualified inspection."
)

def diagnosis_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["diagnosis"] = "No immediate flag"
    out["priority"] = "Low"
    leak = (out["ultrasonic_index"] >= 65) & (out["temperature_c"] >= 145)
    blocked = (out["temperature_c"] <= 105) & (out["ultrasonic_index"] <= 40)
    uncertain = (~leak) & (~blocked) & (
        (out["ultrasonic_index"] >= 35) | (out["inspection_age_days"] >= 120)
    )
    out.loc[leak, "diagnosis"] = "Suspected leak"
    out.loc[blocked, "diagnosis"] = "Suspected blockage"
    out.loc[uncertain, "diagnosis"] = "Inspect / uncertain"
    out.loc[leak | blocked, "priority"] = "High"
    out.loc[uncertain, "priority"] = "Medium"
    out["estimated_annual_cost_inr"] = (
        out["estimated_loss_kg_hr"] / 1000
        * out["steam_cost_inr_per_tonne"]
        * out["operating_hours_per_day"] * 365
    ).round(0)
    order = {"High": 0, "Medium": 1, "Low": 2}
    out["_priority_order"] = out["priority"].map(order)
    return out.sort_values(
        ["_priority_order", "estimated_annual_cost_inr"], ascending=[True, False]
    ).drop(columns=["_priority_order"])

def connect_exasol():
    try:
        import pyexasol
        dsn = os.getenv("EXASOL_DSN", "").strip()
        user = os.getenv("EXASOL_USER", "").strip()
        password = os.getenv("EXASOL_PASSWORD", "")
        if not all([dsn, user, password]) or "YOUR_" in user:
            raise ValueError("Set EXASOL_DSN, EXASOL_USER and EXASOL_PASSWORD in .env.")
        conn = pyexasol.connect(dsn=dsn, user=user, password=password, compression=True)
        return conn
    except Exception as exc:
        st.error(f"Exasol connection failed: {exc}")
        return None

def load_csv_to_exasol(conn, data: pd.DataFrame, schema: str):
    # Use a user-owned schema. If schema creation is restricted, create it manually first.
    safe_schema = "".join(ch for ch in schema.upper() if ch.isalnum() or ch == "_")
    if not safe_schema:
        raise ValueError("EXASOL_SCHEMA must be a valid schema name.")
    conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{safe_schema}"')
    conn.execute(f'CREATE OR REPLACE TABLE "{safe_schema}"."STEAMSAGE_TRAPS" ('
        'TRAP_ID VARCHAR(16), TRAP_TYPE VARCHAR(64), STEAM_PRESSURE_BAR DECIMAL(6,1), '
        'TEMPERATURE_C DECIMAL(6,1), ULTRASONIC_INDEX DECIMAL(6,1), '
        'OPERATING_HOURS_PER_DAY DECIMAL(4,0), INSPECTION_AGE_DAYS DECIMAL(5,0), '
        'ESTIMATED_LOSS_KG_HR DECIMAL(8,2), STEAM_COST_INR_PER_TONNE DECIMAL(10,2), '
        'SYNTHETIC_REFERENCE_LABEL VARCHAR(24))')
    cols = [
        "trap_id", "trap_type", "steam_pressure_bar", "temperature_c", "ultrasonic_index",
        "operating_hours_per_day", "inspection_age_days", "estimated_loss_kg_hr",
        "steam_cost_inr_per_tonne", "synthetic_reference_label"
    ]
    upload = data[cols].copy()
    # pyexasol supports importing a pandas DataFrame directly into an existing table.
    conn.import_from_pandas(upload, f'"{safe_schema}"."STEAMSAGE_TRAPS"')
    return safe_schema

with st.sidebar:
    st.header("Data source")
    mode = st.radio("Choose mode", ["Demo mode (local synthetic data)", "Exasol Personal"])
    st.caption("Competition demonstration should show the Exasol Personal mode working.")

if not DATA_PATH.exists():
    st.error(f"Sample dataset not found: {DATA_PATH}")
    st.stop()

local_df = pd.read_csv(DATA_PATH)

if mode == "Demo mode (local synthetic data)":
    raw = local_df
    st.info("Demo mode reads the bundled synthetic CSV locally. Switch to Exasol Personal to demonstrate database usage.")
else:
    if st.button("Connect and load/refresh synthetic sample in Exasol", type="primary"):
        conn = connect_exasol()
        if conn is not None:
            try:
                schema = load_csv_to_exasol(conn, local_df, os.getenv("EXASOL_SCHEMA", "STEAMSAGE"))
                st.success(f"Loaded {len(local_df)} synthetic records into {schema}.STEAMSAGE_TRAPS")
            except Exception as exc:
                st.error(f"Could not load sample data: {exc}")
            finally:
                try:
                    conn.close()
                except Exception:
                    pass
    conn = connect_exasol()
    if conn is None:
        st.stop()
    try:
        schema = "".join(ch for ch in os.getenv("EXASOL_SCHEMA", "STEAMSAGE").upper() if ch.isalnum() or ch == "_")
        raw = conn.export_to_pandas(
            f'SELECT TRAP_ID AS trap_id, TRAP_TYPE AS trap_type, '
            f'STEAM_PRESSURE_BAR AS steam_pressure_bar, TEMPERATURE_C AS temperature_c, '
            f'ULTRASONIC_INDEX AS ultrasonic_index, OPERATING_HOURS_PER_DAY AS operating_hours_per_day, '
            f'INSPECTION_AGE_DAYS AS inspection_age_days, ESTIMATED_LOSS_KG_HR AS estimated_loss_kg_hr, '
            f'STEAM_COST_INR_PER_TONNE AS steam_cost_inr_per_tonne, '
            f'SYNTHETIC_REFERENCE_LABEL AS synthetic_reference_label '
            f'FROM "{schema}"."STEAMSAGE_TRAPS"'
        )
    except Exception as exc:
        st.error("The table is not available yet. Click the load/refresh button above, then rerun. "
                 f"Database detail: {exc}")
        st.stop()
    finally:
        try:
            conn.close()
        except Exception:
            pass

results = diagnosis_frame(raw)
high = int((results["priority"] == "High").sum())
flagged = int((results["diagnosis"] != "No immediate flag").sum())
annual_cost = float(results["estimated_annual_cost_inr"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Traps analyzed", f"{len(results):,}")
c2.metric("Flagged for review", f"{flagged:,}")
c3.metric("High-priority checks", f"{high:,}")
c4.metric("Illustrative annual loss exposure", f"₹{annual_cost:,.0f}")

st.subheader("Inspection priority queue")
st.caption("Annual cost is an illustrative scenario estimate from synthetic loss-rate and steam-price assumptions.")
priority_filter = st.multiselect(
    "Filter by priority", ["High", "Medium", "Low"], default=["High", "Medium", "Low"]
)
filtered = results[results["priority"].isin(priority_filter)]
display_cols = [
    "trap_id", "trap_type", "temperature_c", "ultrasonic_index", "inspection_age_days",
    "diagnosis", "priority", "estimated_loss_kg_hr", "estimated_annual_cost_inr"
]
st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)
st.download_button(
    "Download diagnosis CSV",
    filtered[display_cols].to_csv(index=False).encode("utf-8"),
    file_name="steamsage_diagnosis.csv",
    mime="text/csv"
)

left, right = st.columns(2)
with left:
    st.subheader("Diagnosis mix")
    st.bar_chart(results["diagnosis"].value_counts())
with right:
    st.subheader("Potential annual cost by priority")
    cost_by_priority = results.groupby("priority")["estimated_annual_cost_inr"].sum().reindex(["High", "Medium", "Low"])
    st.bar_chart(cost_by_priority)

st.subheader("Why a trap was flagged")
trap_id = st.selectbox("Select a trap", results["trap_id"].tolist())
r = results.loc[results["trap_id"] == trap_id].iloc[0]
if r["diagnosis"] == "Suspected leak":
    explanation = "High illustrative ultrasonic index combined with elevated temperature matched the demo leak rule."
elif r["diagnosis"] == "Suspected blockage":
    explanation = "Low illustrative temperature combined with a low/moderate ultrasonic index matched the demo blockage rule."
elif r["diagnosis"] == "Inspect / uncertain":
    explanation = "The signal or inspection age crossed a review threshold, but the available indicators do not confirm a fault."
else:
    explanation = "The record did not cross the current demo thresholds. This is not proof that the trap is healthy."
st.write(f"**{trap_id}: {r['diagnosis']} · {r['priority']} priority**")
st.write(explanation)
st.write("Recommended action: verify trap type and operating load, repeat temperature/ultrasonic inspection with a suitable instrument, and have a qualified technician confirm the fault.")
st.caption("Synthetic reference labels are included to explain the generated data only. They are not used by the diagnosis rules.")
