-- DDL adapted from the saved project reference for the course-lab bucket.
CREATE EXTERNAL TABLE IF NOT EXISTS stedi.step_trainer_landing (
  `distancefromobject` bigint,
  `sensorreadingtime` bigint,
  `serialnumber` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('case.insensitive'='true')
STORED AS TEXTFILE
LOCATION 's3://d609-stedi-932469575102-20261023/landing/step_trainer/'
TBLPROPERTIES ('classification'='json');
