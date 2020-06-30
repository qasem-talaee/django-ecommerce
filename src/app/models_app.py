from django.db import connection

def get_submenu_choice():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM app_category WHERE submenu_id = 0")
        row = cursor.fetchall()
        a = ()
        a = ('0', 'This is main category'),
        for i in range(len(row)):
            a += (str(row[i][0]), str(row[i][1])),
        return a