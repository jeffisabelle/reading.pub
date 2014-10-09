# -*- coding: utf-8 -*-
import bcrypt
import slugify
import re


def encrypt(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, pwd_hash):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        pwd_hash.encode("utf-8")) == pwd_hash.encode("utf-8")


def make_slug(text):
    return slugify.slugify(text.replace(u"ı", u"i"))


def check_mail(text):
    reg = re.compile(
        '[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})'
    )

    regMail = reg.match(text)

    if not regMail:
        return False
    else:
        return True
