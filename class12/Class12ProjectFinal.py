# This program has been developed by Aritra Sur of Class 12-J, DPSRPK, for the Board-Practical of AISSCE 2022-23.

import os
import platform
import mysql.connector
constr=mysql.connector.connect(host="localhost",
user="root",
passwd="",
database="aldb")
print(constr)
mycursor=constr.cursor()
def RegisterAlumni():
    L=[]
    fname=input("Enter Your First Name : ")
    L.append(fname)
    lname=input("Enter Your Last Name :")
    L.append(lname)
    dob=input("Enter Dob in YYYY-MM-DD Format : ")
    L.append(dob)
    gender=input("Enter Your Gender : ")
    L.append(gender)
    add_c=input("Enter your correspondence address : ")
    L.append(add_c)
    add_of=input("Enter your official address : ")
    L.append(add_of)
    email=input("Enter your email address Ex: aa@gmail.com: ")
    L.append(email)
    mob=input("Enter Your Mobile No: ")
    L.append(mob)
    cur_c=input("Enter City Name You Stay : ")
    L.append(cur_c)
    com=input("Enter Company/Organization You are Working : ")
    L.append(com)
    desg=input("Enter Your Desgination in Company/Organization : ")
    L.append(desg)
    start_y=input("Enter Your Session Start Year in College: ")
    L.append(start_y)
    start_e=input("Enter Your Session End Year in College : ")
    L.append(start_e)
    branch=input("Enter Your Branch in College : ")
    L.append(branch)
    alid="al"+fname[0:2]+lname[0:2]+mob[0:4]
    L.insert(0,alid)
    alumni=(L)
sql="insert into alureg"
(alu_id,first_name,last_name,dob,gender,add_corr,add_offc,email_add,mob_no,curr_city,curr_company,desg,session_from,session_to,branch) values
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
mycursor.execute(sql,alumni)
constr.commit()
print("You Have Been Succesfully Registered: This is You AlumniID ,Use This ForFurther Correspondence")
print(alid)
def ViewAlumniDetails():
 print("Select the search criteria to View Details : ")
print("1. Fname")
print("2. Lname")
print("3. Company")
print("4. Stream")
print("5. City")
print("6. Session Start")
print("7. To View All Records")
ch=int(input("Enter the choice : "))
if ch==1 :
 s=input("Enter First Name to Be Searched For")
 rl=(s,)
 sql="select * from alureg where first_name like %s"
 mycursor.execute(sql,rl)
elif ch==2:
 s=input("Enter Last Name to Be Searched For")
 rl=(s,)
 sql="select * from alureg where last_name like %s"
 mycursor.execute(sql,rl)
elif ch==3:
 s=input("Enter Company Name to Be Searched For")
 rl=(s,)
 sql="select * from alureg where curr_company=%s"
 mycursor.execute(sql,rl)
elif ch==4:
 s=input("Enter Stream : ")
 rl=(s,)
 sql="select * from alureg where branch=%s"
 mycursor.execute(sql,rl)
elif ch==5:
 s=input("Enter City : ")
 rl=(s,)
 sql="select * from alureg where curr_city=%s"
 mycursor.execute(sql,rl)
elif ch==6:
 s=input("Enter Session Start Year ")
 rl=(s,)
 sql="select * from alureg where session_from=%s"
 mycursor.execute(sql,rl)
elif ch==7:
 sql="select * from alureg"
 mycursor.execute(sql)
res=mycursor.fetchall()
print("The Alumni Details are as Follows")
print("(alu_id,first_name,last_name,dob,gender,add_corr,add_offc,email_add,mob_no,curr_city,curr_company,desg,session_from,session_to,branch)")
for x in res:
 print(x)

def EditAlumni():
 alid=input("Enter Alumni ID to be edited : ")
sql="select * from alureg where alu_id=%s"
ed=(alid,)
mycursor.execute(sql,ed)
res=mycursor.fetchall()
for x in res:
 print(x)
print("")
fld=input("Enter the field which you want to edit : ")
val=input("Enter the value you want to set : ")
sql="Update alureg set " + fld +"='" + val + "' where alu_id='" + alid + "'"
sq=sql
mycursor.execute(sql)
print("Editing Done : ")
print("After correction the record is : ")
sql="select * from alureg where alu_id=%s"
ed=(alid,)
mycursor.execute(sql,ed)
res=mycursor.fetchall()
for x in res:
 print(x)
constr.commit()
def SearchAlumni():
 print("Enter The Alumni ID")
aluid=input("Enter the Alumni ID for the alumni to be viewed : ")
sql="select * from alureg where alu_id=%s"
rl=(aluid,)
mycursor.execute(sql,rl)
res=mycursor.fetchall()
if res==None:
 print("Record not Found . . . ")
 return
print("The details of the students are : " )
print("(alu_id,first_name,last_name,dob,gender,add_corr,add_offc,email_add,mob_no,curr_city,curr_company,desg,session_from,session_to,branch)")
for x in res:
 print(x)
def DeleteAlumni():
 aluid=input("Enter the Alumni ID for the alumni to be deleted : ")
sql="Delete from alureg where alu_id=%s"
rl=(aluid,)
mycursor.execute(sql,rl)
constr.commit()
def ScheduleEvent():
 E=[]
 ename=input("Enter Event Name to Schedule : ")
 E.append(ename)
 edate=input("Enter Event Date in YYYY-MM-DD :")
 E.append(edate)
 evenue=input("Enter Venue of Event :")
 E.append(evenue)
 estat=input("Enter Event Status as Completed Or Not Completed :")
 E.append(estat)
 event=(E)
 sql="insert into event (event_name,event_date,venue,status) values (%s,%s,%s,%s)"
 mycursor.execute(sql,event)
 constr.commit()
 print("You Have Succesfully Added A Event")
def ViewEventDetails():
  print("Select the search criteria to View Event Details : ")
  print("1. Event Name")
  print("2. Venue")
  print("3. Status")
  print("4. To View All Records")
ch=int(input("Enter the choice : "))
if ch==1 :
 s=input("Enter Event Name to Be Searched For")
 rl=(s,)
 sql="select * from event where event_name like %s"
 mycursor.execute(sql,rl)
elif ch==2:
 s=input("Enter Venue Name to Be Searched For")
 rl=(s,)
 sql="select * from event where event like %s"
 mycursor.execute(sql,rl)
elif ch==3:
 s=input("Enter Status to Be Searched For")
 rl=(s,)
 sql="select * from event where status=%s"
 mycursor.execute(sql,rl)
elif ch==4:
 sql="select * from event"
 mycursor.execute(sql)
res=mycursor.fetchall()
print("The Event Details are as Follows")
print("(Event_Name,Event_Date,Venue,Status)")
for x in res:
 print(x)

def DeleteEvent():
 ename=input("Enter the Event Name to be deleted : ")
 sql="Delete from event where event_name=%s"
 rl=(ename,)
 mycursor.execute(sql,rl)
 constr.commit()

def MainMenu():
 print("Enter 1 : To Register Alumni")
print("Enter 2 : To View Alumni Details ")
print("Enter 3 : To Edit Alumni Details ")
print("Enter 4 : To Search Alumni ")
print("Enter 5 : To delete Alumni")
print("Enter 6 : To Add a Event")
print("Enter 7 : To Search a Event")
print("Enter 8 : To Delete a Event")
try:
 userInput = int(input("Please Select An Above Option: "))
except ValueError:
 exit("You Had Enetered Wrong Choice")
else:
 print("\n")
 if(userInput == 1):
  RegisterAlumni()
 elif (userInput==2):
  ViewAlumniDetails()
 elif (userInput==3):
  EditAlumni()
 elif (userInput==4):
  SearchAlumni()
 elif (userInput==5):
  DeleteAlumni()
 elif(userInput==6):
  ScheduleEvent()
 elif(userInput==7):
  ViewEventDetails()
 elif(userInput==8):
  DeleteEvent()
 else:
  print("Enter correct choice. . . ")

MainMenu()
def AskChoiceAgain():
 AksChcRun = input("\nwant To Run Again Y/n: ")
while(AksChcRun.lower() == 'y'):
 if(platform.system() == "Windows"):
  print(os.system('cls'))
 else:
  print(os.system('clear'))
 MainMenu()
 AksChcRun = input("\nwant To Run Again Y/n: ")
AskChoiceAgain()