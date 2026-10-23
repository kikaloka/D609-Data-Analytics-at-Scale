-- Replace YOUR_BUCKET with your private course-lab bucket.
CREATE EXTERNAL TABLE IF NOT EXISTS stedi.step_trainer_landing (
  `distancefromobject` bigint,
  `sensorreadingtime` bigint,
  `serialnumber` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('case.insensitive'='true')
STORED AS TEXTFILE
LOCATION 's3://YOUR_BUCKET/landing/step_trainer/'
TBLPROPERTIES ('classification'='json');
