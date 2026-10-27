# STEDI: from sensor readings to research-ready tables

STEDI collects customer registrations, phone-motion readings, and step-trainer measurements. This project brings those sources together in an AWS lakehouse so researchers can work with readings from customers who recorded research consent.

AWS Glue Studio defines five visual jobs. Spark runs their SQL transformations, S3 holds JSON and Parquet files, the Glue Data Catalog describes the tables, and Athena checks the results.

```text
Customer landing -> consent filter -> Customer trusted
Phone landing + Customer trusted -> Accelerometer trusted
Customer trusted + Accelerometer trusted -> Customers curated
Device landing + Customers curated -> Step-trainer trusted
Step-trainer trusted + Accelerometer trusted -> Machine-learning curated
```

## What the project demonstrates

- Five dependent Glue Studio workflows with preserved Python exports.
- JSON landing tables and Snappy Parquet outputs in landing, trusted, and curated layers.
- Consent filtering, email and serial-number joins, and deliberate row selection.
- Athena validation that distinguishes sample rows from full-table counts.
- Documentation of what the timestamp join establishes and what it cannot establish.

## Results and limits

**D609 Udacity submission passed**, as confirmed by Erica after evaluation. This portfolio preserves the submitted implementation and historical evidence. Preparing these guides did not run AWS jobs or query AWS.

The October 26, 2026 Athena record shows **43,681 final rows**, **482 trusted customers**, and **zero trusted customer rows with missing research consent**. See [Validation](docs/VALIDATION.md) for all eight table counts and source evidence. Course acceptance and a successful data check are separate kinds of evidence.

Equal timestamps do not prove that a phone and device belong to the same person. The jobs do not enforce consent effective at reading time, anonymize output, or train a model. Reruns can append files to existing output folders. These are limits of the course implementation, not changes made by this portfolio refresh.

## Find your way around

| Start here | What you will find |
|---|---|
| [Walkthrough](docs/WALKTHROUGH.md) | Follow each transformation from source through SQL to output |
| [Glossary](docs/GLOSSARY.md) | Plain-language terms with project examples |
| [Architecture](docs/ARCHITECTURE.md) | Dependencies, row grain, service roles, and tradeoffs |
| [Jobs](jobs/) | Five preserved Glue Studio Python exports |
| [SQL](sql/) | Landing definitions and count/consent queries |
| [Evidence](evidence/README.md) | Original Athena screenshots and their limits |
| [Setup](docs/SETUP.md) | Offline review and future reproduction prerequisites |
| [Validation](docs/VALIDATION.md) | Table mapping, historical results, and diagnostics |
| [Acknowledgments](docs/ACKNOWLEDGMENTS.md) | Udacity sources and assistance |
| [Version notes](docs/VERSION-NOTES.md) | Passing baseline and scope of this update |

For a quick portfolio review, inspect the consent transformation, compare its sample screenshot with the full-table consent check, then read the final join and its limitations. No AWS connection is needed.
