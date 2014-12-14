# -*- coding: utf-8 -*-
import smtplib
import mailconf
import codecs

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.models import User


class MailModule(object):
    """
    """

    def __init__(self, username, recepients):
        """

        Arguments:
        - `username`:
        - `recepients`:
        """
        self._username = username
        self._recepients = self.parse_recepients(recepients)
        self._user = User.objects(username=self._username).first()

    def share_post(self, post):
        """

        Arguments:
        - `post`: Post object to be shared
        """
        for recepient in self._recepients:
            if recepient:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = self._username + " - " + post.title
                msg['From'] = "Reading Pub <noreply@reading.pub> "
                msg['To'] = recepient

                text = "text mails are not supported. (yet)"
                part1 = MIMEText(text, 'plain', "utf-8")

                html = self.build_mail(post)
                part2 = MIMEText(html, 'html', "utf-8")

                msg.attach(part1)
                msg.attach(part2)

                self.send_mail(msg)

    def share_tag(self, tag, posts):
        """

        Arguments:
        - `tag`: tag string
        - `posts`: posts object that belongs to the tag
        """
        for recepient in self._recepients:
            if recepient:
                plen = str(len(posts))
                msg = MIMEMultipart('alternative')
                msg['Subject'] = self._username + " shared " + plen + " article with you"
                msg['From'] = "Reading Pub <noreply@reading.pub> "
                msg['To'] = recepient

                text = "text mails are not supported. (yet)"
                part1 = MIMEText(text, 'plain', "utf-8")

                html = self.build_mail(posts=posts)
                part2 = MIMEText(html, 'html', "utf-8")

                msg.attach(part1)
                msg.attach(part2)

                self.send_mail(msg)

    def build_mail(self, post=None, posts=None):
        """

        Arguments:
        - `self`:
        - `post`: This is not none when single post shared
        - `posts`: This is not none when multiple posts (tag) shared
        """

        snip_file = codecs.open(
            "utils/mail/templates/link-snippet-inlined.html",
            "r", encoding='utf8'
        )

        if post:
            snip_file.seek(0)
            snippet = snip_file.read()
            rpub_path = str(post.seq) + "/" + str(post.slug) + "/"
            rpub_url = "http://reading.pub/" + rpub_path
            snippet = snippet.replace("###title###", post.title)
            snippet = snippet.replace("###domain###", post.domain)
            snippet = snippet.replace("###url###", rpub_url)
            snippet_total = snippet
        elif posts:
            snippet_total = ""
            for post in posts:
                snip_file.seek(0)
                snippet = snip_file.read()
                rpub_path = str(post.seq) + "/" + str(post.slug) + "/"
                rpub_url = "http://reading.pub/" + rpub_path
                snippet = snippet.replace("###title###", post.title)
                snippet = snippet.replace("###domain###", post.domain)
                snippet = snippet.replace("###url###", rpub_url)
                snippet_total += snippet

        snip_file.close()

        with codecs.open(
            "utils/mail/templates/template-inlined.html",
            "r", encoding='utf8'
        ) as f:
            html = f.read()

        # html = file("utils/mail/templates/template-inlined.html", "r").read()
        html = html.replace("###snippet###", snippet_total)
        return html

    def parse_recepients(self, recepients):
        """
        Recepients comes as a string.
        This function returns recepients as an array

        Arguments:
        - `recepients`: recepients string
        """
        recepients = [r.strip('\r\n ') for r in recepients.split("\n")]
        print recepients
        return recepients

    def send_mail(self, msg):
        """
        """

        # msg = MIMEMultipart('alternative')

        # msg['Subject'] = self._username + ": " + post.title
        # msg['From'] = "Reading Pub <noreply@reading.pub> "
        # msg['To'] = "muhitosan@gmail.com"

        # text = ":o"
        # part1 = MIMEText(text, 'plain')

        # # with codecs.open(
        # #         "utils/mail/templates/template.txt", 'r', encoding='utf8'
        # # ) as f:
        # #     text = f.read()

        # html = file("utils/mail/templates/template.html", "r").read()
        # part2 = MIMEText(html, 'html')

        # msg.attach(part1)
        # msg.attach(part2)

        username = mailconf.smtp_username
        password = mailconf.smtp_password

        s = smtplib.SMTP(mailconf.smtp_server, mailconf.smtp_port)

        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())

        s.quit()
