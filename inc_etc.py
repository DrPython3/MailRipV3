#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-12-04'
__version__ = '2.51'
__contact__ = 'https://github.com/DrPython3'

'''
-------------------------------------
Various Functions used by Mail.Rip V3
-------------------------------------

Part of << Mail.Rip V3: https://github.com/DrPython3/MailRipV3 >>
'''

# [IMPORTS]
# ---------

import sys
import os
import re
import json
import tkinter as tk
from tkinter import filedialog

# [FUNCTIONS]
# -----------

def result(target_file, result_output):
    '''
    Saves any output to a certain file in directory "results".

    :param str target_file: file to use
    :param str result_output: output to save
    :return: True (output saved), False (output not saved)
    '''
    # create results directory if not exists:
    try:
        os.makedirs('results')
    except:
        pass
    # write output to given file:
    try:
        output_file = os.path.join('results', str(f'{target_file}.txt'))
        with open(str(output_file), 'a+') as output:
            output.write(str(f'{result_output}\n'))
        return True
    except:
        return False

def email_verification(email):
    '''
    Checks whether a certain string represents an email.

    :param str email: string to check
    :return: True (is email), False (no email)
    '''
    email_format = '^([\w\.\-]+)@([\w\-]+)((\.(\w){2,63}){1,3})$'
    # check given email using format-string:
    if re.search(email_format, email):
        return True
    else:
        return False

def blacklist_check(email):
    '''
    Checks whether the domain of a given email is on the blacklist.

    :param str email: email to check
    :return: True (blacklisted), False (not blacklisted)
    '''
    # try to load blacklist from JSON-file:
    try:
        with open('inc_domainblacklist.json') as included_imports:
            load_blacklist = json.load(included_imports)
            blacklist = (load_blacklist['domainblacklist'])
    # on errors, set empty blacklist:
    except:
        blacklist = []
    # check email domain against blacklist:
    if str(email.split('@')[1]) in blacklist:
        return True
    else:
        return False

def domain_verification(domain):
    '''
    Checks whether a certain string represents a domain.

    :param str domain: string to check
    :return: True (is domain), False (no domain)
    '''
    domain_format = '^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    # check whether string is a valid domain:
    if re.search(domain_format, domain):
        return True
    else:
        return False

def clean():
    '''
    NO-GUI-Version only: Provides a blank screen on purpose.

    :return: None
    '''
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass
    return None

def get_combofile_nogui():
    '''
    NO-GUI-Version only: Provides a open-file-dialog using tkinter.

    :return: combofile chosen by user
    '''
    open_file = tk.Tk()
    # hide Tk window:
    open_file.withdraw()
    # start dialog:
    import_file = filedialog.askopenfilename(
        title='Select Combofile',
        filetypes=(('txt files', '*.txt'),('all files','*.*'))
    )
    # kill Tk window and return chosen file:
    try:
        open_file.destroy()
        open_file.quit()
    except:
        pass
    return import_file

# DrPython3 (C) 2021 @ GitHub.com
