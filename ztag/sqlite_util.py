#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 19-2-1
import json
import sqlite3

# sql_str = '''CREATE TABLE "colasoft_ftp" (
#   "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
#   "name" text,
#   "fingerprint" text,
#   "subprotocol" text,
#   "protocol" text,
#   "port" integer,
#   "local_manufacturer" text,
#   "local_product" text,
#   "local_version" text,
#   "local_revision" text,
#   "local_description" text,
#   "global_manufacturer" text,
#   "global_product" text,
#   "global_version" text,
#   "global_revision" text,
#   "global_os" text,
#   "global_os_version" text,
#   "global_os_description" text,
#   "global_device_type" text,
#   "global_description" text,
#   "create_time" integer
# )'''


class Database:

    def __init__(self):
        self.conn = sqlite3.connect('fingerprint.db')
        self.cursor = self.conn.cursor()

    def query_rules(self, table_name):
        return self.cursor.execute("select * from "+table_name)


if __name__ == '__main__':
    conn = sqlite3.connect('fingerprint.db')
    cursor = conn.cursor()
    result = cursor.execute("select * from colasoft_ftp")
    column = ['local_manufacturer',
              'local_product',
              'local_version',
              'local_revision',
              'local_description',
              'global_manufacturer',
              'global_product',
              'global_version',
              'global_revision',
              'global_os',
              'global_os_version',
              'global_os_description',
              'global_device_type',
              'global_description']
    index = range(6, 20)

    try:
        rule_object = json.loads('{"regex": "121212121"}')
        if rule_object.keys().__contains__('regex'):
            print rule_object['regex']
    except ValueError:
        pass


def database():
    return database()
