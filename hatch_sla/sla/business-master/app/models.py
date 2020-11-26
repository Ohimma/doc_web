# -*- coding: utf-8 -*-

from .db import db

class Business(db.Model):
    __tablename__ = 'business'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(64))
    name_english = db.Column(db.String(64))
    person_duty = db.Column(db.String(64))
    org_id = db.Column(db.String(64))

    def __str__(self):
        return '(%s, %s, %s, %s, %s}' % (self.id, self.name, self.name_english, self.person_duty, self.org_id)
#    def __repr__(self):
#        return '%r' % self.id
#        return self.name, self.id

#    def __str__(self):
#        return self.__repr__()
#
#    class Meta:
#        db_table = 'business'
#        ordering = ['name']

class User(db.Model):

    # Columns
    __tablename__ = 'cmdb_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True)
    pwd = db.Column(db.Integer, default=0)

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd

    def __repr__(self):
        return '<User %r>' % self.name

    def __str__(self):
        return '<User %s>' % self.name
