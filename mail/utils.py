from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from core.config import get_mail_config


config = get_mail_config()


conn_config = ConnectionConfig(
    MAIL_USERNAME=config.mail_username,
    MAIL_PASSWORD=config.mail_password,
    MAIL_FROM=config.mail_from,
    MAIL_PORT=config.mail_port,
    MAIL_SERVER=config.mail_server,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True,
)

async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    fm = FastMail(conn_config)
    await fm.send_message(message)
