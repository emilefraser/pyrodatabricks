metrics = last_version["operationMetrics"]
assert metrics["numOutputRows"] == "5", "Make sure you only insert delicious beans"
assert metrics["numTargetRowsUpdated"] == "1", "Make sure you match on name and color"
assert metrics["numTargetRowsInserted"] == "2", "Make sure you insert newly collected beans"
assert metrics["numTargetRowsDeleted"] == "0", "No rows should be deleted by this operation"