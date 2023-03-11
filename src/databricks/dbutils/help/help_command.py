dbutils.fs.help("cp")

# /**
# * Copies a file or directory, possibly across FileSystems.
# *
# * Example: cp("/mnt/my-folder/a", "dbfs:/a/b")
# *
# * @param from FileSystem URI of the source file or directory
# * @param to FileSystem URI of the destination file or directory
# * @param recurse if true, all files and directories will be recursively copied
# * @return true if all files were successfully copied
# */
# cp(from: java.lang.String, to: java.lang.String, recurse: boolean = false): boolean