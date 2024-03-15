import sqlite3
from flask import jsonify

USER_DATABASE = 'data/user database.db'

def get_user_permission(id=None, username=None, authorization=None):
    conn = sqlite3.connect(USER_DATABASE)
    cursor = conn.cursor()

    query = 'Select \"' + authorization + '\" FROM "User" WHERE id = ?'
    if id:
        cursor.execute(query, (id,))
    elif username:
        cursor.execute(query, (username,))
    else:
        return None

    user_permission = cursor.fetchone()
    conn.close()
    
    if user_permission is not None:
        # Convert the fetched value to boolean
        permission_value = bool(user_permission[0])
        return permission_value
    else:
        return False
    