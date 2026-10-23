-- Replace YOUR_BUCKET with your private course-lab bucket.
CREATE EXTERNAL TABLE IF NOT EXISTS stedi.customer_landing (
  `birthday` string,
  `customername` string,
  `email` string,
  `lastupdatedate` bigint,
  `phone` string,
  `registrationdate` bigint,
  `serialnumber` string,
  `sharewithfriendsasofdate` bigint,
  `sharewithpublicasofdate` bigint,
  `sharewithresearchasofdate` bigint
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('case.insensitive'='true')
STORED AS TEXTFILE
LOCATION 's3://YOUR_BUCKET/landing/customer/'
TBLPROPERTIES ('classification'='json');
