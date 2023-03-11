# PowerShell Modules for Azure Databricks

This repository contains the source code to create different Databricks artifact by powershell scripts. The scripts was developed using Databricks docs to create the correspondent API endpoints.

It works for Databricks on Azure and also AWS. The APIs are almost identical so I decided to bundle them in one single module. The official API documentations can be found here:

Azure Databricks - https://docs.azuredatabricks.net/api/latest/index.html

# Usage
Go to your project directory an execute the root powershel file with the name `./Deploy.ps1'`. You'll have to enter severals parameters to have a succesfull execution:

1. subscriptionId
2. resourceGroupName
3. tenantId
4. location
5. databricksWorkspace
6. servicePrincipalId
7. servicePrincipalPassword
8. armOutputs
9. dbLocalPathsDBFSSettings
10. dbLocalPathSharedFiles

The tasks that this powershell script will do, are:

1. Login
2. Get settings from localsetttings.json
3. Get a token for the global Databricks application
4. Get a token for the Azure management API
5. Create Azure Databricks Token
6. Creating Azure Databricks Cluster
7. Creating Azure Databricks Secrets
8. Uploading necessary settings files to DBFS (Databricks File System)
9. Uploading Notebooks and Shared files to Azure Databricks Workspace

# Supported APIs and endpoint
- Clusters API ([Azure](https://docs.azuredatabricks.net/api/latest/clusters.html))
- Secrets API ([Azure](https://docs.azuredatabricks.net/api/latest/secrets.html))
- Token API ([Azure](https://docs.azuredatabricks.net/api/latest/tokens.html),)
- Workspace API ([Azure](https://docs.azuredatabricks.net/api/latest/workspace.html))
- DBFS API ([Azure](https://docs.azuredatabricks.net/api/latest/dbfs.html))

# Not yet supported APIs
- SCIM API ([Azure](https://docs.azuredatabricks.net/api/latest/scim.html))
- Groups API ([Azure](https://docs.azuredatabricks.net/api/latest/groups.html))
- Jobs API ([Azure](https://docs.azuredatabricks.net/api/latest/jobs.html))
- Libraries API ([Azure](https://docs.azuredatabricks.net/api/latest/libraries.html))

## ARM Template to deploy Azure Databricks + Azure Machine Learning Service
You can find it on `./arm_templates` folder. Inside it, you have the ARM template `./arm_templates/cloud-environment.json` and also a few files more. 

*Note: All this files was developed thinking on Azure DevOps Pipeline. First deploy on IaC infrastructure all resources on Azure.
Then extract outputs from ARM template, create aml config to use in Azure Databricks, create the init script and the final step will be execute powershells azure databricks to create artifacts on it* 

Example of DevOps Pipeline flow:

1. IaC with `./arm_templates/cloud-environment.json`
2. Get ARM ouptuts with `./arm_templates/ArmOutput.ps1`
2. Create/Fill AML config json `./arm_templates/Create-aml-config.ps1`
3. Create/Fill Init Databricks cluster script`./arm_templates/Create-Init-Script.ps1`
4. Deploy the files generated before and start the creation of Azure Databricks Artifacts (Token, DBFS files, Cluster, Workspace directories, Secrets...)`./Deploy.ps1'`

## Databricks CLI Cheat Sheet
Find on `./Databricks-cli` folder!
