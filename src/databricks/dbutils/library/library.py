# install(path: String): boolean -> Install the library within the current notebook session
# installPyPI(pypiPackage: String, version: String = "", repo: String = "", extras: String = ""): boolean -> Install the PyPI library within the current notebook session
# list: List -> List the isolated libraries added for the current notebook session via dbutils
# restartPython: void -> Restart python process for the current notebook session
# updateCondaEnv(envYmlContent: String): boolean -> Update the current notebook's Conda environment based on the specification (content of environment