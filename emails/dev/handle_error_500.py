from emails.base import send_email


def handle_error_500(request, context):
    send_email.dev(
        subject=f"Erro 500 em {request.path}",
        template_path='emails/dev/error_500.html',
        context=context,
    )
