-- Replace YOUR_BUCKET with your private course-lab bucket.
CREATE EXTERNAL TABLE IF NOT EXISTS stedi.accelerometer_landing (
  `timestamp` bigint,
  `user` string,
  `x` double,
  `y` double,
  `z` double
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('case.insensitive'='true')
STORED AS TEXTFILE
LOCATION 's3://YOUR_BUCKET/landing/accelerometer/'
TBLPROPERTIES ('classification'='json');
