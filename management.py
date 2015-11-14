#!/usr/bin/env python
# -*-coding:utf-8 -*

from app.config import conf
from app.manager import manager


if __name__ == '__main__':
    manager.run('localhost', 5000, debug=True)
