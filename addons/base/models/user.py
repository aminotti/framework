# -*-coding:utf-8 -*
from lib.orm import *
from app import HTTPMethod
from config import conf


class User(HTTPMethod, ORMGeneric):
    # uri = conf.sample_moduleDb_uri
    uri = 'ldap://localhost/dc=forpro-creteil,dc=org'  # Require for LDAP
    binddn = 'cn=admin,dc=forpro-creteil,dc=org'  # Facultative
    bindpwd = 'Locfad94!'  # Facultative
    rdn = 'ou=people'  # Facultative, ou=user will be used if ommit
    object_class = ['dafcoCreteilPerson', 'dafcoCreteilMailbox', 'shadowAccount', 'domainRelatedObject']  # Require for LDAP

    mail = EmailField()
    uid = StringField(identifier=True)
    password = StringField(fieldName='userPassword')
    prenom = StringField(fieldName='givenName', notNone=False)
    nom = StringField(fieldName='sn')
    applications = SetField(values=['infovae', 'ofac'])
    structure = StringField(fieldName='structurePrincipale')
    fullname = StringField(fieldName='cn')
    phone = PhoneField(fieldName='telephoneNumber')
    smtp = BoolField(fieldName='SMTPActif')
    km = IntField(fieldName='shadowLastChange')
    heure = TimeField(fieldName='associatedDomain')
    meeting = DateTimeField(fieldName='syncKELIOS')
    photo = ImageField(fieldName='userPKCS12', mimeTypes=['image/gif', 'image/jpeg', 'image/png'], mimeType='image/gif', extension='gif')
