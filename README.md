# Azure Sandbox

```sh
sudo su;
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -;
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list;

sudo apt update;
sudo apt install msodbcsql17;
```

```sql
CREATE EXTERNAL DATA SOURCE dbt WITH
(
	TYPE=HADOOP,
	LOCATION='abfs://dagster.dfs.core.windows.net/dagster/dagster/edfi_api/'
)

CREATE EXTERNAL FILE FORMAT json_format
WITH
(  
    FORMAT_TYPE=DELIMITEDTEXT,
    FORMAT_OPTIONS (
        FIELD_TERMINATOR='0x0b'
    )
)

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;

CREATE EXTERNAL TABLE analytics.edfi_grading_periods
( 
   [is_complete_extract] [varchar],
   [id] [varchar]
)
WITH (
	DATA_SOURCE = dbt,
	LOCATION = N'base_edfi_grading_periods/school_year=*/date_extracted=*/extract_type=*/*.json',
	FILE_FORMAT = json_format);
```

```sh
dbt run-operation stage_external_sources;
```

```sql
SELECT
    JSON_VALUE(jsonContent, '$.studentUniqueId')    AS student_unique_id,
    JSON_VALUE(jsonContent, '$.lastSurname')        AS last_surname,
    JSON_VALUE(jsonContent, '$.firstName')          AS first_name
FROM
    OPENROWSET(
        BULK 'https://dagster.dfs.core.windows.net/dagster/dagster/edfi_api/base_edfi_grading_periods/school_year=*/date_extracted=*/extract_type=*/*.json',
        FORMAT = 'CSV',
        FIELDQUOTE = '0x0b',
        FIELDTERMINATOR ='0x0b',
        ROWTERMINATOR = '0x0b'
    )
    WITH (
        jsonContent varchar(MAX)
    ) AS edfi
WHERE
    edfi.filepath(1) = 2022
    AND edfi.filepath(3) = 'records'
```
