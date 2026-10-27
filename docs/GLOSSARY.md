# STEDI glossary

| Term | Meaning here |
|---|---|
| Lakehouse | Object-store files organized into queryable analytical tables |
| Landing | Incoming JSON before filtering and joins |
| Trusted | Records retained by the applicable eligibility rule |
| Curated | Derived records prepared for the research use case |
| S3 object/prefix | A file and its path-like grouping; one prefix can contain several runs |
| Glue Studio | Visual editor that generated the five Python exports |
| Spark / PySpark | Distributed engine and its Python interface |
| DynamicFrame | Glue abstraction converted to a Spark DataFrame by the SQL helper |
| DataFrame | Table-like rows and columns used by Spark SQL |
| Data Catalog | Names, schema, format, and S3 locations for tables |
| Athena | SQL service used to inspect cataloged data |
| SerDe | Serializer/deserializer; the landing definitions specify a JSON reader |
| Parquet / Snappy | Column-oriented output format and its compression |
| Grain | What one row represents; a final row is a pair, not a customer |
| Inner join | Retains matches; repeated keys can multiply rows |
| DISTINCT | Removes identical selected rows, not every repeated identifier |
| Null | Missing value; `IS NOT NULL` is the consent filter |
| Epoch milliseconds | Integer milliseconds since the Unix epoch |
| Idempotence | Repeating work has the effect of running it once; not guaranteed by these sinks |
| Catalog update | Metadata change, not deletion of existing output objects |
| Full-table check | Query over all rows, unlike a limited sample screenshot |
| Provenance | The source version, environment, query, and time behind a result |
| Static verification | Inspecting files without running the cloud pipeline |

[Walkthrough](WALKTHROUGH.md) · [Setup](SETUP.md) · [Project home](../README.md)
