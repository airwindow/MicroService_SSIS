import json
import config
import sys
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def add(student):
    if not isinstance(student, dict):
        print 'Student must be of dict type'
        return None
    cfg = config.load_config()
    for schema in cfg['create']['KeySchema']:
        if schema['AttributeName'] not in student:
            print 'All key must be in student'
            return None
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    try:
        response = table.put_item(
                Item=student,
                ConditionExpression=Attr('SSN').ne(student['SSN'])
                )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(e.response['Error']['Message'])
            return False
        else:
            raise

    return response

def load_from_json_dict(json_dict):
    cfg = config.load_config()
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    for student in json_dict:
        print 'Adding student:', student
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        json_file = 'studentsdata.json'
        with open(json_file) as fp:
            json_dict = json.load(fp)
            load_from_json_dict(json_dict)
    else:
        student = {}
        student['SSN'] = sys.argv[1]
        student['LastName'] = sys.argv[2]
        student['FirstName'] = sys.argv[3]
        print add(student)
