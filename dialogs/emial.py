


import smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("The body of the email is here")
msg["Subject"] = "An Email Alert"
msg["From"] = "botframe007@gmail.com"
msg["To"] = "botframe007@gmail.com"

context=ssl.create_default_context()

with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg["From"], "Yogesh@123")
    smtp.send_message(msg)



import smtplib

gmail_user = 'botframe007@gmail.com'
gmail_password = 'Yogesh@123'

sent_from = gmail_user
to = ['abhi05jan@gmail.com']
subject = 'MSG Subject'
body = 'Hey,Hows you'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    import pdb
    pdb.set_trace()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print 'Email sent!'
except:
    print 'Something went wrong...'