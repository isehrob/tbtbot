import datetime
import sqlite3

# bot database name
DB_NAME = "bot_db"

class DB():

    def __init__(self):
        self.db_name = DB_NAME
        self.conn = sqlite3.connect(self.db_name)

    def close():
        return self.conn.close()



class BotDB(DB):

    def create_table(self, table_name, attr):
        try:
            self.conn.execute(
                "create table %s (%s)" % (table_name, attr)
            )
        except sqlite3.OperationalError:
            return True
        return self.conn.commit()

    def alter_table(self, table_name, attr):
        pass

    def drop_table(self, table_name):
        self.conn.execute("drop table %s" % table_name)
        return self.conn.commit()


class Updates(DB):

    def select_one(self):
        c = self.conn.cursor()
        c.execute("select * from updates")
        return c.fetchone()

    def select(self):
        pass

    def update(self, updid, values):
        c = self.conn.cursor()
        c.execute(
            "update updates set %s where id=%d" % (values, updid))
        return self.conn.commit()

    def insert(self, values):
        c = self.conn.cursor()
        c.execute(
            "insert into updates(id, offset, date) values(%s)" % values)
        return self.conn.commit()


if __name__ == "__main__":

    # kind of unit test
    botdb = BotDB()
    upd = Updates()

    if botdb.create_table('example', "name text, date int"):
        print("Create table good")
    if botdb.drop_table("example"):
        print("Drop table good")

    if upd.insert("1234, %d" %
                  datetime.datetime.now().toordinal()):
        print("Update insert good")

