abfss://metadata@nasdevcurdlswus01.dfs.core.windows.net/unity_catalog

nasdevcuracdbwus01 
8debc92f-7749-40b7-ad07-d4b468e13512



nasdevmtddlswus01



databricks

databricks unity-catalog storage-credentials create --name nasdevmtdstcwus01 --az-mi-access-connector-id /subscriptions/001c8981-6e75-46d9-af97-176f82648ea3/resourceGroups/nas-dev-cur-wus01/providers/Microsoft.Databricks/accessConnectors/nasdevcuracdbwus01


The Azure resource ID of the Azure
                                  Databricks Access Connector. Use the format,
                                  /subscriptions/{guid}/resourceGroups/{rg-nam
                                  e}/providers/Microsoft.Databricks/accessConn
                                  ectors/{connector-name}



databricks unity-catalog metastores create --help


abfss://databricks@nasdevmtddlswus01.dfs.core.windows.net/unity_catalog




databricks unity-catalog metastores create --name nasdevmtsdlswus01 --region WUS01 --storage-root abfss://databricks@nasdevmtddlswus01.dfs.core.windows.net/unity_catalog




databricks unity-catalog metastores create --name az-dbms-pyr-san-01 --region southafricanorth --storage-root abfss://metadata@azstg2datprdsan01.dfs.core.windows.net/unity_catalog --profile personal


{
  "name": "az-dbms-pyr-san-01",
  "storage_root": "abfss://metadata@azstg2datprdsan01.dfs.core.windows.net/unity_catalog/f0543b12-8705-4240-9076-1c57ffd60724",
  "delta_sharing_scope": "INTERNAL",
  "owner": "efraser25@gmail.com",
  "privilege_model_version": "1.0",
  "region": "southafricanorth",
  "metastore_id": "f0543b12-8705-4240-9076-1c57ffd60724",
  "created_at": 1679003780206,
  "created_by": "efraser25@gmail.com",
  "updated_at": 1679003780206,
  "updated_by": "efraser25@gmail.com",
  "cloud": "azure",
  "global_metastore_id": "azure:southafricanorth:f0543b12-8705-4240-9076-1c57ffd60724",
  "full_name": "az-dbms-pyr-san-01",
  "securable_type": "METASTORE",
  "securable_kind": "METASTORE_STANDARD"
}
