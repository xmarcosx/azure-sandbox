# Azure Sandbox

```sql
SELECT
    JSON_VALUE(jsonContent, '$.studentUniqueId')    AS student_unique_id,
    JSON_VALUE(jsonContent, '$.lastSurname')        AS last_surname,
    JSON_VALUE(jsonContent, '$.firstName')          AS first_name
FROM
    OPENROWSET(
        BULK 'https://dagster.dfs.core.windows.net/dagster/dagster/edfi_api/base_edfi_students/school_year=*/date_extracted=*/extract_type=*/*.json',
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
