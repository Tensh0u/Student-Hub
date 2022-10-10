import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect,url_for,render_template,session, request
from datetime import datetime
from settings import app

@app.route("/Student_Hub")
def test():
    return render_template("base.html")

@app.route("/send_mail")
def send_mail():
    mail_content = 'hellos this is a sample mail'
    #The mail addresses and password
    sender_address = 'sender123@gmail.com'
    sender_pass = 'xxxxxxxx' # app password configure in gmail
    receiver_address = 'receiver567@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

     return redirect(url_for("test"))

if __name__ == "__main__":
    app.run(debug=True)
