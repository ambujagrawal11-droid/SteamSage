# Data Sources, Licences, APIs, and Third-Party Tools

## Data sources
- `data/synthetic_steam_traps.csv`: generated specifically for this prototype with a deterministic random seed. It is synthetic, not sourced from a real factory.
- `scripts/generate_data.py`: generation script bundled in this repository.
- No confidential, personal, or proprietary plant data is included.
- The temperature, ultrasonic index, pressure, operating hours, inspection age, loss-rate values, steam-price values, and reference labels are simulated for demonstration only.

## Licence
- Project code: MIT License (see `LICENSE`).
- Synthetic data: included with this repository under the same permissive project licence, unless a separate data licence is added by the team.
- Any later-added external dataset must have its source URL, access date, licence, attribution requirements, and any usage restrictions recorded here before inclusion.

## APIs and services
- No external API is required for the current prototype.
- Exasol Personal is the required database platform for the competition demonstration.
- Exasol connection details are supplied locally through `.env`; credentials must never be committed to the public repository.

## Third-party tools
- Python
- Streamlit
- pandas
- python-dotenv
- pyexasol
- Exasol Personal

Dependency licences are governed by their respective upstream projects. The team should verify dependency versions and licences at submission time.

## Reproducibility
- Python 3.10–3.12 recommended.
- Install dependencies using `pip install -r requirements.txt`.
- Copy `.env.example` to `.env` and configure Exasol Personal.
- Run `streamlit run app/streamlit_app.py`.
- Synthetic dataset generation: `python scripts/generate_data.py`.

## Safety and claims
Do not claim real-world fault accuracy, energy savings, or financial returns based on synthetic data. All cost outputs are scenario estimates. All fault classifications require verification by qualified personnel.
