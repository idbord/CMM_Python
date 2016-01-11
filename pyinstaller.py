# -*- coding: utf-8 -*-
__author__ = 'idbord'

import  os

if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['run.py', '-w', '--icon=cmm.ico']
    run(opts)
