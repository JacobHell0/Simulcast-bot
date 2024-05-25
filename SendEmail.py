import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def sendEmail(address):  # takes an email address as a string and sends an email to it

    body = '''Attached is a pdf of the RTN schedule. If you find any errors or have suggestions, feel free to reply to this email
	
	
	'''
    # put your email here
    sender = os.environ['email']
    password = os.environ['pass']
    # put the email of the receiver here
    receiver = address
    # cc
    cc = os.environ['j_address']

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'RTN Schedule'

    message.attach(MIMEText(body, 'plain'))

    pdfname = 'RTN_Tracks.pdf'

    # open the file in bynary
    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    # payload = MIMEBase('application', 'pdf', Name=pdfname)
    payload.set_payload(binary_pdf.read())

    # encoding the binary into base64
    encoders.encode_base64(payload)

    # add header with pdf name
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)

    # use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)

    # enable security
    session.starttls()

    # login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, [receiver] + [cc], text)
    session.quit()
    print('Mail Sent')
