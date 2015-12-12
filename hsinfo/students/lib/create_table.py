import boto3
import config

cfg = config.load_config()
db = config.get_db(cfg)
dbclient = db.meta.client
table_list = dbclient.list_tables()['TableNames']
if cfg['table'] not in table_list:
    create = cfg['create']
    try:
        table = db.create_table(
                TableName=cfg['table'],
                KeySchema=create['KeySchema'],
                AttributeDefinitions=create['AttrDef'],
                ProvisionedThroughput=create['Provision']
        )
        print 'Table %s status: %s' % (cfg['table'], table.table_status)
    except Exception as e:
        print(e)
else:
    table = config.get_table(db, cfg)
    print '%s has been created.' % cfg['table']
    print 'Table status: %s' % table.table_status
