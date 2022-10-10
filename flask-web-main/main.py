import smtplib, random
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect,url_for,render_template,session, request
from datetime import datetime
from DataBaseTable import *
from settings import app,db

@app.route("/Student_Hub", methods = ['POST','GET'])
def test():
    if request.method == 'POST':
        try:
            if request.form['L_Email']:
                login_email = request.form['L_Email']
                login_password = request.form['L_Pword']
            
                session_username = UserInfo.query.filter_by(username=login_email).first()
                session_password = UserInfo.query.filter_by(password=login_password).first()
                
                if session_username and session_password:
                    return redirect(url_for('user'))
        except:
            if request.form['R_Email']:
                user_email = request.form['R_Email']
                password = request.form['Pword']
                password_auth = request.form['ConfirmPword']
                if not UserInfo.query.filter_by(username=user_email).first():
                
                    if password == password_auth:
                        return redirect(url_for('send_mail', user_email = user_email, password = password))
                else: 
                    return redirect(url_for("test"))

    return render_template("base.html")

@app.route("/user")
def user():
    return f'welcome madapaker'

@app.route("/OTP/<gen_otp>/<key>/<user_email>/<password>",methods = ['POST','GET'])
def OTP(gen_otp,key,user_email,password):
    if request.method == 'POST':
        request_otp = request.form['Generated_OTP']
        fernet = Fernet(key)
        decrypt_otp = fernet.decrypt(gen_otp).decode()

        if str(request_otp) == decrypt_otp:
            Add_User = UserInfo(user_email,password)
            db.session.add(Add_User)
            db.session.commit()

            return redirect(url_for('test'))
        else:
            print('robot') 

    return render_template('OneTimePin.HTML')

@app.route("/mail/<user_email>/<password>")
def send_mail(user_email,password):
    generated_otp = ''
    for i in range(4):
        generated_otp += str(random.randint(0,9))

    key = Fernet.generate_key()
    fernet = Fernet(key)

    encrypt_otp = fernet.encrypt(generated_otp.encode())


    mail_content = f'your pin is {generated_otp}'
    #The mail addresses and password
    sender_address = 'roxas.emerson10dummy@gmail.com'
    sender_pass = 'lnoqdrmszgwibmyz'
    receiver_address = user_email
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Ako to si natoy, na mahal na mahal ka.'   #The subject line
    
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

    return redirect(url_for("OTP", gen_otp = encrypt_otp, key=key, user_email = user_email, password = password))

if __name__ == "__main__":
    app.run(debug=True)