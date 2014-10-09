# -*- coding: utf-8 -*-
from mongoengine import *

connect('readingpub')


class User(Document):
    username = StringField(required=True, unique=True, max_length=100)
    email = EmailField(required=True, unique=True, max_length=200)
    password = StringField(required=True, max_length=100)
    register_date = DateTimeField()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __str__(self):
        return self.username
