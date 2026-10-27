# Validation: recorded results and limits

## Provenance

The submitted repository records Athena observations from **October 26, 2026**. The baseline is commit [`bf1f7ca22f8c1e8ca648efe4a2225690756a0958`](https://github.com/kikaloka/D609-Data-Analytics-at-Scale/commit/bf1f7ca22f8c1e8ca648efe4a2225690756a0958). Its jobs, SQL, screenshots, and query-text companions remain unchanged.

Erica subsequently confirmed that the D609 Udacity submission passed. That status comes from her confirmation; no new evaluator-report capture is included. Historical results, course acceptance, and static verification of this update are distinct claims.

## Table mapping and recorded results

All tables use database `stedi`.

| Logical table | Actual table | Recorded rows |
|---|---|---:|
| Customer landing | `customer_landing` | 956 |
| Accelerometer landing | `accelerometer_landing` | 81,273 |
| Step-trainer landing | `step_trainer_landing` | 28,680 |
| Customer trusted | `erica_customer_trusted` | 482 |
| Accelerometer trusted | `erica_accelerometer_trusted` | 40,981 |
| Customers curated | `erica_customers_curated` | 482 |
| Step-trainer trusted | `erica_step_trainer_trusted` | 14,460 |
| Machine-learning curated | `erica_machine_learning_curated` | 43,681 |

`customers_curated` is plural. The `erica_` prefix distinguishes visual-job outputs from earlier tables. The file `customer_trusted.png` displays the actual prefixed table.

Other recorded checks: **474** landing customers with null research consent; **0** trusted customers with null research consent. The [count screenshot](../evidence/rubric-counts-and-consent.png) and [complementary view](../evidence/rubric-counts-results.png) jointly show the results; the AWS sticky footer obscures some rows in one view. The [text companion](../evidence/rubric-counts-and-consent.txt) retains the historical query reference. Opening that history may require the original authenticated lab.

## What the checks establish

- [rubric_validation.sql](../sql/rubric_validation.sql) counts eight named tables and null consent in customer landing/trusted.
- [landing_missing_consent_examples.sql](../sql/landing_missing_consent_examples.sql) illustrates excluded records. Samples are not full-table counts.
- The four sample images support schema and record inspection, not uniqueness or completeness claims.
- The generated Glue rule `ColumnCount > 0` checks for columns, not correct counts or consent.

Matching totals does not establish same-person pairing, historical consent, absence of duplicates, or model accuracy. The preserved SQL does not check every one of those properties. No new result is claimed here.

## Diagnosing a future mismatch

| Observation | Inspect first |
|---|---|
| Landing count differs | Dataset version, JSON parsing, prefix, and schema |
| Trusted count grows unexpectedly | Repeated customer emails or files from repeated runs |
| Curated customers repeat | `DISTINCT c.*`; distinct full rows may still share email |
| Trainer count differs | Serial membership, selected fields, existing output objects |
| Final count exceeds an input | Many-to-many timestamp matches; not automatically a failed join |
| Consent violation appears | Actual table name, SQL filter, output version being queried |

Investigate rather than changing expected numbers or historical screenshots. Document new validation separately.

[Evidence guide](../evidence/README.md) · [Setup](SETUP.md) · [Project home](../README.md)
