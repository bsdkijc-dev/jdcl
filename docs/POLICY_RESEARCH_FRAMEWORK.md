# JDCL v1.0 — Policy Research Framework

## Epistemic Classification Standard

Every JDCL research output must explicitly tag statements into one of six categories:

| Tag | Category | Description |
| :--- | :--- | :--- |
| **A** | Observed Facts | Direct outputs from executed local code/tests or verified internal records |
| **B** | Verified Public-Source Information | Attributable facts from official public publications (not fabricated) |
| **C** | Synthetic Assumptions | Structural equations, distributions, and parameters in `jflm_2027.csv` |
| **D** | Model-Generated Estimates | Predictions, MAE/RMSE, calibration ECE, and subgroup gaps on synthetic splits |
| **E** | Hypotheses Requiring Empirical Validation | Testable propositions derived from synthetic or exploratory patterns (non-causal) |
| **F** | Policy Recommendations | Structured intervention proposals requiring human/institutional review |

> **Non-Causality Rule:** Correlations observed in synthetic or observational data must **never** be presented as causal proof.

## Structured Policy Recommendation Template (Pilot Hypothesis Example)

### Recommendation F-01: Targeted Mobile Circuit Court & Legal-Aid Co-Deployment in `Remote-3T` Tiers *(Hypothesis Requiring Empirical Validation)*

1. **Identified Problem:** Geographic distance, travel cost, and low digital connectivity create access-to-justice bottlenecks in remote/archipelagic (`3T`) areas (**C** synthetic modeling assumption; **E** empirical hypothesis).
2. **Evidence Supporting the Problem:** In `jflm_2027.csv`, `Remote-3T` synthetic records exhibit longer modeled resolution times and lower `eCourt_Digital` share (**C/D** — synthetic data only, not empirical court performance).
3. **Proposed Intervention:** Co-locate mobile circuit court schedules (`Sidang Keliling`) with community paralegal intake and `Posbakum` fee-waiver (`prodeo`) screening (**F**).
4. **Intended Beneficiaries:** Low-income litigants, female-headed households, persons with disabilities, and remote/indigenous communities.
5. **Legal & Institutional Feasibility:** High — builds on existing Indonesian Supreme Court (`PERMA No. 1 Tahun 2014`) legal-aid and circuit-court mechanisms (subject to human legal verification).
6. **Implementation Costs:** Zero additional software cost via JDCL open-source planning tools; operational field costs must be evaluated within existing court DIPA budgets.
7. **Risks:** Weather/maritime scheduling disruptions, privacy leakage during community intake, and uneven paralegal training.
8. **Evaluation Design:** Stepped-wedge or matched-district pilot comparing intake-to-resolution duration and SLA completion rates with strict PII anonymization.
9. **Expected Measurable Outcomes:** Measurable reduction in travel burden and intake-to-resolution variance across `Remote-3T` vs. `Urban` tiers (to be empirically tested).
