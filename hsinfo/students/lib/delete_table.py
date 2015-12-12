import boto3
import config

cfg = config.load_config()
db = config.get_db(cfg)
dbclient = db.meta.client
table_list = dbclient.list_tables()['TableNames']
if cfg['table'] in table_list:
    table = config.get_table(db, cfg)
    table.delete()
    print 'Table %s is deleted.' % cfg['table']
else:
    print 'Table %s does not exist.' % cfg['table']
