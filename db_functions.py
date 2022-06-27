import pymysql
from pymysql.cursors import DictCursor

dbh = pymysql.connect (
    host        = '185.12.94.106',
    user        = '2p1s17',
    password    = '107-296-432',
    db          = '2p1s17',
    charset     = 'utf8mb4',
    cursorclass = DictCursor,
    autocommit  = True
)

def dbh_request(request):
    try:
        with dbh.cursor() as cur:
            cur.execute(request)
            rows = cur.fetchall()
            out_data = {
                'status': 'OK',
                'data': rows
            }
    except Exception as err:
        out_data = {
            'status': 'ERROR',
            'data': str(err)
        }
    return out_data