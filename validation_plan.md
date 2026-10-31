# Validation Plan and Known Limitations

## Before the demo
- [ ] Confirm the app connects to the team's Exasol Personal instance.
- [ ] Load the synthetic CSV into `STEAMSAGE_TRAPS`.
- [ ] Verify row count is 500.
- [ ] Run `sql/diagnosis.sql` and compare the returned columns with the dashboard.
- [ ] Check that the CSV export opens correctly.
- [ ] Confirm `.env` is excluded from version control.
- [ ] Record a short screen demo showing the database-backed workflow.

## Validation for a real pilot
1. Collect instrument readings with measurement method, units, timestamp, operating load, and trap type.
2. Establish fault labels only from confirmed field inspections by qualified staff.
3. Calibrate thresholds by trap type and operating conditions.
4. Separate training and evaluation records by asset and time to reduce leakage.
5. Report precision, recall, confusion matrix, and false-negative rates for each fault class.
6. Validate loss estimates against an accepted engineering calculation and document uncertainty.
7. Have maintenance and safety owners approve use cases before operational use.

## Known limitations
- Synthetic data is not evidence of real diagnostic accuracy.
- Ultrasonic index is an arbitrary relative demo feature, not a standard calibrated measurement.
- Temperature-only signals are not sufficient to diagnose every trap type.
- Rules are illustrative and may misclassify real readings.
- Annual cost estimates use synthetic loss assumptions and constant prices/hours.
- The dashboard is not connected to live sensors, CMMS, or plant-control systems.
- The tool must not autonomously operate equipment or replace qualified inspections.
