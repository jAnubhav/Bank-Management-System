from mysql.connector import connect
from time import ctime, sleep
from datetime import date
from random import randrange

#=================================== GLOBAL VARIABLES ==================================#

cred = ['Name', 'Age', 'Mobile No.', 'Profession', 'Salary', 'Balance', 'Account', 'Date Modified']
types = ['Regular', 'Savings', 'Current', 'Fixed Deposit']
options = ['Account Management', 'Leave/Exit']
acc_opt = ['Create', 'Search', 'Delete', 'Update', 'Display All', 'Delete All']

#==================================== BASE FUNCTIONS ===================================#

def get_data():
    try:
        cur.execute('select * from data')
        data = cur.fetchall()
        return data
    except:
        return []

def get_display():
    try:
        cur.execute('select * from display')
        data = cur.fetchall()
        return data
    except:
        return []

def daytime():
    hh = int(ctime()[11:13])
    if hh >= 0 and hh < 12:
        return "Good Morning"
    elif hh >= 12 and hh < 16:
        return "Good Afternoon"
    else:
        return "Good Evening"

def get_accno():
    try:
        cur.execute('select acc_no from data')
        data = cur.fetchall()
        return [i[0] for i in data]
    except:
        return []

def accno(query):
    while True:
        acc_nos = get_accno()
        a = randrange(100, 999)
        no = '10' + str(ord(query[0])) + str(a)
        if no not in acc_nos:
            return no 

def dis_format(ent):
    len_en = [len(str(ent[i])) for i in range(len(ent))]
    for i in range(len(len_en)):
        if i == 2:
            pass
        else:
            print('+', '-'*(len_en[i]+1), sep='', end='')
    print('+')
    for i in range(len(len_en)):
        if i == 2:
            pass
        else:
            print('|', str(ent[i]) + ' ', sep='', end='')
    print('|')
    for i in range(len(len_en)):
        if i == 2:
            pass
        else:
            print('+', '-'*(len_en[i]+1), sep='', end='')
    print('+')
    return


def amt():
    data,amount=get_display(),0
    for i in data:
        amount+=int(i[5])
    return str(amount)

#================================= WORKING FUNCTIONS ===================================#

def init():
    try:
        cur.execute('create database anubhav_jain')
    except:
        pass
    cur.execute('use anubhav_jain')
    try:
        cur.execute('create table data(acc_no char(7) primary key,name char(50),age int,mobile_no char(10),profession char(30),salary float,balance float,account char(15),date_modified date)')
        cur.execute('create table display(acc_no char(7) primary key,name char(50),mobile_no char(10),profession char(30),salary float,balance float,account char(15))')
    except:
        pass

def insert_rec():
    print('\n',f'{"MENU OF ACCOUNTS":^89s}')
    print(f"{'+----+--------------+':^89s}")
    for i in range(4):
        print(f"{'|':>35s}{i+1:<4d}{'|'}{types[i]:14s}{'|'}")
        print(f"{'+----+--------------+':^89s}")
    print()
    print("Press Enter to leave anytime\n")
    while True:
        ch = input("Enter your Choice : ")
        if len(ch) == 0:
            leave = input("\nAre you sure you want to leave (y/n)? ")
            if leave.lower()=='y':
                return
            else:
                print("\nOk. Continue.\n")
                sleep(0.6)
        elif ch in '1234' and len(ch) == 1:
            surety = input('\nYou want to create a ' + types[int(ch)-1] + ' Account (y/n)? ')
            if surety.lower()=='y':
                print("\nCreating a", types[int(ch)-1], "Account\n")
                acc_type = types[int(ch)-1]
                break
            else:
                print("\nOk. Try choosing the account again.\n")
                sleep(0.6)
        else:
            print("\nInvalid Choice. Try Again.\n")
            sleep(0.6)
    sleep(0.6)
    acc_no = accno(types[int(ch)-1])
    print("Provide the following credentials\n\nPress Enter to leave anytime")
    i, cred_list, dis_list = 0, [acc_no], [acc_no]
    while i <= 5:
        cred_in = input('\n' + cred[i] + ' : ')
        if len(cred_in) == 0:
            leave = input("\nAre you sure you want to leave (y/n)? ")
            if leave.lower() == 'y':
                return
            else:
                print("\nOk.Continue")
                sleep(0.6)
        else:
            if i == 1:
                if cred_in > '20' and cred_in < '85' and len(cred_in) == 2:
                    cred_list.append(int(cred_in))
                    i += 1
                else:
                    print("\nEnter a valid Age")
                    sleep(0.6)
            elif i == 2:
                try:
                    if len(cred_in) == 10:
                        ac = int(cred_in)
                        cred_list.append(cred_in)
                        dis_list.append(cred_in)
                        i += 1
                    else:
                        print("\nEnter a valid Mobile No.")
                        sleep(0.6)
                except:
                    print("\nEnter a valid Mobile No.")
                    sleep(0.6)
            elif i ==4 or i == 5:
                try:
                    cred_list.append(float(cred_in))
                    dis_list.append(float(cred_in))
                    i += 1
                except:
                    print("\nEnter a valid", cred[i])
                    sleep(0.6)
            else:
                try:
                    ac = int(cred_in)
                    print("\nEnter a valid", cred[i])
                    sleep(0.6)
                except:
                    cred_list.append(cred_in.title())
                    dis_list.append(cred_in.title())
                    i += 1
    cred_list.append(types[int(ch)-1]), cred_list.append(date.today())
    dis_list.append(types[int(ch)-1])
    print("\nOk. Bringing all data together. Wait for a while.\n")
    sleep(0.8)
    dis_format(cred_list)
    cur.execute('insert into data values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', cred_list)
    db.commit()
    cur.execute('insert into display values(%s, %s, %s, %s, %s, %s, %s)', dis_list)
    db.commit()
    print("\n\nSuccessfully registered\n")
    print(''' - Thank You for choosing us
 - Your money is safe in our bank
 - Read all the documentations carefully 
 - T&C applied\n\n''')
    add = input("Want to create more accounts(y/n)? : ")
    if add.lower() == 'y':
        print('\n')
        insert_rec()

def search_rec():
    st, acc_no, data = ['SNo.','Account No.s'], get_accno(), get_data()
    if len(acc_no)==0:
        print('\nNo records present. Try entering some records')
        sleep(0.6)
    else:
        print('\n+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        print('|' + st[0] + '|' + st[1] + '|')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        for i in range(len(acc_no)):
            print('|', i + 1, ' ' * (4 - len(str(i + 1))), sep='', end='')
            print('|', acc_no[i] , ' ' * (12 - len(acc_no[i])), '|', sep='')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        while True:
            print("\nPress Enter to leave anytime")
            no = input("\nPlease enter the SNo. of the account to be searched : ")
            try:
                if int(no) <= len(acc_no) and int(no) > 0:
                    break
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
            except:
                if len(no) == 0:
                    leave = input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower() == 'y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
        print('\n+', '-' * 34, '+', sep='-')
        for j in range(1, len(data[int(no)-1])):
            print('|', cred[j-1], ' ' * (13 - len(cred[j-1])), " : ", end='')
            print(data[int(no)-1][j], ' ' * (15-len(str(data[int(no)-1][j]))), '|')
        print('+', '-' * 34, '+', sep='-')
        sleep(0.8)
        add = input("\n\nWant to search more accounts(y/n)? : ")
        if add.lower() == 'y':
            search_rec()

def delete_rec():
    st, acc_no, cred_data = ['SNo.', 'Account No.s'], get_accno(), get_data()
    dis_data = get_display()
    if len(acc_no) == 0:
        print('\nNo records present. Try entering some records')
        sleep(0.6)
    else:
        print('\n+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        print('|' + st[0] + '|' + st[1] + '|')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        for i in range(len(acc_no)):
            print('|', i + 1, ' ' * (4 - len(str(i))), sep='', end='')
            print('|', acc_no[i], ' ' * (12 - len(acc_no[i])), '|', sep='')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        while True:
            print("\nPress Enter to leave anytime")
            no = input("\nPlease enter the SNo. of the account to be deleted : ")
            try:
                if int(no) <= len(acc_no) and int(no) > 0:
                    break
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
            except:
                if len(no) == 0:
                    leave = input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower() == 'y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
        for i in cred_data:
            if i[0] == acc_no[int(no)-1]:
                print()
                for j in range(1, len(i)):
                    if j == 2 or j == 3 or j == len(i) - 1:
                        pass
                    else:
                        print(cred[j-1], ' ' * (13 - len(cred[j-1])), " : ", i[j])
                break
        for k in dis_data:
            if k[0] == acc_no[int(no)-1]:
                break
        sure = input('\nAre you sure you want to delete this account(y/n)? : ')
        if sure.lower() == 'y':
            print('\nDeleting...')
            cur.execute('delete from data where acc_no=%s', (acc_no[int(no)-1],))
            db.commit()
            cur.execute('delete from display where acc_no=%s', (acc_no[int(no)-1],))
            db.commit()
            sleep(0.8)
            print("\nSuccessfully Deleted\n")
            print(" - All the amount deposited will be returned within 2 days\n")
            add = input("\n\nWant to delete more accounts(y/n)? : ")
            if add.lower() == 'y':
                delete_rec()
        else:
            print('\nOk. Not deleting the account. Exiting\n')
            return

def update_rec():
    st, acc_no, data = ['SNo.', 'Account No.s'], get_accno(), get_data()
    display = get_display()
    if len(acc_no) == 0:
        print('\nNo records present. Try entering some records')
        sleep(0.6)
    else:
        print('\n+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        print('|' + st[0] + '|' + st[1] + '|')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        for i in range(len(acc_no)):
            print('|', i + 1, ' ' * (4 - len(str(i))), sep='', end='')
            print('|', acc_no[i], ' ' * (12 - len(acc_no[i])), '|', sep='')
        print('+', '-' * len(st[0]), '+', '-' * len(st[1]), '+', sep='')
        while True:
            print("\nPress Enter to leave anytime")
            no = input("\nPlease enter the SNo. of the account to be updated : ")
            try:
                if int(no) <= len(acc_no) and int(no) > 0:
                    break
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
            except:
                if len(no) == 0:
                    leave = input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower() == 'y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
        print("\nProvide the new credentials.\nPress Enter to skip that credential.")
        i = 0
        while i <= 4:
            cred_in = input('\n' + cred[i] + ' : ')
            if len(cred_in) == 0:
                i+=1
                continue
            else:
                if i == 1:
                    if cred_in > '20' and cred_in < '75' and len(cred_in) == 2:
                        cur.execute('update data set age=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                        db.commit()
                        i += 1
                    else:
                        print("\nEnter a valid Age")
                        sleep(0.6)
                elif i == 2:
                    try:
                        if len(cred_in) == 10:
                            ac = int(cred_in)
                            cur.execute('update data set mobile_no=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                            cur.execute('update display set mobile_no=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                            
                            i += 1
                        else:
                            print("\nEnter a valid Mobile No.")
                            sleep(0.6)
                    except:
                        print("\nEnter a valid Mobile No.")
                        sleep(0.6)
                elif i == 4:
                    try:
                        ac = int(cred_in)
                        cur.execute('update data set salary=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                        db.commit()
                        cur.execute('update display set salary=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                        db.commit()
                        i += 1
                    except:
                        print("\nEnter a valid", cred[i])
                        sleep(0.6)
                else:
                    try:
                        ac = int(cred_in)
                        print("\nEnter a valid", cred[i])
                        sleep(0.6)
                    except:
                        if cred[i] == 'Name':
                            cur.execute('update data set name=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                            cur.execute('update display set name=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                        else:
                            cur.execute('update data set profession=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                            cur.execute('update display set profession=%s where acc_no=%s', (cred_in, acc_no[int(no)-1]))
                            db.commit()
                        i += 1
        cur.execute('update data set date_modified=%s where acc_no=%s', (date.today(), acc_no[int(no)-1]))
        db.commit()
        print('\nUpdating...')
        sleep(0.8)
        print('\nSuccessfully Updated\n')
        sleep(0.6)
        add=input("\n\nWant to update more accounts(y/n)? : ")
        if add.lower() == 'y':
            update_rec()

def read_all():
    display = get_display()
    if len(display) == 0:
        print('\nNo records Present. Try entering some records')
        sleep(0.6)
        return
    print('\n+', '-' * 87, '+', sep='')
    print('|', ' ' * 85, '|\n|', f"{'XYZ BANK OF INDIA,NOIDA':^85}", '|')
    print('|', f"{'ACCOUNT MANAGEMENT SYSTEM': ^85}", '|')
    print('|   ', ctime()[11:19], ' ' * 59, date.today(), '   |')
    print('|', ' ' * 85, '|')
    print('+' + '-' * 7, '-' * 16, '-' * 10, '-' * 13, '-' * 10, '-' * 11, '-' * 14, '', sep='+')
    print('|' + ' ' * 7, ' ' * 16, ' ' * 10, ' ' * 13, ' ' * 10, ' ' * 11, ' ' * 14, '', sep='|')
    print('|Acc No.|      Name', ' ' * 6, '|Mobile No.| Profession  |  Salary' ,sep='', end='')
    print('  |  Balance  | Account Type |')
    print('|' + ' ' * 7, ' ' * 16, ' ' * 10, ' ' * 13, ' ' * 10, ' ' * 11, ' ' * 14, '', sep='|')
    print('+' + '-' * 7, '-' * 16, '-' * 10, '-' * 13, '-' * 10, '-' * 11, '-' * 14, '', sep='+')
    for i in display:
        print(f"{'|'}{i[0]:7s}{'|'}{i[1]+' ':>16s}{'|'}{i[2]}{'|'}{i[3]:>13s}", end='')
        print(f"{'|'}{i[4]:>10.1f}{'|'}{i[5]:>11.1f}{'|'}{i[6]:>14s}{'|'}")
        print('+' + '-' * 7, '-' * 16, '-' * 10, '-' * 13, '-' * 10, '-' * 11, '-' * 14, '', sep='+')
    print('|', ' ' * 85, '|')
    print(f"{'|'}{'No. of accounts : ' + str(len(display)): ^44s}", end='')
    print(f"{'Total Bank Balance : ' + amt(): ^43s}{'|'}")
    print('|', ' ' * 85, '|')
    print('+', '-' *87, '+', sep='')
    print('\n')
    i=input("PRESS ENTER TO PROCEED")
    return

def with_money():
    st,acc_no,data,dis=['SNo.','Account No.s'],get_accno(),get_data(),get_display()
    if len(acc_no)==0:
        print('\nNo records present. Try entering some records')
        sleep(0.6)
        return
    else:
        print('\n+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        print('|'+st[0]+'|'+st[1]+'|')
        print('+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        for i in acc_no:
            print('|',acc_no.index(i)+1,' '*(4-len(str(acc_no.index(i)))),sep='',end='')
            print('|',i,' '*(12-len(i)),'|',sep='')
        print('+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        while True:
            print("\nPress Enter to leave anytime")
            no=input("\nPlease enter the SNo. of the account : ")
            try:
                if int(no)<=len(acc_no) and int(no)>0:
                    break
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
            except:
                if len(no)==0:
                    leave=input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower()=='y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
        for i in data:
            if i[0]==acc_no[int(no)-1]:
                print()
                for j in range(1,len(i)):
                    if j==2 or j==3 or j==len(i)-1:
                        pass
                    else:
                        print(cred[j-1],' '*(13-len(cred[j-1]))," : ",i[j])
                break
        for k in dis:
            if k[0]==acc_no[int(no)-1]:
                break    
        while True:
            mon=input('\nEnter the amount to be withdrawn : ')
            if len(no)==0:
                    leave=input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower()=='y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
            else:
                try:
                    ac=int(mon)
                    if i[len(i)-2]=='Current':
                        if int(mon)>=(int(i[len(i)-3])-1000):
                            print('\nInsufficient Balance in account.')
                            sleep(0.7)
                        else:
                            data[data.index(i)][len(i)-3]-=int(mon)
                            dis[dis.index(k)][len(k)-2]-=int(mon)
                            break
                    else:
                        if int(mon)>=(int(i[len(i)-3])):
                            print('\nInsufficient Balance in account.')
                            sleep(0.7)
                        else:
                            break
                except:
                    print('\nInvalid Entry.')
        print('\nWithdrawing...')
        cur.execute('update data set balance=balance-%s where acc_no=%s', (int(mon), acc_no[int(no)-1]))
        db.commit()
        cur.execute('update display set balance=balance-%s where acc_no=%s', (int(mon), acc_no[int(no)-1]))
        db.commit()
        sleep(0.8)
        print('\nSuccessfully Withdrawn\n')
        sleep(1)
        return

def depo_money():
    st,acc_no,data,dis=['SNo.','Account No.s'],get_accno(),get_data(),get_display()
    if len(acc_no)==0:
        print('\nNo records present. Try entering some records')
        sleep(0.6)
        return
    else:
        print('\n+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        print('|'+st[0]+'|'+st[1]+'|')
        print('+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        for i in acc_no:
            print('|',acc_no.index(i)+1,' '*(4-len(str(acc_no.index(i)))),sep='',end='')
            print('|',i,' '*(12-len(i)),'|',sep='')
        print('+','-'*len(st[0]),'+','-'*len(st[1]),'+',sep='')
        while True:
            print("\nPress Enter to leave anytime")
            no=input("\nPlease enter the SNo. of the account : ")
            try:
                if int(no)<=len(acc_no) and int(no)>0:
                    break
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
            except:
                if len(no)==0:
                    leave=input("\nAre you sure you want to leave (y/n)? ")
                    if leave.lower()=='y':
                        return
                    else:
                        print("\nOk.Continue")
                        sleep(0.6)
                else:
                    print("\nInvalid Sno. Try again.")
                    sleep(0.6)
        for i in data:
            if i[0]==acc_no[int(no)-1]:
                print()
                for j in range(1,len(i)):
                    if j==2 or j==3 or j==len(i)-1:
                        pass
                    else:
                        print(cred[j-1],' '*(13-len(cred[j-1]))," : ",i[j])
                break
        for k in dis:
            if k[0]==acc_no[int(no)-1]:
                break    
        while True:
            mon=input('\nEnter the amount to be deposited : ')
            if len(no)==0:
                leave=input("\nAre you sure you want to leave (y/n)? ")
                if leave.lower()=='y':
                    return
                else:
                    print("\nOk.Continue")
                    sleep(0.6)
            else:
                try:
                    ac=int(mon)
                    if i[len(i)-2]=='Fixed Deposit':
                        print('\nCannot Deposit money in FD.')
                        sleep(1)
                        return
                    else:
                        break
                except:
                    print('\nInvalid Entry.')
        print('\nDepositing...')
        cur.execute('update data set balance=balance+%s where acc_no=%s', (int(mon), acc_no[int(no)-1]))
        db.commit()
        cur.execute('update display set balance=balance+%s where acc_no=%s', (int(mon), acc_no[int(no)-1]))
        db.commit()
        sleep(0.9)
        print('\nSuccessfully Deposited\n')
        sleep(1)
        return

#==================================== MAIN FUNCTION ====================================#

def acc_manage():
    while True:
        print('\n',f"{'ACCOUNT MANAGEMENT':^89s}")
        print('\n',f"{'MENU OF OPTIONS':^89s}")
        print(f"{'+----+----------------------+':^89s}")
        for i in range(9):
            if i == 6:
                print(f"{'|':>31s}{i+1:<4d}{'|'}{'Withdraw Money':22s}{'|'}")
            elif i == 7:
                print(f"{'|':>31s}{i+1:<4d}{'|'}{'Deposit Money':22s}{'|'}")
            elif i == 8:
                print(f"{'|':>31s}{i+1:<4d}{'|'}{'Go Back':22s}{'|'}")
            else:
                print(f"{'|':>31s}{i+1:<4d}{'|'}{acc_opt[i]+' Accounts':22s}{'|'}") 
            print(f"{'+----+----------------------+':^89s}")
        ch = input("\nEnter your choice from the menu of options : ")
        sleep(0.6)
        if ch == '1':
            insert_rec()
        elif ch == '2':
            search_rec()
        elif ch == '3':
            delete_rec()
        elif ch == '4':
            update_rec()
        elif ch == '5':
            read_all()
        elif ch == '6':
            inp = input("\nAre you sure you want to delete all accounts(y/n)? : ")
            if inp.lower() == 'y':
                print('\nOk. Deleting...')
                sleep(0.8)
                cur.execute('drop database anubhav_jain')
                print('\nSuccessfully Deleted.')
                sleep(0.6)
            else:
                print('\nOk continue.')
                sleep(0.6)
        elif ch == '7':
            with_money()
        elif ch == '8':
            depo_money()
        elif ch == '9':
            print('\nReturning back to main menu.')
            sleep(0.6)
            return
        else:
            print('\nInvalid Choice. Try Again')
            sleep(0.6)

#==================================== MAIN PROGRAM =====================================#

if __name__ == "__main__":
    print('''\n\n'''f'{"Welcome":^89s}')
    passwd = input("\nEnter the password of the database : ")
    flag = 0
    try:
        db = connect(host='localhost', user='root', password=passwd)
        cur = db.cursor()
        init()
        flag = 1
    except:
        print("\nAccess Denied")
        sleep(1)
    while flag:
        print('\n\n', ' ' * 24,daytime() + '! All systems ready for use.\n')
        print(f'{"MENU OF OPTIONS":^89s}')
        print(f"{'+----+------------------+':^89s}")
        for i in range(2):
            print(f"{'|':>33s}{i+1:<4d}{'|'}{options[i]:18s}{'|'}")
            print(f"{'+----+------------------+':^89s}")
        ch = input("\n\nEnter your Choice : ")
        if ch == '2':
            sure = input('\nAre you sure you want to leave(y/n)? : ')
            if sure.lower() == 'y':
                print('\nExiting the system. Closing all files.')
                sleep(0.8)
                print('\nGood Bye')
                sleep(0.8)
                break
            else:
                print('\nOk Continue')
                sleep(0.6)
        elif ch == '1':
            sleep(0.6)
            acc_manage()
        else:
            print('\nEnter a valid option')
            sleep(0.6)
