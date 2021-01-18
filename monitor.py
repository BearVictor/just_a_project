import smtplib
import mimetypes
from modules import *
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import config as Config

cwd_name_regex = re.search(r'^.*?[/\\][^/\\]+?(_[^/\\]+$)', os.getcwd())
cwd_name = cwd_name_regex.group(1) if cwd_name_regex else ''

cache_dir = Config.cache_dir

def count_caches(dir_path, interval=60*10):
    count = 0
    while True:
        list_len = len(os.listdir(dir_path))
        difference = list_len - count
        msg = f'total: {list_len}\ndifference: {difference}\n{dir_path}'
        if list_len > count:
            print(msg)
            sleep(interval, '\n')
            count = list_len
        else:
            print('count_caches(): STOPPED! \n%s' % msg)
            email = Email('locfocchay@gmail.com', 'notify.Me')
            email_to = ['nnd2890@gmail.com']
            subject = 'scraping%s was STOPPED!' % cwd_name
            text = 'scraping%s\n%s' % (cwd_name, msg)
            email.email(email_to, subject, text=text)
            break

class Email:
    def __init__(self, email_from, password):
        self.email_from = email_from
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(email_from, password)

    def email(self, email_to, subject, *, text='', file_paths=[]):
        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["To"] = ", ".join(email_to)
        msg["Subject"] = subject

        msg.attach(MIMEText(text, 'plain'))

        for file_to_send in file_paths:
            ctype, encoding = mimetypes.guess_type(file_to_send)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)
            if maintype == "text":
                fp = open(file_to_send)
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(file_to_send, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(file_to_send, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(file_to_send, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            filename = re.sub('^.*/', '', file_to_send)
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attachment)

        self.server.sendmail(self.email_from, email_to, msg.as_string())
        self.server.quit()
        print('Email(done - attach_files): %s...' % subject)

if __name__ == '__main__':

    count_caches(cache_dir)