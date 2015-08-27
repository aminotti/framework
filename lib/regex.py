# -*-coding:utf-8 -*
import re


class RFC3339(object):
    date = re.compile("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$")  # <AAAA>-<MM>-<DD>
    time = re.compile("^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])(:(([0-5][0-9])|60))?(.[1-9]+)?$")  # <HH>:<MM>[:<SS>[.<XXXX>]]
    datetime = re.compile("^[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])(t|T)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])(:(([0-5][0-9])|60))?(.[1-9]+)?(Z|((\+|-)(0[0-9]|1[0-9]|2[0-3])):([0-5][0-9]))$")  # <AAAA>-<MM>-<DD>T<HH>:<MM>[:<SS>[.<XXXX>]](Z|((+|-)<HH>:<MM>))


HTMLColor = re.compile('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
XSS = re.compile('((\%3C)|<)[^\n]+((\%3E)|>)')  # Cross Site Scripting
MAIL = re.compile('^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
PHONE = re.compile('^\+?[\(|\)|0-9|\s|\-]*$')  # optinal + follow by (, ), space, -, and figure from 0 to 9 unlimitted
URL = re.compile('^[a-zA-Z]+://([a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(%[0-9a-fA-F][0-9a-fA-F]))+$')
