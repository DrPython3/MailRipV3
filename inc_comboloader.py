#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-12-04'
__version__ = '2.4'
__contact__ = 'https://github.com/DrPython3'

'''
---------------------------------
Functions for Handling Combolists
---------------------------------

Part of << Mail.Rip V3: https://github.com/DrPython3/MailRipV3 >>
'''

# [IMPORTS]
# ---------

import sys
from datetime import datetime
from inc_etc import result
from inc_etc import email_verification
from inc_etc import blacklist_check

# [FUNCTIONS]
# -----------

def comboloader(input_file):
    '''
    Loads combos from a given file.

    :param str input_file: file containing the combos
    :return: list with loaded combos
    '''
    # set variables:
    loaded_combos = []
    output_blacklist = str('combos_blacklisted')
    output_clean = str('combos_loaded')
    # log message on start:
    timestamp = datetime.now()
    output_startup = str(
        'Comboloader started on: '
        + str(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        + f', combofile: {input_file}'
    )
    # logging import of combofile:
    result(output_blacklist, str('\n' + output_startup + '\n' + len(output_startup)*'='))
    result(output_clean, str('\n' + output_startup + '\n' + len(output_startup) * '='))
    # import the combos:
    try:
        for line in open(input_file, 'r'):
            try:
                # replace any other seperator than semicolon in combos:
                new_combo = str(
                    line.replace(';', ':').replace(',', ':').replace('|', ':')
                )
                # check combo for email address:
                with_email = email_verification(
                    new_combo.split(':')[0]
                )
                if with_email == False:
                    continue
                # check email domain against provider blacklist:
                blacklisted = blacklist_check(
                    new_combo.split(':')[0]
                )
                if blacklisted == True:
                    new_combo = str(new_combo.replace('\n', ''))
                    result(output_blacklist,new_combo)
                    continue
                # add unique combos to target-list:
                if new_combo in loaded_combos:
                    continue
                else:
                    loaded_combos.append(new_combo)
                    new_combo = str(new_combo.replace('\n', ''))
                    result(output_clean, new_combo)
            except:
                continue
    # write logs when finished and quit:
        result(output_blacklist, str(f'\nCombos imported from file: {input_file}.\n=== END OF IMPORT ==='))
        result(output_clean, str(f'\nCombos imported from file: {input_file}.\n=== END OF IMPORT ==='))
    except:
        result(output_blacklist, str(f'\nAn error occurred while importing the combos from file: {input_file}.\n=== END OF IMPORT ==='))
        result(output_clean, str(f'\nAn error occurred while importing the combos from file: {input_file}.\n=== END OF IMPORT ==='))
    return loaded_combos

# DrPython3 (C) 2021 @ GitHub.com
