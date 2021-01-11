import json
import pymysql
from tqdm import trange
import traceback
import config

def write_into_db(words_path):
    with open(words_path) as f:
        words = f.read()
    words_list = json.loads(words)

    db = pymysql.connect(host=config.db_host, user=config.db_username, password=config.db_passwd, database=config.db_name, charset=config.db_charset)

    cursor = db.cursor()
    for i in trange(len(words_list)):
        try:
            word = words_list[i]
            cursor.execute('select id from ' + config.db_table + ' where words = %s limit 1', (word,))
            result = cursor.fetchone()
            try:
                if result is None:
                    cursor.execute('insert into ' + config.db_table + '(words) values (%s)', (word,))
                    db.commit()
            except Exception:
                print("写入失败")
                traceback.print_exc()
                db.rollback()
        except Exception:
            print("查询失败")
            traceback.print_exc()

    db.close()