# STEDI course project

Five AWS Glue Studio jobs move customer, phone-motion, and step-trainer data from landing through trusted and curated layers. Research consent determines customer eligibility; the final table pairs sensor readings by timestamp.

## Jobs and verified results

Run these jobs in order. All tables use the `stedi` database.

| Script in jobs/ | Actual output table | Rows |
|---|---|---:|
| customer_landing_to_trusted.py | erica_customer_trusted | 482 |
| accelerometer_landing_to_trusted.py | erica_accelerometer_trusted | 40,981 |
| customer_trusted_to_curated.py | erica_customers_curated | 482 |
| step_trainer_trusted.py | erica_step_trainer_trusted | 14,460 |
| machine_learning_curated.py | erica_machine_learning_curated | 43,681 |

Landing counts: `customer_landing` 956; `accelerometer_landing` 81,273; `step_trainer_landing` 28,680. The `erica_` prefix identifies the verified visual-job outputs; `customers_curated` is plural. Exports retain the actual lab-specific S3 paths and table names.

## Evidence

The four sample screenshots in `evidence/` are named `customer_landing.png`, `accelerometer_landing.png`, `step_trainer_landing.png`, and `customer_trusted.png`. Samples do not establish full-table counts.

- [Counts and consent](evidence/rubric-counts-and-consent.png) and [complementary results](evidence/rubric-counts-results.png) collectively show all eight required counts, 474 missing-consent customer landing rows, and zero missing-consent customer trusted rows. The paired views cover rows crossed by the AWS sticky footer.
- [Blank landing consent examples](evidence/landing-missing-consent.png) shows multiple rows selected with `IS NULL`.
- [Recorded values and query reference](evidence/rubric-counts-and-consent.txt) accompany the screenshots. Reusable count and consent queries and three landing-table definitions are in `sql/`.

Results were observed October 26, 2026. Only AWS account/session banners were masked in these public-safe captures; technical evidence is unchanged. Preparing this package did not rerun AWS jobs.

## Limits

Equal timestamps do not prove that the phone and device belong to the same person. These jobs do not apply consent effective at reading time or anonymize output. Rerunning into an existing output folder can append duplicate files; plan fresh output locations and matching catalog settings. Exact catalog naming and course acceptance remain the evaluator's decision.

## Sources and assistance

This project builds on the [Udacity STEDI starter datasets and project materials](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/tree/main/project/starter). The requirements and rubric came from the WGU Udacity classroom.

I used AI to help develop and debug the code, check the results, and organize the project documentation and screenshots.
