# Following one STEDI reading through the lakehouse

[Project home](../README.md) · [Glossary](GLOSSARY.md) · [Architecture](ARCHITECTURE.md)

## 1. Start with the question and source rows

Researchers need phone-motion and step-trainer readings for customers who agreed to research sharing. The pipeline prepares records; it does not evaluate anyone's balance or train a model.

Read the [customer](../sql/customer_landing.sql), [accelerometer](../sql/accelerometer_landing.sql), and [step-trainer](../sql/step_trainer_landing.sql) definitions. A customer row describes a registration. A phone row contains `user`, `timestamp`, and `x`, `y`, `z`. A trainer row contains `serialnumber`, `sensorreadingtime`, and `distancefromobject`. The sensor times are epoch-millisecond integers.

## 2. Filter customers by research consent

In [customer_landing_to_trusted.py](../jobs/customer_landing_to_trusted.py), find `SqlQuery0`:

```sql
SELECT *
FROM myDataSource
WHERE sharewithresearchasofdate IS NOT NULL
```

The source reads `stedi.customer_landing`; the sink writes `stedi.erica_customer_trusted` as Parquet. Historical counts fall from 956 to 482. The other 474 landing records have null consent.

Compare the [landing sample](../evidence/customer_landing.png) and [trusted sample](../evidence/customer_trusted.png). Samples illustrate the rule; the full-table query establishes the recorded zero-missing-consent result. Presence of a consent date does not establish that consent predates a reading or remains active after withdrawal.

## 3. Retain eligible phone readings

[accelerometer_landing_to_trusted.py](../jobs/accelerometer_landing_to_trusted.py) joins `a.user` to `c.email` and selects `a.*`. This retains phone columns while using trusted customers for eligibility. Historical output: 40,981 rows from 81,273 landing rows.

An inner join can multiply rows when several customer rows match one email. This step does not deduplicate customer emails. Inspect key uniqueness before assuming a one-to-one relationship.

## 4. Build the customer research population

[customer_trusted_to_curated.py](../jobs/customer_trusted_to_curated.py) joins the two trusted inputs by email and selects `DISTINCT c.*`. A customer with many phone readings should appear once per distinct selected customer record, rather than once per reading. Historical output: 482 rows in `erica_customers_curated` (plural).

`DISTINCT` removes identical selected rows. It does not enforce unique email addresses or prove that a reused device serial identifies one person.

## 5. Retain eligible device readings

[step_trainer_trusted.py](../jobs/step_trainer_trusted.py) joins trainer and curated customer records by `serialnumber`, then selects `DISTINCT s.*`. Historical output: 14,460 rows from 28,680 landing rows. Selecting only device fields prevents matching customer fields from changing the row shape; `DISTINCT` removes identical selected device observations.

This is a serial-membership rule. The job does not reconstruct historical device ownership intervals.

## 6. Pair the sensors

[machine_learning_curated.py](../jobs/machine_learning_curated.py) uses:

```sql
FROM s
INNER JOIN a
    ON s.sensorreadingtime = a.timestamp
```

The output contains trainer serial/time/distance and phone user/time/x/y/z. It retains every matching timestamp pair. Historical output: 43,681 rows. The total can exceed either input because multiple readings can share a timestamp. For illustration, two trainer rows and three phone rows at one time produce six pairs; this is not a new measurement of the course data.

There is no person-identity condition in this final join. Describe the output as timestamp-paired readings, not verified same-person pairs.

## 7. Understand the generated wrapper

Each export initializes Glue/Spark, reads catalog tables as DynamicFrames, exposes SQL aliases through `sparkSqlQuery`, evaluates `ColumnCount > 0`, and writes Parquet with catalog updates. The default rule only checks that columns exist. Separate Athena queries check table counts and consent.

The five files are independent exports. Their data dependencies require the order above, but no scheduler or infrastructure deployment is included. [Setup](SETUP.md) explains reproduction prerequisites and rerun behavior.

## 8. Give a short portfolio tour

Explain the research question, show the consent SQL and its evidence, explain the two uses of `DISTINCT`, and finish with the timestamp join and its limitation. Describe the hands-on visual configuration and assistance accurately using [Acknowledgments](ACKNOWLEDGMENTS.md).

Possible future work includes identity-aware pairing, event-time consent, uniqueness checks, orchestration, and idempotent publication. None is implemented or tested by this documentation update. Keep experiments separate from the passing baseline.
