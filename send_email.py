import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sched
import time
import datetime
import random
import threading
import pytz

scheduler = sched.scheduler(time.time, time.sleep)

def send_email_at_time(send_time, recipient, recipient_email, company_name, business_type, business_type_2, resume_file, additional_file):
    sender_email = "ik254@cornell.edu"  # Replace with your Gmail address
    sender_password = "xwrr tiif egzo skes"  # Replace with your password or App Password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = f"Ivan Kwong <{sender_email}>"
    message['To'] = recipient_email
    message['Subject'] = f"Interest in Student {business_type_2}{' ' if business_type_2 else ''}Summer Opportunities at {company_name or recipient} | Ivan Kwong"

    body = (f"Dear {recipient},\n\n"
            f"I am Ivan Kwong, and I am a junior undergraduate student studying Finance at Cornell University. I am interested in {business_type} experiences at {company_name or recipient}, in order to apply my previous investment management internship experience and further develop real-world experiences at a boutique firm. I'm wondering if you had any opportunities for students for Summer 2024?\n\n"
            f"If you are interested, I am more than happy to chat with you about this further, and you can call me at (607) 375-7081 or feel free to message me via email at ik254@cornell.edu. I have also attached a reference letter for your convenience.\n\n"
            f"Thank you so much for your time and consideration, and I look forward to hearing back from you shortly\n\n"
            f"Best regards,\n"
            f"Ivan Kwong\n"
            f"--")

    signature_html = """
    <br>
    <strong style="color: #000000;">Ivan Kwong</strong> <em style="color: #000000;">Applied Economics and Management Student</em><br>
    <span style="color: #000000;">Cornell University | Charles H. Dyson School of Applied Economics and Management</span><br>
    <span style="color: #CC0000;">p:</span> <span style="color: black;">(607) 375-7081<br></span>
    <span style="color: #CC0000;">e:</span> <a href="mailto:ik254@cornell.edu" style="color: #0000EE;">ik254@cornell.edu</a>
    """

    message.attach(MIMEText(body, 'plain'))
    message.attach(MIMEText(signature_html, 'html'))

    def attach_file(file_path):
        filename = file_path.split("/")[-1]
        attachment = open(file_path, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {filename}")
        message.attach(p)
        attachment.close()

    attach_file(resume_file)
    attach_file(additional_file)

    session = smtplib.SMTP(smtp_server, smtp_port)
    session.starttls()
    session.login(sender_email, sender_password)
    text = message.as_string()
    session.sendmail(sender_email, recipient_email, text)
    session.quit()

def schedule_email(recipient, recipient_email, company_name, business_type, business_type_2, resume_file, additional_file):
    eastern = pytz.timezone('US/Eastern')
    current_time_eastern = datetime.datetime.now(eastern)
    if 0 <= current_time_eastern.hour < 9:
        schedule_date_eastern = current_time_eastern.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        schedule_date_eastern = (current_time_eastern + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

    send_time_eastern = schedule_date_eastern + datetime.timedelta(seconds=random.randint(0, 3600))

    local_timezone = pytz.timezone('America/Los_Angeles')
    send_time_local = send_time_eastern.astimezone(local_timezone)

    current_time_local = datetime.datetime.now(local_timezone)
    delay_seconds = (send_time_local - current_time_local).total_seconds()

    scheduler.enter(delay_seconds, 1, send_email_at_time, (send_time_eastern, recipient, recipient_email, company_name, business_type, business_type_2, resume_file, additional_file))
    print(f"Email to {recipient} scheduled for {send_time_eastern} Eastern Time.")


roles = {
    "1": "Investment Banking",
    "2": "Private Equity",
    "3": "Venture Capital",
    "4": "Venture Capital and Private Equity",
    "5": "Investment Management",
    "6": "Equity Research",
    "7": "Wealth Management",
    "8": "Investment",
    "9": "Other",
}

def run_scheduler():
    try:
        while True:
            scheduler.run(blocking=False)
            time.sleep(1)
    except Exception as e:
        print(f"Scheduler error: {e}")

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

try:
    while True:
        recipient = input("Enter the recipient's name: ")
        if recipient == 'cancel':
            continue
        recipient_email = input("Enter the recipient's email: ")
        if recipient_email == 'cancel':
            continue
        company_name = input("Enter the companies name: ")
        if company_name == 'cancel':
            continue
        business_type = input("Select the business type:\n1: Investment Banking\n2: Private Equity\n3: Venture Capital\n4: Venture Capital and Private Equity\n5: Investment Management\n6: Equity Research\n7: Wealth Management\n8: Investment\n9: Other\n")
        if business_type == 'cancel':
            continue
        if business_type != 9:
            business_type = roles[business_type]
        else:
            business_type = input("Enter the business type: ")
        business_type_2 = input("Enter the second business type if applicable: ")
        if business_type_2 == 'cancel':
            continue
        resume_file = "Ivan_Kwong_Resume.pdf"  # Replace with the path to your resume file (assumes this file is in the same folder)
        additional_file = "Ivan_Kwong_Reference.pdf"  # Replace with the path to your additional file (assumes this file is in the same folder)


        schedule_email(recipient, recipient_email, company_name, business_type, business_type_2, resume_file, additional_file)

except KeyboardInterrupt:
    print("Email scheduling stopped.")