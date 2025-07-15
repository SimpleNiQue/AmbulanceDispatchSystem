from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email_task(
    subject, recipient_email, template_name, context: dict, attachements
):
    html_message = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=html_message,
        to=[recipient_email],
        from_email=context["from_email"],
        attachments=attachements,
    )
    email.content_subtype = "html"
    email.send()
