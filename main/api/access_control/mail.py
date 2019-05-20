from flask_mail import Mail, Message
from main.app import app


mail = Mail(app)

def send_mail(code, recipient):
	message = Message('Verify your email with this one time code' ,
		sender='ronniwallace2017@gmail.com', recipients=[recipient])
	message.body = code
	mail.send(message)
