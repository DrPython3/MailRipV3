#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-10-10'
__version__ = '2.1'
__contact__ = 'https://github.com/DrPython3'

'''
---------------------------------
Functions for Handling Combolists
---------------------------------

Part of << Mail.Rip V3 >>
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
    loaded_combos = []
    output_blacklist = str('combos_blacklisted')
    output_clean = str('combos_cleaned')
    timestamp = datetime.now()
    output_startup = str(
        'Comboloader start: '
        + str(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        + f', combofile: {input_file}'
    )
    result(
        output_blacklist,
        str('\n' + output_startup + '\n' + len(output_startup)*'=')
    )
    result(
        output_clean,
        str('\n' + output_startup + '\n' + len(output_startup) * '=')
    )
    try:
        for line in open(input_file, 'r'):
            try:
                new_combo = str(
                    line.replace(';', ':').replace(',', ':').replace('|', ':')
                )
                with_email = email_verification(
                    new_combo.split(':')[0]
                )
                if with_email == False:
                    continue
                blacklisted = blacklist_check(
                    new_combo.split(':')[0]
                )
                if blacklisted == True:
                    result(
                        output_blacklist,
                        new_combo
                    )
                    continue
                if new_combo in loaded_combos:
                    continue
                else:
                    loaded_combos.append(new_combo)
                    result(
                        output_clean,
                        new_combo
                    )
            except:
                continue
    except:
        result(
            output_blacklist,
            str(f'An error occurred while importing the combos from file: {input_file}.')
        )
        result(
            output_clean,
            str(f'An error occurred while importing the combos from file: {input_file}.')
        )
    return loaded_combos

# DrPython3 (C) 2021 @ GitHub.com
