from emails.base import send_email


def new_order(order):
    send_email.admin(
        subject=f'Novo pedido #{order.id} recebido',
        template_path='emails/admins/new_order.html',
        context={
            'order': order,
        },
    )
