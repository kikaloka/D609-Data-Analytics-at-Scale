D609 STEDI Human Balance Analytics

Status: all five AWS Glue jobs SUCCEEDED on October 23, 2026.
All 14 actual Athena checks passed, including every standard rubric row count.
Execution and query IDs are saved in evidence/*.json. The local SQL reference
validation is a separate check, not a substitute for AWS execution evidence.

Actual AWS row counts:
customer_landing 956; accelerometer_landing 81273; step_trainer_landing 28680;
customer_trusted 482; accelerometer_trusted 40981; customers_curated 482;
step_trainer_trusted 14460; machine_learning_curated 43681.

Source data: Udacity's official reduced project/starter dataset:
https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises
Raw course datasets are excluded from this repository.
AWS credentials are excluded too.

Run the five jobs in this order:
1. customer_landing_to_trusted
2. accelerometer_landing_to_trusted
3. customer_trusted_to_curated
4. step_trainer_trusted
5. machine_learning_curated

Provide --DATABASE stedi and --OUTPUT_ROOT s3://YOUR_BUCKET/runs/UNIQUE_RUN_ID.
Use a NEW output root for a complete rerun to prevent appended duplicate rows.
Never run a completed job twice against the same output root.
The catalog table locations must point to the latest successful complete run.
Each job writes Snappy Parquet and enables catalog schema updates using
enableUpdateCatalog=True and updateBehavior='UPDATE_IN_DATABASE'.

Create the stedi database first, then replace YOUR_BUCKET in the landing DDL.
The DDL includes all JSON fields with bigint epoch milliseconds, double axes,
and string identifiers. The final table retains the standard rubric columns;
it does not implement the optional anonymization enhancement.

Landing data remains unchanged. Customer consent is tested as non-null because
the official dataset uses JSON null for customers without research consent.
Accelerometer user joins customer email; customer DISTINCT prevents one row
per accelerometer reading. Step trainer DISTINCT prevents duplicated device
records from reused customer serial numbers. The final timestamp join follows
the standard rubric. Optional consent-at-reading-time filtering is not enabled.
This is a training-case transformation, not a production identity-resolution system.

AWS catalog update configuration follows:
https://docs.aws.amazon.com/glue/latest/dg/update-from-job.html

Required evidence: actual Athena counts for all eight tables, landing customer
rows with missing consent, and trusted customer rows with zero missing consent.

Local reference validation:
python tools/validate_source.py PATH_TO_OFFICIAL_PROJECT_STARTER

Temporary course lab deployment and verification:
python tools/deploy_lab.py --create-role --run
python tools/verify_lab.py
python tools/create_evidence_queries.py

The deployment script guards the observed D609 course account. Adapt that
guard deliberately before using a different account. The role-creation flag
requires approval of the scoped Glue role. Storage is private and encrypted.
Jobs use two G.1X workers, a 15-minute timeout, and no retries.

OpenAI Codex generated the implementation and performed inspection, debugging,
execution, and documentation. Reviewing this example does not make it a
student-authored submission. Use it to understand the pipeline, then develop
your own work under the course's permitted-assistance rules.

Separate WGU assessment: the downloaded CBN1 Task 1 architecture proposal
requires Microsoft/Azure services; this AWS implementation does not replace it.

AWS progress: the full five-stage pipeline and all 14 Athena checks passed.
