from sendgrid.helpers.mail import Email, Content, Mail

from . import sg

######## EMAIL METHODS ########
def send_email(to, subject, content):
    from_email = Email("olin-api@example.com")
    to_email = Email(to)
    body = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, body)
    response = sg.client.mail.send.post(request_body=mail.get())
