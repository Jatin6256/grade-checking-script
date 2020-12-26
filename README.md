# grade-checking-script

It is a simple script for IIITR students to reduce their effort to check grades again and again on result day.  As soon as student will get grades an email will be sent to students with grades in each course and calculated cgpa.

# Prerequisites

 1. requests module
 
 to install:
 
 ` $ pip install -r requirement.txt `

# How to run the script 

Make Some changes in calculator.py file:

1. <cookie_id> : Login to aims portal of IIIT Raichur and replace <cookie_id> with cookie stored in browser.
  eg -  <cookie_id> : 'abcd4327ghfsaaksj'
  
2 <sender_email> : student will get email from email id replaced with <sender_email>
  eg -  <sender_email> : 'xyz@gmail.com'
  
3 <password> : It will be replaced by app password generated for senders email in google account settings.
  eg - <password> : 'dgwoq4567asa'
  
4 <student_email> : Replace it with the email on which you want to recieve mail.
    eg - <student_email> : 'csxxb10xx@iiitr.ac.in' or student personal gmail account
    
  and finally run this command : 
    
` $ python calculator.py `

  and host it somewhere

` 
    
    

  
