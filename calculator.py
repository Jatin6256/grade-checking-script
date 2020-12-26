import requests
import json
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage

msg = EmailMessage()




url = 'https://aims.iiitr.ac.in/iiitraichur/courseReg/loadMyCoursesHistroy?studentId=3&courseCd=&courseName=&orderBy=1&degreeIds=&acadPeriodIds=&regTypeIds=&gradeIds=&resultIds=&isGradeIds='
cookie = {'JSESSIONID' : <cookie_id>}







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

    


def getCgpa():
    r = requests.get(url, cookies=cookie)
    r = json.loads(r.content)
    points = 0
    totalCredits = 0
    grades = {}
    grades['name'] = []
    grades['grade'] = []
    for course in r:
            if course['acadPeriodId'] == <acad_period_id>:
                if course['gradeDesc'] == "" :
                    grades['res'] = False
                    grades['cgpa'] = 0
                    return grades
                else:
                    temp = (float(course['credits']) * getPoints(course['gradeDesc']))
                    points += temp 
                    totalCredits += float(course['credits'])
                    grades['grade'].append(course['gradeDesc'])
                    grades['name'].append(course['courseName'])

   
    if totalCredits != 0:
        grades['res'] = True
        grades['cgpa'] = points/totalCredits
    else:
        grades['cgpa'] = 0
        grades['res'] = False
    return grades

def sendEmail():
    dict = getCgpa()
    if(dict['res'] == False):
        time.sleep(600)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('[' + dt_string + ']: '+'Trying again')
        sendEmail()
    else:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

                smtp.login(<sender_email>, <password>)

                msg["subject"] = "Semester Grades Uploaded"
                msg["To"] = <student_email>
                msg["From"] = "AIMS Script <aims_script@testerworld.com>"

                gradeList = ''
                for i in range(len(dict['name'])):
                    gradeList += dict['name'][i] + ': ' + dict['grade'][i] + '\n'

                print(gradeList)
                msg.set_content("Your CGPA for the semester is " + str(dict['cgpa']) + ". Your break down of grades is:  \n\n" + gradeList )

                smtp.send_message(msg)
                print("Successfully sent email.")
        except SMTPException:
            print("Error: unable to send email")



sendEmail()



