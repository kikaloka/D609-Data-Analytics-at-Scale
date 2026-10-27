SELECT 'customer_landing' AS check_name, COUNT(*) AS actual_value FROM stedi.customer_landing
UNION ALL SELECT 'accelerometer_landing', COUNT(*) FROM stedi.accelerometer_landing
UNION ALL SELECT 'step_trainer_landing', COUNT(*) FROM stedi.step_trainer_landing
UNION ALL SELECT 'erica_customer_trusted', COUNT(*) FROM stedi.erica_customer_trusted
UNION ALL SELECT 'erica_accelerometer_trusted', COUNT(*) FROM stedi.erica_accelerometer_trusted
UNION ALL SELECT 'erica_customers_curated', COUNT(*) FROM stedi.erica_customers_curated
UNION ALL SELECT 'erica_step_trainer_trusted', COUNT(*) FROM stedi.erica_step_trainer_trusted
UNION ALL SELECT 'erica_machine_learning_curated', COUNT(*) FROM stedi.erica_machine_learning_curated
UNION ALL SELECT 'landing_missing_consent', COUNT(*) FROM stedi.customer_landing WHERE sharewithresearchasofdate IS NULL
UNION ALL SELECT 'trusted_missing_consent', COUNT(*) FROM stedi.erica_customer_trusted WHERE sharewithresearchasofdate IS NULL;