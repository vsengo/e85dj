import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#aws asia south
SMTP_Username="AKIAXZ2CH3LHQ5VURBSM"
SMTP_Password="BF3xXN/G68pblWwAcUbNm4WtsVwIUTWxxd3D5bFwe9h6"

sender_email = "sengo@idaikkadu.com"
receiver_email = "vsengo@gmail.com"
password = input("xt&K{&nE!YC#7TF")
smtp="email-smtp.us-east-1.amazonaws.com"
message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp, 465, context=context) as server:
    server.login(sender_email, password)
    print("Logged in to smtp")
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
    print("Sent mail "+sender_email)