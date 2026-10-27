-- DDL adapted from the saved project reference for the course-lab bucket.
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
LOCATION 's3://d609-stedi-932469575102-20261023/landing/accelerometer/'
TBLPROPERTIES ('classification'='json');
