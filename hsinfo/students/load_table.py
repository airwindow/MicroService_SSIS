import boto3
import json
import config
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

json_file = 'studentsdata.json'
with open(json_file) as fp:
    json_dict = json.load(fp)
    cfg = config.load_config()
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    for student in json_dict:
        print('Adding student:', student)
        try:
            table.put_item(
                    Item=student,
                    ConditionExpression=Attr('SSN').ne(student['SSN'])
                    )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(e.response['Error']['Message'])
            else:
                raise
