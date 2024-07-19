import sqlite3
import datetime
from datetime import date
import os
import json

def change_user_status(id, status):
    with open('config.json', 'r') as f:
        data = json.load(f)

    for node in data['nodes']:
        if node['type'] == 'TrojanAuthServer':
            # Find the user and update their enable status
            for user in node['settings']['users']:
                if user['uid'] == id:
                    if(status=="true"):
                        user['enable'] = True
                    else:
                        user['enable'] = False
                    break
            break

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)

def disableuser(id):
    
    connection_obj = sqlite3.connect('WP.db')

    txtsql="UPDATE Users SET UserStatus='false' WHERE UserID="+str(id)+";"
    connection_obj.execute(txtsql)
    connection_obj.commit() 
    connection_obj.close()
    connection_obj.close()



def main():
    connection_obj = sqlite3.connect('WP.db') 
  
    cursor_obj = connection_obj.cursor() 
  
    statement = '''SELECT * FROM Users'''
  
    cursor_obj.execute(statement) 
  
    output = cursor_obj.fetchall() 
    for row in output: 
        x = datetime.datetime.now()
        y=x.year
        m=x.month
        d=x.day

        exp=str(row[4])

        tmp=exp.split('-')

        d1 = date(y, m, d)
        d2 = date(tmp[2], tmp[1], tmp[0])

        leftdays=abs((d2 - d1).days)

        if(str(row[3])=="true"):
            if(leftdays<0):
                change_user_status(row[2],"false")
                disableuser(row[0])


             
 
  
    connection_obj.commit()
    connection_obj.close()
