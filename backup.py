import sys

import storage

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3 or args[0] not in ('restore', 'backup'):
        print('Invalid arguments')
        exit()

    operation_type, filename, mongo_url = args
    if operation_type == 'backup':
        storage.backup(mongo_url, filename)
    else:
        storage.restore(mongo_url, filename)