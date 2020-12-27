import requests
import json
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage

msg = EmailMessage()




url = 'https://aims.iiitr.ac.in/iiitraichur/courseReg/loadMyCoursesHistroy?studentId=3&courseCd=&courseName=&orderBy=1&degreeIds=&acadPeriodIds=&regTypeIds=&gradeIds=&resultIds=&isGradeIds='
cookie = {'JSESSIONID' : <cookie_id>}
#time interval = 600 secs 
Time_Interval = 600
acadPeriodId = <acad_period_id>
sender_email = <sender_email>
password = <password>
send_to = <student_email>







def getPoints(grade):
    if grade == 'A+':
        return 10
    elif grade == 'A':
        return 10
    elif grade == 'A-':
        return 9
    elif grade == 'B':
        return 8
    elif grade == 'B-':
        return 7
    elif grade == 'C':
        return 6
    elif grade == 'C-':
        return 5
    elif grade == 'D':
        return 4
    else:
        return 0

    

prevCount = 0
def getCgpa(cookie,acadPeriodId):
    r = requests.get(url, cookies=cookie)
    r = json.loads(r.content)
    points = 0
    totalCredits = 0
    grades = {}
    grades['name'] = []
    grades['grade'] = []
    totalCourses = 0
    currCount = 0
    for course in r:
            if course['acadPeriodId'] == acadPeriodId:
                if course['gradeDesc'] != "" :
                    currCount += 1
                    temp = (float(course['credits']) * getPoints(course['gradeDesc']))
                    points += temp 
                    totalCredits += float(course['credits'])
                    grades['grade'].append(course['gradeDesc'])
                    grades['name'].append(course['courseName'])
                totalCourses += 1 


    global prevCount
    if totalCourses == currCount :
        grades['sendEmail'] = True
        grades['cgpa'] = points/totalCredits
        grades['isFinal'] = True
    elif currCount > prevCount :
        prevCount = currCount
        grades['cgpa'] = 0
        grades['sendEmail'] = True
        grades['isFinal'] = False
    else:
        grades['cgpa'] = 0
        grades['sendEmail'] = False
        grades['isFinal'] = False
        
    return grades

def sendEmail():
    dict = getCgpa(cookie,acadPeriodId)
    if(dict['sendEmail'] == False):
        time.sleep(Time_Interval)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('[' + dt_string + ']: '+'Trying again')
        sendEmail()
    elif dict['isFinal'] == True:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

                smtp.login('sweprojectams@gmail.com', 'kvwnqvmrbftbhxiy')

                msg["subject"] = "Semester Grades Uploaded"
                msg["To"] = 'cs19b1013@iiitr.ac.in'
                msg["From"] = "AIMS Script <aims_script@testerworld.com>"

                gradeList = ''
                for i in range(len(dict['name'])):
                    gradeList += dict['name'][i] + ': ' + dict['grade'][i] + '\n'

                msg.set_content("Your CGPA for the semester is " + str(dict['cgpa']) + ". Your break down of grades is:  \n\n" + gradeList )

                smtp.send_message(msg)
                print("Successfully sent email.")
        except SMTPException:
            print("Error: unable to send email")
    else:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

                smtp.login(sender_email, password)

                msg["subject"] = "Semester Grades Uploaded"
                msg["To"] = send_to
                msg["From"] = "AIMS Script <aims_script@testerworld.com>"

                gradeList = ''
                for i in range(len(dict['name'])):
                    gradeList += dict['name'][i] + ': ' + dict['grade'][i] + '\n'

                msg.set_content("Your CGPA for the semester is not calculated yet. Your break down of grades is:  \n\n" + gradeList )

                smtp.send_message(msg)
                print("Successfully sent email.")
        except SMTPException:
            print("Error: unable to send email")
    
    time.sleep(Time_Interval)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('[' + dt_string + ']: '+'Trying again')
    sendEmail()



sendEmail()



