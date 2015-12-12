import sys
import config

def update(student, update):
    if not isinstance(student, dict) or not isinstance(update, dict):
        print 'Student or update must be of dict type'
        return None
    cfg = config.load_config()
    for schema in cfg['create']['KeySchema']:
        if schema['AttributeName'] not in student:
            print 'All key must be in student'
            return None
    db = config.get_db(cfg)
    table = config.get_table(db, cfg)
    exp = []
    exp_attr_vals = {}
    for attr in update:
        var = ':' + ''.join(attr.split('.'))
        exp.append(attr + ' = ' + var)
        exp_attr_vals[var] = update[attr]
    update_exp = 'SET ' + ','.join(exp)
    response = table.update_item(
            Key=student,
            UpdateExpression=update_exp,
            ExpressionAttributeValues=exp_attr_vals,
            ReturnValues='UPDATED_NEW')
    return response

if __name__ == '__main__':
    student = {}
    student['SSN'] = sys.argv[1]
    data = {}
    data[sys.argv[2]] = sys.argv[3]
    print update(student, data)
