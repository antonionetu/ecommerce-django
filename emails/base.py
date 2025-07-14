import os
from dotenv import load_dotenv

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


load_dotenv()


class SendEmail:
    @staticmethod
    def customer(subject, customer_email, template_path, context):
        html_content = render_to_string(template_path, context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=os.getenv("USER_EMAIL"),
            to=[customer_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    @staticmethod
    def admin(subject, template_path, context):
        html_content = render_to_string(template_path, context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=os.getenv("USER_EMAIL"),
            to=[os.getenv("USER_EMAIL"), "devantonio.fer@gmail.com"]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    @staticmethod
    def dev(subject, template_path, context):
        html_content = render_to_string(template_path, context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=os.getenv("USER_EMAIL"),
            to=["devantonio.fer@gmail.com"]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


send_email = SendEmail()
