from src.datasource.blg_database import BlgDatabase

ENV_CFG_PRODUCTION = "/Users/vincent/.pythonbot/blg_akaun_master_db_production.json"
ENV_CFG_STAGING = "/Users/vincent/.pythonbot/blg_akaun_master_db_staging.json"
ENV_CFG_DEVELOPMENT = "/Users/vincent/.pythonbot/blg_akaun_master_db_development.json"

dbProd = BlgDatabase()
dbProd.read_json_config(ENV_CFG_PRODUCTION)
print("Production.....")
print(dbProd)
dbProd.init_ssh_tunnel()
dbProd.init_sqlalchemy_engine()
dbProd.init_psycopg_engine()

dbStg = BlgDatabase()
dbStg.read_json_config(ENV_CFG_STAGING)
print("Staging.....")
print(dbStg)
dbStg.init_ssh_tunnel()
dbStg.init_sqlalchemy_engine()
dbStg.init_psycopg_engine()



dbDev = BlgDatabase()
dbDev.read_json_config(ENV_CFG_DEVELOPMENT)
print("Development.....")
print(dbDev)
dbDev.init_ssh_tunnel()
dbDev.init_sqlalchemy_engine()
dbDev.init_psycopg_engine()

