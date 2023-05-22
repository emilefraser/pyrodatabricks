# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## DevOps notebook dealing with:
# MAGIC - Source Control
# MAGIC - Version History 
# MAGIC - CICD

# COMMAND ----------

# MAGIC %sh 
# MAGIC
# MAGIC databricks fs ls

# COMMAND ----------

# MAGIC %sh
# MAGIC # databricks workspace list -l --absolute / | cut -d " " -f 1 
# MAGIC databricks workspace list -l --absolute / | cut -d " " -f 3,4 | awk '{ print "\""$0"\""}' 

# COMMAND ----------

# MAGIC %sh
# MAGIC databricks workspace list -l --absolute | awk '{ print "\""$0"\""}' 

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC a=($(databricks workspace list -l --absolute))
# MAGIC echo ${b[@]}
# MAGIC #echo ${a[@]}
# MAGIC #echo ${a[7]}
# MAGIC #echo ${a[8]}
# MAGIC
# MAGIC for elem in "${a[@]}"
# MAGIC do
# MAGIC   echo $elem
# MAGIC done

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC
# MAGIC # databricks workspace list -l --absolute "${ws_path}"
# MAGIC
# MAGIC function traverse_ws() {
# MAGIC   
# MAGIC   ws_path="${1}"
# MAGIC   path_dir=($(databricks workspace list -l --absolute "${ws_path}"))
# MAGIC   path_dir_size=$(echo $(((${#path_dir[@]}))))
# MAGIC   path_dir_iters=$((($path_dir_size+1)/2))
# MAGIC   
# MAGIC   for i in $(seq 1 $path_dir_iters)
# MAGIC   do
# MAGIC     echo "${path_dir[i]}"
# MAGIC   done
# MAGIC
# MAGIC #   for ws_object in 
# MAGIC #   do
# MAGIC #       object_type = $(echo $ws_object | cut -d " " -f 1)
# MAGIC #       echo "object type: ${ws_object}"
# MAGIC #       if [ "${object_type}"  == 'DIRECTORY' ] ; then 
# MAGIC #           echo "${ws_object} is a folder, entering..."
# MAGIC #           traverse_ws "${ws_object}"
# MAGIC #       else
# MAGIC #           echo "${ws_object} is not a folder"
# MAGIC #       fi
# MAGIC #   done
# MAGIC }
# MAGIC
# MAGIC
# MAGIC ws_path='/'
# MAGIC traverse_ws "${ws_path}"

# COMMAND ----------

# MAGIC %sh
# MAGIC function traverse() {
# MAGIC   for file in "$1"/*
# MAGIC   do
# MAGIC     if [ ! -d "${file}" ] ; then
# MAGIC         echo "${file} is a file"
# MAGIC     else
# MAGIC         echo "entering recursion with: ${file}"
# MAGIC         traverse "${file}"
# MAGIC     fi
# MAGIC   done
# MAGIC }
# MAGIC
# MAGIC traverse "." 
# MAGIC databricks workspace list -l --absolute / 

# COMMAND ----------

# MAGIC %sh
# MAGIC pwdtt
# MAGIC ls
# MAGIC git status

# COMMAND ----------

# MAGIC %sh
# MAGIC mkdir test
# MAGIC ls

# COMMAND ----------

# MAGIC %sh
# MAGIC cd test
# MAGIC git init

# COMMAND ----------

add all artefacts
use git to puah
normal cicd
location of repo

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC databricks fs ls dbfs:/mnt/repo

# COMMAND ----------

# MAGIC %sh 
# MAGIC workspace_name="az-db-pyr-prd-san-01"
# MAGIC databricks fs mkdirs "dbfs:/mnt/repo/${workspace_name}"

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC databricks fs ls dbfs:/mnt/repo

# COMMAND ----------

# MAGIC %sh 
# MAGIC workspace_name="az-db-pyr-prd-san-01"
# MAGIC git -C "/dbfs/mnt/repo/az-db-pyr-prd-san-01" init .
# MAGIC #ls ../../dbfs/mnt/repo/az-db-pyr-prd-san-01

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC databricks fs ls dbfs:/mnt/repo/az-db-pyr-prd-san-01

# COMMAND ----------

 root_path="dbfs:/mnt/repo/az-db-pyr-prd-san-01"
 repo_folders=
 
 databricks fs mkdirs "dbfs:/mnt/repo/az-db-pyr-prd-san-01"

# COMMAND ----------

# MAGIC %sh ls /tmp/

# COMMAND ----------

# MAGIC %sh 
# MAGIC databricks fs ls dbfs:

# COMMAND ----------

dbutils.fs.ls("/mnt/")

# COMMAND ----------

# MAGIC %fs ls file:/tmp

# COMMAND ----------

dbutils.fs.ls ("/tmp/")

# COMMAND ----------

# MAGIC %sh 
# MAGIC ss=()
# MAGIC a="dssfsd"

# COMMAND ----------

# MAGIC %sh
# MAGIC ss+="gekki"

# COMMAND ----------

# MAGIC %sh
# MAGIC echo "${ss}"
# MAGIC echo $a

# COMMAND ----------

# MAGIC %sh 
# MAGIC # ges the root folders of the workspace
# MAGIC databricks workspace list -l --absolute / | cut -d " " -f 1 
# MAGIC databricks workspace list -l --absolute / | cut -d " " -f 3

# COMMAND ----------

# MAGIC %sh 
# MAGIC directories=()
# MAGIC directories+=($(databricks workspace list - ))
# MAGIC echo $directories

# COMMAND ----------

# MAGIC %fs 
# MAGIC ls -l

# COMMAND ----------

# MAGIC %python
# MAGIC import os
# MAGIC l = ['A', 'B', 'C', 'D']
# MAGIC os.environ['LIST'] = ' '.join(l)
# MAGIC print(os.getenv('LIST'))

# COMMAND ----------

# MAGIC %sh
# MAGIC for i in $LIST
# MAGIC do
# MAGIC   echo $i
# MAGIC done

# COMMAND ----------

k = ['A', 'B', 'C', 'D']


# COMMAND ----------

# MAGIC %sh
# MAGIC for i in $k
# MAGIC do
# MAGIC   echo $i
# MAGIC done

# COMMAND ----------

l = ['A', 'B', 'C']


# COMMAND ----------

# MAGIC %%bash -s "$l"
# MAGIC for i in $1
# MAGIC do
# MAGIC echo $i
# MAGIC done

# COMMAND ----------

# MAGIC %%bash -s "{" ".join(l)}"
# MAGIC for i in $1
# MAGIC do
# MAGIC echo $i
# MAGIC done

# COMMAND ----------

# MAGIC %python
# MAGIC with open('varL.txt', 'w') as f:
# MAGIC   for elem in l:
# MAGIC     f.write(elem+'\n')
# MAGIC   f.close()  
# MAGIC
# MAGIC %%bash
# MAGIC pwd
# MAGIC ls -lh varL.txt
# MAGIC echo '=======show content=========='
# MAGIC cat varL.txt
# MAGIC echo '=====result of script========'
# MAGIC for i in $(cat varL.txt)
# MAGIC do
# MAGIC   echo $i
# MAGIC done

# COMMAND ----------

dbutils.fs.ls("/")

# COMMAND ----------

dbutils.fs.help("ls")