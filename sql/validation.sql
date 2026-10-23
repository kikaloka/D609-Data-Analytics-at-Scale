-- Run after all five Glue jobs succeed. Save actual Athena results as evidence.

SELECT 'customer_landing' AS table_name, COUNT(*) AS actual_rows, 956 AS expected_rows FROM stedi.customer_landing;

SELECT 'accelerometer_landing' AS table_name, COUNT(*) AS actual_rows, 81273 AS expected_rows FROM stedi.accelerometer_landing;

SELECT 'step_trainer_landing' AS table_name, COUNT(*) AS actual_rows, 28680 AS expected_rows FROM stedi.step_trainer_landing;

SELECT 'customer_trusted' AS table_name, COUNT(*) AS actual_rows, 482 AS expected_rows FROM stedi.customer_trusted;

SELECT 'accelerometer_trusted' AS table_name, COUNT(*) AS actual_rows, 40981 AS expected_rows FROM stedi.accelerometer_trusted;

SELECT 'customers_curated' AS table_name, COUNT(*) AS actual_rows, 482 AS expected_rows FROM stedi.customers_curated;

SELECT 'step_trainer_trusted' AS table_name, COUNT(*) AS actual_rows, 14460 AS expected_rows FROM stedi.step_trainer_trusted;

SELECT 'machine_learning_curated' AS table_name, COUNT(*) AS actual_rows, 43681 AS expected_rows FROM stedi.machine_learning_curated;

SELECT COUNT(*) AS invalid_consent_rows FROM stedi.customer_trusted WHERE sharewithresearchasofdate IS NULL;

SELECT * FROM stedi.customer_landing WHERE sharewithresearchasofdate IS NULL LIMIT 10;

SELECT * FROM stedi.customer_trusted LIMIT 10;
