# BL per definire ed inviare una mail

import aiosmtplib, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from BL.CommonFun import IsNullOrEmpyStr, LoggingManager
from Config.appsettings import (
    MAIL_SENDER, MAIL_PASSWORD, MAIL_SERVER,
    MAIL_PORT, MAIL_TLS,
    MAIL_USE_CREDENTIALS, MAIL_TEMPLATES_FOLDER, MAIL_RECEIVER_DEFAULT,
    MAIL_SYSTEMNAME, ABILITA_INVIO_MAIL
)
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Configurazione per inviare email in modo asincrono
conf = {
    "MAIL_USERNAME":MAIL_SENDER,
    "MAIL_PASSWORD":MAIL_PASSWORD,
    "MAIL_FROM":MAIL_SENDER,
    "MAIL_PORT":MAIL_PORT,
    "MAIL_SERVER":MAIL_SERVER,
    "MAIL_STARTTLS":MAIL_TLS,
    "MAIL_SSL_TLS":False,
    "USE_CREDENTIALS":MAIL_USE_CREDENTIALS,
    "TEMPLATE_FOLDER":MAIL_TEMPLATES_FOLDER  # Folder for HTML templates
}

# MailSenderClient
class EMailClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if IsNullOrEmpyStr(ABILITA_INVIO_MAIL) == True:
            raise RuntimeError('detail": "CONFIG KEY NOT FOUND: ABILITA_INVIO_MAIL')
        if ABILITA_INVIO_MAIL == False:
            return None
        if not cls._instance:
            cls._instance = super(EMailClient, cls).__new__(cls, *args, **kwargs)
            
            # Precarico l'ambiente per jinja2
            cls._instance.template_env = Environment(loader=FileSystemLoader(conf['TEMPLATE_FOLDER']))
            print('EMAILClient istanziato')
        return cls._instance
    
    # Function to send email asynchronously with dynamic placeholders
    async def send_email(self, templateName: str, receiver: str, subject: str, placeholders: dict):
        reiceverOk = receiver
        if IsNullOrEmpyStr(MAIL_RECEIVER_DEFAULT) == False:
            reiceverOk = MAIL_RECEIVER_DEFAULT

        template = self.template_env.get_template(templateName)
        html_content = template.render(placeholders)

        msg = MIMEMultipart('alternative')
        msg['From'] = conf["MAIL_FROM"]
        msg['To'] = receiver
        msg['Subject'] = subject

        # Imposto il corpo della mail html
        msg.attach(MIMEText(html_content, 'html'))
        
        # Imposto l'immagine
        imageFileName = 'logo.png'
        imagePath = conf['TEMPLATE_FOLDER']+'\logo.png'
        with open(imagePath, 'rb') as f:
            image_data = f.read()
            image = MIMEApplication(image_data, name=imageFileName)
            image.add_header('Content-ID', '<logo>')
            msg.attach(image)

        # Imposto la connessione al server SMTP
        try:
            server = aiosmtplib.SMTP(hostname=conf['MAIL_SERVER'], port=conf['MAIL_PORT'])
            await server.connect()
            await server.login(conf['MAIL_USERNAME'], conf['MAIL_PASSWORD'])

            # Send the email
            senderEmail = MAIL_SENDER
            await server.sendmail(senderEmail, reiceverOk, msg.as_string())

        except smtplib.SMTPAuthenticationError:
            LoggingManager().warning("SMTP | Authentication failed: check username/password.")
        except smtplib.SMTPConnectError:
            LoggingManager().error("SMTP | Failed to connect to SMTP server: check server details.")
        except (ConnectionError, TimeoutError) as e:
            LoggingManager().error(f"SMTP | Connection error: {e}")
        except Exception as e:
            # Catch-all for other unexpected errors
            LoggingManager().critical(f"SMTP | Unexpected error: {e}")
        finally:
            try:
                await server.quit()
            except Exception as e:
                LoggingManager().warning(f"SMTP | Error closing SMTP connection: {e}")

    async def send_login(self, receiver: str):
        current_time = datetime.now().strftime("%d/%m/%Y - %H:%M")
        ph = {
            "system_name": MAIL_SYSTEMNAME,
            "current_time": current_time
        }
        await self.send_email('login_template.html', receiver, 'Notifica - Promo+', ph)

    async def send_loginFailed5(self, receiver: str):        
        current_time = datetime.now().strftime("%d/%m/%Y - %H:%M")
        ph = {
            "system_name": MAIL_SYSTEMNAME,
            "current_time": current_time
        }
        await self.send_email('loginFailed5_template.html', receiver, 'Notifica - Promo+', ph)
    
    async def send_pwdChanged(self, receiver: str):
        ph = {
            "system_name": MAIL_SYSTEMNAME
        }
        await self.send_email('pwdChanged_template.html', receiver, 'Notifica - Promo+', ph)

    async def send_resetPwd(self, receiver: str):
        ph = {
            "system_name": MAIL_SYSTEMNAME
        }
        await self.send_email('resetPwd_template.html', receiver, 'Notifica - Promo+', ph)