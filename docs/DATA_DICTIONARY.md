# JFLM 2027 Synthetic Data Dictionary

> **PROMINENT SYNTHETIC DATA DISCLAIMER:**  
> `data/synthetic/jflm_2027.csv` is **100% deterministically generated synthetic data** (`SYNTHETIC_JFLM_2027_V1`). It contains **no real citizen identities, no real litigant information, and no real judicial case records**. Synthetic distributions and relationships are modeling assumptions only and must never be interpreted as empirical measurements of Indonesian judicial institutions.

## Dataset Summary

- **File:** `data/synthetic/jflm_2027.csv`
- **Default Size:** 10,000 rows × 19 columns
- **Default Seed:** `20270101`
- **Encoding:** UTF-8 CSV, pure numeric values (no currency symbols or thousand separators), missing optional values preserved as empty cells (zero-imputation policy).

## Column Definitions

| Column | Type | Nullable | Domain / Bounds | Description |
| :--- | :--- | :--- | :--- | :--- |
| `record_id` | string | No | `^JFLM2027-[0-9]{6}$` (unique) | Synthetic unique record identifier |
| `province_group` | category | No | 10 representative province groups | Synthetic province tier grouping |
| `region_tier` | category | No | `Urban`, `Peri-Urban`, `Rural`, `Remote-3T` | Geographic accessibility tier |
| `court_jurisdiction` | category | No | `General_District`, `Religious_Family`, `Administrative`, `Industrial_Labor` | Synthetic court jurisdiction category |
| `service_channel` | category | No | `Posbakum_InPerson`, `Mobile_Circuit_Court`, `eCourt_Digital`, `Community_Paralegal` | Justice service delivery channel |
| `dispute_category` | category | No | `Civil_Small_Claims`, `Family_Custody_Support`, `Land_Agrarian`, `Labor_Dispute`, `Legal_Aid_Consultation` | Synthetic dispute/consultation category |
| `vulnerability_group` | category | No | `Standard`, `Low_Income_Prodeo`, `Indigenous_Remote`, `Person_With_Disability`, `Female_Headed_Household` | Synthetic vulnerability group for fairness diagnostics |
| `gender_category` | category | No | `Female`, `Male`, `Undisclosed` | Synthetic gender category for fairness diagnostics |
| `distance_to_court_km` | float | No | `[0.5, 350.0]` | Synthetic travel distance to nearest court/service point (km) |
| `travel_cost_idr_thousands` | float | No | `[5.0, 2500.0]` | Synthetic round-trip travel cost (IDR thousands, numeric only) |
| `digital_connectivity_index` | float | No | `[0.0, 1.0]` | Synthetic local digital connectivity score |
| `legal_aid_available` | int | No | `{0, 1}` | Synthetic indicator for Posbakum/legal-aid availability |
| `fee_waiver_prodeo` | int | No | `{0, 1}` | Synthetic indicator for court fee-waiver (`prodeo`) eligibility/use |
| `digital_intake_score` | float | Yes (≤5%) | `[0.0, 100.0]` | Synthetic digital intake readiness score (missingness preserved) |
| `paralegal_hours` | float | Yes (≤5%) | `[0.0, 80.0]` | Synthetic community paralegal support hours (missingness preserved) |
| `case_complexity_index` | float | No | `[1.0, 10.0]` | Synthetic procedural complexity index |
| `resolution_days` | float | No | `[1.0, 365.0]` | **Primary Regression Target:** Synthetic service delivery duration (days) |
| `service_completed` | int | No | `{0, 1}` | **Secondary Classification Target:** Synthetic completion within 90-day SLA |
| `data_origin` | category | No | `SYNTHETIC_JFLM_2027_V1` | Explicit synthetic provenance tag on every row |
