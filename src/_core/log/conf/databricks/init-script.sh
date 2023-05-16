#/bin/bash -c

echo Setting the log4j configuration on the driver
SOURCE_LOG4J_PATH=/dbfs/logs-config/log4j2.xml
DRIVER_LOG4J_PATH=/databricks/spark/dbconf/log4j/driver/log4j.xml
DRIVER_LOG4J2_PATH=/databricks/spark/dbconf/log4j/driver/log4j2.xml

echo "writing ${SOURCE_LOG4J_PATH} properties to ${DRIVER_LOG4J_PATH}"
cp ${SOURCE_LOG4J_PATH} ${DRIVER_LOG4J_PATH}
cp ${SOURCE_LOG4J_PATH} ${DRIVER_LOG4J2_PATH}
echo Setting the log4j configuration on the driver - done

