from pathlib import Path

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader

from core.settings import MailSettings

template_dir = Path(__file__).parent.resolve() / "templates"


config = MailSettings.get()


conn_config = ConnectionConfig(
    MAIL_USERNAME=config.username,
    MAIL_PASSWORD=config.password,
    MAIL_FROM=config.username,
    MAIL_PORT=1025,
    MAIL_SERVER="localhost",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS=False,
)

env = Environment(loader=FileSystemLoader(template_dir))


class EmailSender:
    def __init__(self, email_to: str, subject: str):
        self.email_to = email_to
        self.subject = subject

    def _create_message(self, body) -> MessageSchema:
        return MessageSchema(
            subject=self.subject,
            recipients=[self.email_to],
            body=body,
            subtype="html"
        )

    async def _create_and_send_message(self, html: str) -> None:
        message = self._create_message(html)
        fm = FastMail(conn_config)
        await fm.send_message(message)

    async def verify_email(self, token: str, username: str) -> None:
        html = env.get_template("verify-by-email.html").render(
            username=username,
            verify_token=token
        )
        await self._create_and_send_message(html)

    async def change_email(self, change_email_token: str, username: str) -> None:
        html = env.get_template("change-email.html").render(
            username=username,
            change_email_token=change_email_token
        )
        await self._create_and_send_message(html)



