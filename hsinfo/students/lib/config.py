import boto3
import json

def load_config():
    config = None
    with open('students/lib/config.json') as config_json:
        config = json.load(config_json)
    return config

def get_db(cfg):
    return boto3.resource('dynamodb', endpoint_url=cfg['dynamodb'])

def get_table(db, cfg):
    return db.Table(cfg['table'])

if __name__ == '__main__':
    print load_config()