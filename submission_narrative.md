# Submission Narrative — SteamSage

## Project title
SteamSage — Explainable Steam-Trap Fault Triage and Maintenance Prioritization

## Track
Factories, Fleets & Supply Chains

## Problem statement
Industrial maintenance teams can struggle to identify and prioritize faulty steam traps across large steam networks because inspection records and operating measurements are difficult to review consistently. Missed or delayed identification of steam leaks and condensate drainage problems can contribute to energy waste, maintenance cost, and process disruption.

## Solution
SteamSage is an analytics prototype that converts steam-trap inspection data into a prioritized inspection queue. It uses Exasol Personal to store and query the records, SQL rules to flag suspected leak/blockage/uncertain conditions, and a Streamlit dashboard to show supporting signals and illustrative potential-cost estimates.

## Why Exasol
The prototype loads the dataset into an Exasol table and runs queries against it. This demonstrates an analytical database workflow over a fleet-scale dataset, rather than using Exasol as a logo or an unused integration. Exasol supports filtering, aggregation, ranking, and repeatable SQL-based analysis.

## Users
- Plant reliability and maintenance engineers
- Energy managers
- Steam-system auditors
- Operations teams coordinating inspections

## Expected value
- Focus inspection effort on the most concerning records.
- Make diagnostic reasoning visible instead of returning an unexplained label.
- Connect suspected faults to a transparent cost scenario.
- Support consistent fleet-level reporting.

## What is demonstrated
- 500 reproducible synthetic records.
- Exasol table load and SQL query workflow.
- Interpretable rules with explicit uncertainty.
- Ranked inspection queue, aggregate metrics, and CSV export.
- Reproduction instructions and limitations.

## Limitations and responsible use
The data, reference labels, loss rates, prices, and thresholds are synthetic or illustrative. The prototype does not establish validated diagnostic accuracy, actual energy savings, or a safety certification. A production system would require verified sensor data, trap-specific thresholds, calibration, labelled field observations, and review by qualified engineers. Recommendations are inspection prompts, not automatic maintenance commands.

## Future work
- Ingest time-series readings from calibrated temperature and ultrasonic instruments.
- Add trap-type-specific rules and baseline comparisons.
- Validate against confirmed inspection outcomes.
- Add drift detection and a feedback loop for maintenance results.
- Estimate uncertainty ranges and distinguish measured losses from modelled exposure.

## Demo flow
1. Show the data-source toggle and select Exasol Personal.
2. Load the bundled synthetic records into Exasol.
3. Show database-backed totals and the inspection priority queue.
4. Open one trap and explain the signals behind its classification.
5. Show the potential-cost assumptions and export the queue.
