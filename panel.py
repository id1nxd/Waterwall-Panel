import sqlite3
import datetime
import uuid
import os
import json
from datetime import date


def showuser():
    connection_obj = sqlite3.connect('WP.db') 
  
    cursor_obj = connection_obj.cursor() 
  
    statement = '''SELECT * FROM Users'''
  
    cursor_obj.execute(statement) 
  
    print("All the Users \n UserID \t UserRemark \t UserUUID \t UserStatus \t UserExp") 
    output = cursor_obj.fetchall() 
    for row in output: 
        print(row) 
  
    connection_obj.commit()
    connection_obj.close()
 

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



def addusertoconfig(username, uid):
    with open('config.json', 'r') as f:
        data = json.load(f)

    for node in data['nodes']:
        if node['type'] == 'TrojanAuthServer':
            # Add the new user to the users list
            node['settings']['users'].append({
                'name': username,
                'uid': uid,
                'enable': True
            })
            break

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)


def adduser():
    x = datetime.datetime.now()
    remark = input("Enter email/name/remark for user:")
    Exp = int(input("Enter Days:"))
    uuid1 = uuid.uuid4()

    day=Exp
    mon=0

    if(Exp>30):
        mon=int(Exp/30)
        day=Exp%30
    elif(Exp ==0):
        return 0

    
    txtExp=str(int(x.day)+day)+"-"+str(int(x.month)+mon)+"-"+str(x.year)

    addusertoconfig(remark,str(uuid1))

    connection_obj = sqlite3.connect('WP.db')
    txtsql="INSERT INTO Users (Useremail,UserUUID,UserExp,UserStatus) VALUES ('"+remark+"','"+str(uuid1)+"','"+str(txtExp)+"','true')"
    print(txtsql)
    connection_obj.execute(txtsql) 
    connection_obj.commit() 
    connection_obj.close()

    showuser()


def removeuser():
    id = int(input("Enter UserID to Delete:"))
    uid=""

    connection_obj = sqlite3.connect('WP.db') 
  
    cursor_obj = connection_obj.cursor() 
  
    statement = '''SELECT * FROM Users'''
  
    cursor_obj.execute(statement) 
  
    output = cursor_obj.fetchall() 
    for row in output: 
        if(str(row[0])==str(id)):
            uid=str(row[2])
  
    connection_obj.commit()
    connection_obj.close()

    change_user_status(uid,"false")

    connection_obj = sqlite3.connect('WP.db')
    txtsql="DELETE FROM Users WHERE UserID="+str(id)+" ;"
    connection_obj.execute(txtsql)
    connection_obj.commit() 
    connection_obj.close()
    connection_obj.close()


def renewuser():
    x = datetime.datetime.now()

    id = int(input("Enter UserID to ReNew:"))
    day=int(input("Enter Day to Exp:"))
    mon=int(input("Enter month to Exp:"))
    year=int(input("Enter year to Exp:"))

    uid=""

    connection_obj = sqlite3.connect('WP.db') 
  
    cursor_obj = connection_obj.cursor() 
  
    statement = '''SELECT * FROM Users'''
  
    cursor_obj.execute(statement) 


    output = cursor_obj.fetchall() 
    for row in output: 
        if(row[0]==id):
            uid=row[2]
      
    connection_obj.commit()
    connection_obj.close()

    change_user_status(uid,"true")


    if(day>32 or mon>12):
        return 0
    elif(day ==0 or mon==0):
        return 0
    
    
    connection_obj = sqlite3.connect('WP.db')
    txttmp=str(day)+"-"+str(mon)+"-"+str(year)

    txtsql="UPDATE Users SET UserExp='"+txttmp+"', UserStatus='true' WHERE UserID="+str(id)+";"
    connection_obj.execute(txtsql)
    connection_obj.commit() 
    connection_obj.close()
    connection_obj.close()


def importbackup():
    connection_obj = sqlite3.connect('WP.db') 
  
    cursor_obj = connection_obj.cursor() 
  
    statement = '''SELECT * FROM Users'''
  
    cursor_obj.execute(statement) 
  
    output = cursor_obj.fetchall() 
    for row in output: 
        remark = row[1]
        uuid1 = row[2]

        addusertoconfig(remark,str(uuid1))


  
    connection_obj.commit()
    connection_obj.close()

    showuser()


def main():
    while True:
        print("Welcome to WP Panel")
        print("1 - Show Users \n 2 - ADD Users \n 3 - Delete Users \n 4 - Renew Users \n 5 - Import BackUP \n 0 to Exit")
        worknum = int(input("Enter num:"))
        if(worknum == 1):
            showuser()    
        elif(worknum == 2):
            adduser()
        elif(worknum == 3):
            removeuser()
        elif(worknum == 4):
            renewuser()
        elif(worknum == 5):
            importbackup()
        elif(worknum == 0):
            return 0




main()