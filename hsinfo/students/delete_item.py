import sys
import config

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
    return response

if __name__ == '__main__':
    key = {}
    key['SSN'] = sys.argv[1]
    print delete(key)
