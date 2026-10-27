# Reviewing and reproducing the project

## Review without AWS

A text editor or GitHub is enough to read scripts, SQL, and historical evidence. The exports import `awsglue`, `awsgluedq`, and PySpark. Ordinary local Python is not a Glue runtime. Syntax parsing is not execution of transformations.

Start with [Walkthrough](WALKTHROUGH.md) and [Validation](VALIDATION.md). No infrastructure is needed to understand the portfolio.

## Before a future authorized reproduction

The exports retain the original database, table names, and S3 paths. They record the passing implementation; they are not portable deployment scripts. The following is a preparation guide, not a claim of a new tested deployment.

1. Obtain the official [Udacity starter data](ACKNOWLEDGMENTS.md). Record its version; another dataset may produce different counts.
2. Identify the region, compatible Glue runtime, execution role, source locations, separate output prefixes, script/temporary storage, and Athena results location. Keep credentials outside the repository.
3. Provide the catalog database. The submitted DDLs assume `stedi`; provisioning for the database, IAM, and networking is not included.
4. Review the three [landing DDLs](../sql/) before execution. In a separate reproduction copy, adapt their old-lab S3 locations to the intended source and verify JSON SerDe and field types.
5. Configure the five Glue Studio jobs using the catalog reads, SQL, and sinks shown in the exports. A Python export does not restore an editable visual graph; recreate the nodes if visual editing is needed, and export that version separately.
6. Choose job runtime, workers, timeout, and related settings deliberately. The Python files alone do not establish all job settings. Do not infer them from a syntax check.

## Order and validation checkpoints

| Step | Job | Check before continuing |
|---|---|---|
| 1 | Customer landing to trusted | Customer count and missing consent |
| 2 | Accelerometer landing to trusted | Output count and email eligibility |
| 3 | Customer trusted to curated | Customer count and distinct selected rows |
| 4 | Step-trainer trusted | Device count and serial membership |
| 5 | Machine-learning curated | Final count, schema, and timestamp pair behavior |

Execute only in an authorized environment. Inspect each table and its location; job success alone does not establish correct data. The included [rubric validation SQL](../sql/rubric_validation.sql) supplies count/consent checks. Adjust names only in the separate reproduction copy and keep all downstream reads aligned with that version.

## Keep runs separate

The sinks write fixed prefixes. `job.commit()` and `UPDATE_IN_DATABASE` do not guarantee idempotent overwrite. Reusing populated output locations can accumulate duplicate files. Plan fresh output locations and matching catalog mappings; do not delete historical evidence or source data to make counts match.

For a new run, record dataset version, job settings, run/query IDs, locations, observation date, and actual counts. Save new screenshots separately from October 26 evidence. This portfolio update performed no cloud execution.

[Back to the project](../README.md)
