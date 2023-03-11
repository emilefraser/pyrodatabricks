from azureml.core import Workspace
from azureml.mlflow import register_model
from azureml.core.authentication import ServicePrincipalAuthentication

svc_pr = ServicePrincipalAuthentication(
    tenant_id=dbutils.secrets.get(scope = "my-secrets", key = "tenantid"),
    service_principal_id=dbutils.secrets.get(scope = "my-secrets", key = "appid"),
    service_principal_password=dbutils.secrets.get(scope = "my-secrets", key = "auth"))

ws = Workspace.from_config(auth=svc_pr)