#!/bin/bash
#To set class-specific logging on the driver or on workers, use the following script:

#%sh

echo "Executing on Driver: $DB_IS_DRIVER"
if [[ $DB_IS_DRIVER = "TRUE" ]]; then
    LOG4J_PATH="/home/ubuntu/databricks/spark/dbconf/log4j/driver/log4j.properties"
else
    LOG4J_PATH="/home/ubuntu/databricks/spark/dbconf/log4j/executor/log4j.properties"
fi

echo "Adjusting log4j.properties here: ${LOG4J_PATH}"

#Replace <custom-prop> with the property name, and <value> with the property value.
# Upload the script to DBFS and select a cluster using the cluster configuration UI.
# You can also set log4j.properties for the driver in the same way.
echo "log4j.<custom-prop>=<value>" >> ${LOG4J_PATH}


