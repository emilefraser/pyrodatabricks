aws_bucket_name = "my-bucket"
mount_name = "s3-my-bucket"

dbutils.fs.updateMount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name)