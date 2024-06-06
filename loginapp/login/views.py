from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.db import models
import mysql.connector
from json import dumps
from django.contrib import messages
import datetime
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import json
from django.urls import resolve
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv

#dictionary to hold the meeting details
meeting = {}

#list containing the mentor schedule
mentor_meeting = []

#maintain the login status of a user


menteeans = []



#list containing the subjects of the eight semesters
subjects = [
    ["Courses","Course 1","Course 2","Course 3","Course 4","Course 5","Course 6","Course 7","Course 8"],
    ["Semester 1","Engineering Physics","Engineering Chemistry","Maths","Programming in Python","Engineering Graphics","Heritage of Tamils","Programming in Python(lab)","Physics and Chemistry Laboratory"],
    ["Semester 2","Programming and Data Structures","Complex function and Laplace Transforms","Basic Electrical and Electronic engineering","Heritage of Tamils","Physics for Information Science and Technology","Humanities","Software Development","Design thinking and Engineering Practices Lab"],
    ["Semester 3","Discrete Mathematics","Universal Human Values 2: Understanding Harmony","Programming and Design Patterns","DataBase Technology","Digital Logic and Computer Organization","Introduction to Digital Communication","Database Tecchnology Lab","Programming and Design Patterns Lab"],
    ["Semester 4","Probability and Statistics","Microprocessor and Microcotroller","Indian Constitution","Advanced Data Structures and Algorithm Analysis","Data communication and networks","Automata Theory and compiler design","Network Programming Lab","Digital Systems and Microprocessors lab"],
    ["Semester 5","Principles of Software Engineering and Practices","Data Analytics and Visualization","Principles of Operating Systems","Artificial Intelligence","Profession Elective 1","Management Elective","Software Development Project 2","Operating Systems Practices Lab"],
    ["Semester 6","Pattern Recognition and Machine Learning","Web Programming","Internet of Things and C Programming","Professional Elective 2","Open Elective 1","Mobile Application Development Lab"],
    ["Semester 7","Network and Communication Security","Cloud and Distributed Computing","Professional Elective 3","Professional Elective 4","Professional Elective 5","Project Work - Phase 1","Industrial Trainig / Internship"],
    ["Semester 8","Professional Elective 6","Open Elective 2","Project Phase 2"]
]

#defining a stack adt
class Stack:

    '''class representing a stack'''

    def __init__(self):
        self.items = []
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)
    
    def push(self,element):
        self.items.append(element)
    
    def isempty(self):
        return (self.items == [])
    
    def top(self):
        return self.items[-1]
    
    def pop(self):
        if self.isempty():
            return False
        self.items.pop()
        return True
    
    '''def __iter__(self):
        return iter(self._items)'''

class StackEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stack):
            return obj.items  # Serialize only the items in the stack
        return json.JSONEncoder.default(self, obj)
    


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "login"
)
mycursor = mydb.cursor()
if mydb.is_connected() == False:
    print("Connection not established")
else:
    print("Connection established")


# Create your views here.

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        mycursor.execute("SELECT * FROM login")
        result = mycursor.fetchall()
        for i in result:
            if email == i[2] and  password == i[3]:
                    name = i[1]
                    request.session["name"] = name
                    if i[4] == "Mentee":
                        name = i[1]
                        request.session['name'] = name
                        request.session["email"] = email

                        return redirect(mentee)
                        
                    elif i[4] == "Mentor":
                        mentorlogin = True
                        request.session["email"] = email
                        request.session["mentorlogin"] = mentorlogin
                        return redirect(mentor)
                    elif i[4] == "Manager":
                        managerlogin = True
                        request.session["manageremail"] = email
                        return redirect(manager)
                        
            else:
                continue
        else:
            return render(request,"403.html")
    return render(request,'login.html')

def mentor(request):
    mentorlogin = request.session["mentorlogin"]
    if mentorlogin == True:
            
        dict = {}
        mycursor.execute("Select * from personal order by Name asc")
        result = mycursor.fetchall()
        for j in result:
            dict[j[0]] = {"name":j[2],"dept":j[9]}
        #dict = {1:{"name":"Abinaya","dept":"CSE"},2:{"name":"arohi","dept":"civil"}}
        return render(request,"mentor.html",{"dict":dict,"mentor":mentor_meeting})
    else:
        return render(request,"403.html")

'''def manager(request):
    
    dict = {}
    mycursor.execute("select * from personal order by Name asc")
    result = mycursor.fetchall()
    print(result)
    for j in result:
        dict[j[0]] = {"name":j[2],"dept":j[9]}
    print(dict)
    return render(request,"manager.html",{"dict":dict})'''

def mentee(request):
        name = request.session["name"]
        mycursor.execute("SELECT * from personal")
        result1 = mycursor.fetchall()
        for j in result1:
            if name == j[2]:
                personal = {
                    "regno":j[1],
                    "name":j[2],
                    "mobile":j[3],
                    "email":j[4],
                    "add":j[5],
                    "g":j[6],
                    "bg":j[7],
                    "dob":j[8],
                    "dept":j[9]
                }
                mycursor.execute("SELECT * from father")
                result2 = mycursor.fetchall()
                for k in result2:
                    if name == k[1]:
                        father = {
                            "na":k[2],
                            "em":k[3],
                            "mob":k[4],
                            "qua":k[5],
                            "occ":k[6]
                        }
                mycursor.execute("SELECT * FROM mother")
                result3 = mycursor.fetchall()
                for a in result3:
                    if name == a[1]:
                        mother = {
                            "name" : a[2],
                            "email":a[3],
                            "mobile":a[4],
                            "qua":a[5],
                            "occ":a[6]
                        }
                mycursor.execute("SELECT * FROM academic")
                result4 = mycursor.fetchall()
                for b in result4:
                    if name == b[1]:
                        academic = {
                            "high_s" : b[2],
                            "sec_s" : b[3]
                    }
                print(mentor_meeting)

                return render(request,"mentee.html",{
                                        "personal":personal,
                                        "father":father,
                                        "mother":mother,
                                        "academic":academic,
                                        "mentor_meeting":mentor_meeting})
def add(request):
    result = False
    if request.method == "POST":
        #inserting details into the personal table
        Name = request.POST.get("name")
        Mobile = request.POST.get("mobile")
        Email = request.POST.get("email")
        Address = request.POST.get("add")
        Gender = request.POST.get('gender')
        Blood_Group = request.POST.get('bg')
        regno = request.POST.get("regno")
        DOB = request.POST.get("dob")
        Department = request.POST.get("dept")
        mycursor.execute("Select * from personal")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        print(S_No)
        query = "insert into personal values({},{},'{}',{},'{}','{}','{}','{}','{}','{}');".format(S_No,regno,Name,Mobile,Email,Address,Gender,Blood_Group,DOB,Department)
        mycursor.execute(query)
        print("Personal done")

        #inserting details into the father table
        Name = request.POST.get("name")
        fname = request.POST.get("fname")
        fmail = request.POST.get("fmail")
        fmob = request.POST.get("fmob")
        fqua = request.POST.get("fqua")
        focc = request.POST.get("focc")
        mycursor.execute("Select * from father")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into father values({},"{}","{}","{}",{},"{}","{}");'.format(S_No,Name,fname,fmail,fmob,fqua,focc)
        print("father done")
        mycursor.execute(query)

        #inserting details into the mother table
        Name = request.POST.get("name")
        mname = request.POST.get("mname")
        mmail = request.POST.get("mmail")
        mmob = request.POST.get("mmob")
        mqua = request.POST.get("mqua")
        mocc = request.POST.get("mocc")
        mycursor.execute("Select * from mother")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into mother values({},"{}","{}","{}",{},"{}","{}");'.format(S_No,Name,mname,mmail,mmob,mqua,mocc)
        print("mpther done")
        mycursor.execute(query)

        #inserting details into the academic table
        Name = request.POST.get("name")
        perc1 = request.POST.get("perc1")
        perc2 = request.POST.get("perc2")
        mycursor.execute("Select * from academic")
        result = mycursor.fetchall()
        S_No = len(result) + 1
        query = 'insert into academic values({},"{}",{},{});'.format(S_No,Name,perc1,perc2)
        mycursor.execute(query)

        result = True
        resultjs = dumps(result)
        request.session["resultjs"] = resultjs
        return redirect(success)

    resultjs = dumps(result)
    return render(request,"form.html",{"resultjs":resultjs})

def success(request):
    resultjs = request.session["resultjs"]
    return render(request,"form.html",{"resultjs":resultjs})

   
def delete(request):
    if request.method == "POST":
        student = request.POST.get("student")
        student = str.title(student)
        result = False
        mycursor.execute("Select * from login")
        result = mycursor.fetchall()
        for l in result:
            if l[1] == student:
                result = True
                mycursor.execute("Delete from personal where Name = '{}'".format(student))
                mycursor.execute("Delete from father where S_Name = '{}'".format(student))
                mycursor.execute("Delete from mother where S_Name = '{}'".format(student))
                mycursor.execute("Delete from academic where S_Name = '{}'".format(student))
                resultjs = dumps(result)
                return render(request,"mentor.html",{"resultjs":resultjs})
    resultjs = dumps(result)
    return render(request,"mentor.html",{"resultjs":resultjs})



def detail(request):
        if request.method == "POST":
            sname = request.POST.get("sname")
            request.session["sname"] = sname
            result = False
            deleted = True
        else:
            result = request.session["result"]
            deleted = request.session["deleted"]
        print(deleted)
        sname = request.session["sname"]
        mycursor.execute("SELECT * from personal")
        result1 = mycursor.fetchall()
        for j in result1:
            if sname == j[2]:
                personal = {
                    "regno":j[1],
                    "name":j[2],
                    "mobile":j[3],
                    "email":j[4],
                    "add":j[5],
                    "g":j[6],
                    "bg":j[7],
                    "dob":j[8],
                    "dept":j[9]
                }
                break
        mycursor.execute("SELECT * from father")
        result2 = mycursor.fetchall()
        for k in result2:
            if sname == k[1]:
                father = {
                    "na":k[2],
                    "em":k[3],
                    "mob":k[4],
                    "qua":k[5],
                    "occ":k[6]
                }
                break
        mycursor.execute("SELECT * FROM mother")
        result3 = mycursor.fetchall()
        for a in result3:
            if sname == a[1]:
                mother = {
                    "name" : a[2],
                    "email":a[3],
                    "mobile":a[4],
                    "qua":a[5],
                    "occ":a[6]
                }
                break
        mycursor.execute("SELECT * FROM academic")
        result4 = mycursor.fetchall()
        for b in result4:
            if sname == b[1]:
                academic = {
                    "high_s" : b[2],
                    "sec_s" : b[3]
                }
                break
        mycursor.execute("SELECT * FROM notes")
        result5 = mycursor.fetchall()
        note = ""
        note1 = None
        noteStack = Stack()
        temp = []
        if not noteStack:
            for y in result5:
                if sname == y[1]:
                    note = y[2]
                    for k in y[2].split(".")[:-1]:
                        k = k + "."
                        noteStack.push(k)
                        temp.append(k)
                    break
        note1 = temp
        serialized_stack = json.dumps(noteStack, cls=StackEncoder)
        request.session["noteStack"] = serialized_stack
        request.session["note"] = note
        request.session["sname"] = sname
        resultjs = dumps(result)
        deletedjs = dumps(deleted)
        print(meeting)
        print(mentor_meeting)
        data1 = None
        date = datetime.datetime.now()
        print(date)
        for y in meeting:
            if y == sname:
                if datetime.datetime.strptime(meeting[y]["Date"], '%Y-%m-%d') >= date:
                    data1 = meeting[y]
        return render(request,"detail.html",{
                            "personal":personal,
                            "father":father,
                            "mother":mother,
                            "academic":academic,
                            "note":note1,
                            "resultjs":resultjs,
                            "data1":data1,
                            "deletedjs":deletedjs})
    
'''personal = request.session["personal"]
    father = request.session["father"]
    mother = request.session["mother"]
    academic = request.session["academic"]
    return render(request,"detail.html",{
                                    "personal":personal,
                                    "father":father,
                                    "mother":mother,
                                    "academic":academic,
                                    "note":note})'''
  

def note(request):
    if request.method == "POST":
        date = str(datetime.datetime.now().date())
        print(date)
        notes = '[' + date + '] '
        notes += request.POST.get("notes")
        print(notes) 
        sname = request.session["sname"]
        note = request.session["note"]
        print(note)
        if note:
            notes =  note + notes
        mycursor.execute("SELECT * FROM notes")
        temp = mycursor.fetchall()
        for u in temp:
            if sname == u[1]:
                query = "update notes set Notes = '{}' where S_Name = '{}'".format(notes,sname)
                mycursor.execute(query)
                break
        else:
            S_No = len(temp) + 1
            query = "insert into notes values({},'{}','{}')".format(S_No,sname,notes)
            mycursor.execute(query)
        deleted = True
        result = False
        request.session["deleted"] = deleted
        request.session["result"] = result
        return redirect(detail)
    return redirect(detail)

def back(request):
    return redirect(mentor)

def schedule(request):
    result = True
    request.session["result"] = result
    sname = request.session["sname"]
    subject = request.POST.get("subject")
    date = request.POST.get("date")
    time = request.POST.get("time")
    if sname not in meeting:
        meeting[sname] = {"Subject":subject,"Date":date,"Time":time}
        mentor_meeting.append([sname,date,time])
    #messages.success(request, 'Successfully Sent The Message!')
    
    return redirect(detail)

'''def edit(request):
    result = False
    request.session["result"] = result
    print(father)
    return render(request,"edit.html",{
                            "personal":personal,
                            "father":father,
                            "mother":mother,
                            "academic":academic,})'''


def semester(request):
    
    #final_table = "<table>\n<tr>{}</tr>\n{}</table>".format('\n'.join('<th>{}</th>'.format(i) for i in subjects[0]), '<tr>{}</tr>'.format('\n'.join('\n'.join(['<td>{}</td>'.format(b) for b in i]) for i in subjects[1:])))
    #table  = tabulate(subjects, headers="firstrow", tablefmt="html")
    if request.method == "GET":
        name = request.GET.get("stuname")
        dept = request.GET.get("studept")
        request.session["name"] = name
        request.session["dept"] = dept
    else:
        name = request.session["name"]
        dept = request.session["dept"]
    return render(request,"marks.html",{
        "name":name,
        "dept":dept,
        "subject":subjects
    })
    
def check_reverse_exists(url_name):
    try:
        # Attempt to resolve the URL pattern
        resolver_match = resolve(reverse(url_name))
        # Check if the resolver match has a view function associated with it
        if resolver_match.func is not None:
            return True  # URL pattern exists
        else:
            return False  # URL pattern does not exist
    except Http404:
        return False


def deletelatest(request):
        serialized_stack = request.session["noteStack"]
        deserialized_stack = json.loads(serialized_stack)
        if  not deserialized_stack:
             deleted = False
        else:
            deserialized_stack.pop()
            string = ""
            for j in deserialized_stack:
                string = string + j
            sname = request.session["sname"]
            sql = "update notes set Notes = '{}' where S_Name = '{}' ".format(string,sname)
            mycursor.execute(sql)
            deleted = True
           
        request.session["deleted"] = deleted
        return redirect(detail)

def forgot(request):
    if request.method == "POST":
        email = request.POST.get("email")
        newpass = request.POST.get("newpass")
        mycursor.execute("SELECT * FROM login")
        result = mycursor.fetchall()
        for l in result:
            if l[2] == email:
                sql = "update login set Password = '{}' where Email = '{}'".format(newpass,email)
                mycursor.execute(sql)
                break
        print(newpass)
        return render(request,"home.html")
    return render(request,"forgot.html")

def manager(request):
    login = request.session["login"]
    if login == True:
        return render(request,"manager.html")


def enter(request):
    if request.method == "POST":
        semesterno = request.POST.get("semester")
        name = request.session["name"]
        dept = request.session["dept"]
        course1 = request.POST.get("1")
        course2 = request.POST.get("2")
        course3 = request.POST.get("3")
        course4 = request.POST.get("4")
        course5 = request.POST.get("5")
        course6 = request.POST.get("6")
        course7 = request.POST.get("7")
        course8 = request.POST.get("8")
        cgpa = request.POST.get("cgpa")
        semester = "Semester_"+semesterno
        mark = ",".join([cgpa,course1,course2,course3,course4,course5,course6,course7,course8])
        sql = "update Semester set {} = '{}' where Name = '{}'".format(semester,mark,name)
        mycursor.execute(sql)
        return render(request,"marks.html",{
        "name":name,
        "dept":dept,
        "subject":subjects
    })

def viewmarks(request):
    if request.method == "GET":
        semester = request.GET.get("values")
        name = request.session["name"]
        dept = request.session["dept"]
        final = []
        print(name)
        mycursor.execute("Select * from Semester where Name = '{}'".format(name))
        result = mycursor.fetchall()
        semester1 = int(semester)
        print(result)
        string = result[0][semester1]
        print(string)
        if string:
            print(string)
            listofsem = string.split(',')
            mark_dict = {}
            print(listofsem)
            temp =  subjects[semester1]
            mark_dict["CGPA"] = listofsem[0]
            try:
                index = listofsem.index("0")
            except:
                index = len(listofsem)
            for i in range(1,index):
                mark_dict[temp[i]] = listofsem[i]
            final.append(subjects[1])
            final.append(listofsem)
            print(final)

            print(result)
            print(mark_dict)
            return render(request,"marks.html",{
                "name":name,
                "dept":dept,
                "semester":semester,
                "result":mark_dict,
                "subject":subjects
            })
        elif string is None:
            return render(request,"404.html")
        else:
            return redirect(semester)

def postquestion(request):
    return render(request,"questions.html",{"range":range(1,11)})

def createquestion(request):
    if request.method == "POST":
        questionList = []
        for j in range(1,11):
            temp  = request.POST.get(str(j))
            if temp != "":
                questionList.append(temp)
        print(questionList)
        f = open("question.txt","w")
        for i in questionList:
            f.write(i+"\n")
        f.close()
    return render(request,"mentor.html")

def answer(request):
    result = False
    f = open("question.txt","r")
    s = f.read()
    f.close()
    temp = s.split("\n")
    temp = temp[:-1]
    if request.method == "POST":
        answerList = []
        name = request.session["name"]
        for k in range(1,len(temp)+1):
            temp1 = request.POST.get(str(k))
            answerList.append(temp1)
        f = open("answer.txt","a")
        f.write(name + "\n")
        for l in answerList:
            f.write(l)
        f.write("\n")
        f.close()
        result = True
    f = open("question.txt","r")
    s = f.read()
    f.close()
    temp = s.split("\n")
    temp = temp[:-1]
    number = [i for i in range(1,11)][:len(temp)]
    combined_list = zip(temp,number)
    resultjs = dumps(result)
    return render(request,"answer.html",{"list":combined_list,"resultjs":resultjs})

def viewans(request):
    return render(request,"viewans.html")

def ans(request):
    if request.method == "GET":
        name = request.GET.get("mentee")
        f = open("answer.txt","r")
        templist = f.read().split("\n")
        f.close()
        index = templist.index(name)
        result = ""
        try:
            string = templist[index + 1]
            result = string.split(".")[:-1]
        except:
            result = ""
        f = open("question.txt","r")
        temp = f.read().split("\n")[:-1]
        combined = zip(temp,result)
        print(result)
        
        return render(request,"viewans.html",{"resultlist":combined,"result":result})

        