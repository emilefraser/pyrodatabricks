# Databricks CLI - Cheat sheet

### Log in
```databricks configure --token```

### Copy a file to DBFS 
```databricks fs cp test.txt dbfs:/test.txt```

```databricks fs cp -r test-dir dbfs:/test-dir```

### Copy a file from DBFS
```databricks fs cp dbfs:/test.txt ./test.txt```

```databricks fs cp -r dbfs:/test-dir ./test-dir```

### List workspace files
```databricks workspace ls /Users/algonzalez@plainconcepts.com```

### Import a local directory of notebooks
```databricks workspace import\_dir . /Users/algonzalez@plainconcepts.com```

```databricks workspace ls /Users/algonzalez@plainconcepts.com -l```

### Export a workspace folder to the local filesystem
```databricks workspace export\_dir /Users/algonzalez@plainconcepts.com .```

### List runtime versions
```databricks clusters spark-versions```

### List node types
```databricks clusters list-node-types```

### Create Clusters
```databricks clusters create --json-file PATH```

`"cluster_name": "my-cluster",
  "spark_version": "5.3.x-scala2.11",
  "node_type_id": "i3.xlarge",
  "spark_conf": {
    "spark.speculation": true
  },
  "aws_attributes": {
    "availability": "SPOT",
    "zone_id": "us-west-2a"
  },
  "num_workers": 25
}`

### Delete Clusters
```databricks clusters delete --cluster-id```

### Get Clusters
```databricks clusters get --cluster-id```

### Cluster restart
```databricks clusters restart --cluster-id```

### Create Pool
```databricks instance-pools create --json-file PATH```

`{
  "instance_pool_name": "my-pool",
  "node_type_id": "i3.xlarge",
  "min_idle_instances": 10,
  "aws_attributes": {
    "availability": "SPOT"
  }
}`

### List Pools
```databricks instance-pools list```

### Create Jobs
```databricks jobs create --json-file PATH```

`{
  "name": "Nightly model training",
  "new_cluster": {
    "spark_version": "6.5.x-cpu-ml-scala2.11",
    "node_type_id": "Standard_DS3_v2",
    "aws_attributes": {
      "availability": "ON_DEMAND"
    },
    "num_workers": 2
  },
  "libraries": [
    {
      "pypi": "azureml-sdk"
    },
    {
      "jar": "dbfs:/my-jar.jar"
    },
    {
      "maven": {
        "coordinates": "org.jsoup:jsoup:1.7.2"
      }
    }
  ],
  "email_notifications": {
    "on_start": [],
    "on_success": [],
    "on_failure": []
  },
  "timeout_seconds": 3600,
  "max_retries": 1,
  "schedule": {
    "quartz_cron_expression": "0 15 22 ? * *",
    "timezone_id": "America/Los_Angeles"
  },
  "spark_jar_task": {
    "main_class_name": "com.databricks.ComputeModels"
  }
}`

### List Jobs
```databricks jobs list```

```databricks jobs list | grep "JOB_NAME"```

### Get Jobs
```databricks jobs get --job-id JOB_ID```

### Jobs run-now
```databricks jobs run-now 
--job-id JOB_ID
--jar-params
--notebook-params JSON
--python-params JSON
--spark-submit-params JSON
```

### Cancel Run
```databricks runs cancel --run-id RUN_ID```

### Get Run
```databricks runs get --run-id RUN_ID```

### List Runs
```databricks runs list```

### List groups databricks groups list
```databricks groups list```

### List groups 
```databricks groups add-member --parent-name TEXT  --user-name TEXT --group-name TEXT```

### List the members of admins
```databricks groups list-members --group-name admins```

### Add group finance 
```databricks groups create --group-name finance```

### Install a JAR from DBFS
```databricks libraries install --cluster-id $CLUSTER_ID --jar dbfs:/test-dir/test.jar```

### List library statuses for a cluster
```databricks libraries list --cluster-id $CLUSTER_ID```

### Create secret scope
```databricks secrets create-scope --scope my-scope --initial-manage-principal users```

### List secret scopes
```databricks secrets list-scopes```

### Delete secret scopes
```databricks secrets delete-scope --scope my-scope```

### Create secrets
```databricks secrets put --scope my-scope --key my-key --string-value my-value```

### List secrets
```databricks secrets list --scope my-scope databricks secrets delete --scope my-scope --key my-key```