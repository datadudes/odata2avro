odata2avro [![Build Status](https://travis-ci.org/datadudes/odata2avro.svg?branch=master)](https://travis-ci.org/datadudes/odata2avro) [![Coverage Status](https://coveralls.io/repos/datadudes/odata2avro/badge.svg?branch=master)](https://coveralls.io/r/datadudes/odata2avro?branch=master)
=====

odata2avro is a Python command-line tool to automatically
convert OData datasets to Avro. Using `odata2avro` together with standard
Hadoop tooling, it should be very simple to ingest OData data from
[Microsoft Azure DataMarket](https://datamarket.azure.com/browse/data) to Hadoop.

### Usage:

```
$ odata2avro ODATA_XML AVRO_SCHEMA AVRO_FILE
```

This command reads data from `ODATA_XML` and creates two files: `AVRO_SCHEMA`
 and `AVRO_FILE`. The Avro schema is in JSON format.


### Example: Ingest data from Azure DataMarket to Hive/Impala

```
# Download OData data in XML format
$ curl 'https://api.datamarket.azure.com/opendata.rdw/VRTG.Open.Data/v1/KENT_VRTG_O_DAT?$top=100' > cars.xml

# Convert data to Avro
$ odata2avro cars.xml cars.avsc cars.avro

# Upload to HDFS
$ hdfs dfs -put cars.avro cars.avsc /tmp

# Create Avro-backed Hive table using Avro schema stored in /tmp/cars.avsc
$ hive -e "
  CREATE TABLE cars
  ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
  STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
  OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
  TBLPROPERTIES ('avro.schema.url'='hdfs:///tmp/cars.avsc');"

# Load data from /tmp/cars.avro to the cars table
$ hive -e "LOAD DATA INPATH '/tmp/cars.avro' INTO TABLE cars"

# Query with Impala
$ impala-shell -i <impala-daemon-ip> -q "REFRESH cars; select count(*) from cars"
+----------+
| count(*) |
+----------+
|      100 |
+----------+
```

### Installation:

`pip install odata2avro`


### Contributions:

Please create an issue if you spot any problem or bug.
We'll try to get back to you as soon as possible.

### Authors:

Created with passion by [Marcel](https://github.com/mkrcah)
and [Daan](https://github.com/DandyDev).

