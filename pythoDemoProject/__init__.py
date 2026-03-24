import pymysql

# Override the version info to satisfy Django's check
pymysql.version_info = (2, 2, 8, "final", 0) 
pymysql.install_as_MySQLdb()
