import json
import config
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError



# add a student into K-12 Database
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



# delete a student
def delete(student):
    if not isinstance(student, dict):
        print 'Student must be of dict type'
        return None
    cfg = config.load_config()
    for schema in cfg['create']['KeySchema']:
        if schema['AttributeName'] not in student:
            print 'All keys must be in student'
            return None
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    response = table.delete_item(Key=student)
    print "I was called!"
    return response



# list all records in K-12 database 
def get_all():
    cfg = config.load_config()
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    response = table.scan()
    return response



# list a student's info in K-12 database
def get(student):
    if not isinstance(student, dict):
        print('Student must be of dict type')
        return None
    cfg = config.load_config()
    for schema in cfg['create']['KeySchema']:
        if schema['AttributeName'] not in student:
            print 'All keys must be in student'
            return None
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    response = table.get_item(Key=student)
    return response



# update a student's information
# def update(student, update):
#     if not isinstance(student, dict) or not isinstance(update, dict):
#         print 'Student or update must be of dict type'
#         return None
#     cfg = config.load_config()
#     for schema in cfg['create']['KeySchema']:
#         if schema['AttributeName'] not in student:
#             print 'All key must be in student'
#             return None
#     db = config.get_db(cfg)
#     table = config.get_table(db, cfg)
#     exp = []
#     exp_attr_vals = {}
#     for attr in update:
#         var = ':' + ''.join(attr.split('.'))
#         exp.append(attr + ' = ' + var)
#         exp_attr_vals[var] = update[attr]
#     update_exp = 'SET ' + ','.join(exp)
#     response = table.update_item(
#             Key=student,
#             UpdateExpression=update_exp,
#             ExpressionAttributeValues=exp_attr_vals,
#             ReturnValues='UPDATED_NEW')
#     return response