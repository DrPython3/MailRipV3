#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-10-10'
__version__ = '2'
__contact__ = 'https://github.com/DrPython3'

'''
-------------------------------------
Various Functions used by Mail.Rip V3
-------------------------------------

Part of << Mail.Rip V3 >>
'''

# [IMPORTS]
# ---------

import sys
import os
import re
import json

# [FUNCTIONS]
# -----------

def result(target_file, result_output):
    '''
    Saves any output to a certain file in directory "results".

    :param str target_file: file to use
    :param str result_output: output to save
    :return: True (output saved), False (output not saved)
    '''
    try:
        os.makedirs('results')
    except:
        pass
    try:
        output_file = os.path.join('results', str(f'{target_file}.txt'))
        with open(str(output_file), 'a+') as output:
            output.write(result_output + '\n')
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
    if re.search(email_format, email):
        return True
    else:
        return False

def blacklist_check(email):
    '''
    Checks whether the domain of a given email is on the blacklist.

    :param str email: email to check
    :return: True (is blacklisted), False (not blacklisted)
    '''
    with open('inc_domainblacklist.json') as included_imports:
        json_object = json.load(included_imports)
        blacklist = (json_object['domainblacklist'])
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
    if re.search(domain_format, domain):
        return True
    else:
        return False

def clean():
    '''
    NO-GUI-Version only: Provides a blank screen on purpose.

    :return: None
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    return None

# DrPython3 (C) 2021 @ GitHub.com
