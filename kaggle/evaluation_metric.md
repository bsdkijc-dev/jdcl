# Evaluation Metric — JFLM 2027

- **Primary Metric:** Mean Absolute Error (`MAE`) on `predicted_resolution_days` vs. `resolution_days` across the deterministic holdout split.
- **Secondary Diagnostics:** `RMSE`, `R2`, and **Max Subgroup MAE Gap** across `region_tier` and `vulnerability_group`.
- **Submission Format:** CSV with columns `record_id,predicted_resolution_days` (values bounded `[1.0, 365.0]`, no NaNs).
