# Common variables for an OPF Postgres environment
# Those variables can be overridden by adding a .py file

#Common database variables
datasourceServer = 'dbserver'
datasourceDBPort = '5432'
datasourceAuthAlias = 'bphdb'
datasourceAuthUserName = 'xct_16_6_postgres'
datasourceAuthPassword = 'password'
datasourcePGDatabaseName = 'bph'
datasourcePGSchema = 'xct_16_6_postgres'

# Connection pool variables
poolConnectionTimeout = '180'
poolMaxConnections = '120'
poolUnusedTimeout = '1800'
poolMinConnections = '1'
poolPurgePolicy = 'EntirePool'
poolAgedTimeout = '300'
poolReapTime = '180'
