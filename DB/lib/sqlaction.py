import pymysql

# from conf import dbpass, dbhost
#
#
# def defaultAction(where, userid):
#     conn = pymysql.connect(host=dbhost, user='root', password=dbpass, db='useraccess', characterset='utf8')
#     cur = conn.cursor()
#     query = 'select ' + where + ' from user where id=' + userid
#
#     if cur.execute(query) != 1:
#         return False
#     else:
#         if cur.fetchone()[0] == 1:
#             return True
#         else:
#             return False


class DBAction(object):
    """docstring for DBAction."""

    def __init__(self, host, port, id, pw, characterset='utf8', db='roomAccess'):
        super(DBAction, self).__init__()
        self.host = host
        self.port = port
        self.id = id
        self.pw = pw
        self.characterset = characterset
        self.db = db

        self.conn = pymysql.connect(
            host=self.host, user=self.id, password=self.pw, db=self.db, charset=self.characterset)
        self.cur = self.conn.cursor()

    def defaultAction(self, doorID, OpenClose, userid):
        query = 'select ' + doorID + ' from user where userId=' + userid

        if self.cur.execute(query) != 1:
            return False
        else:
            if self.cur.fetchone()[0] == 1:
                return True
            else:
                return False
