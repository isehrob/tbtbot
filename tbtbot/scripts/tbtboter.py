# console program for creating, registering
# and etc. telegram bots which will help to
# automate some routines while creating and 
# developing telegram bots

import os
import sys
import subprocess
import argparse
import re

import tbtbot
from tbtbot.scripts import templatestrings



def get_parser():
    """command line argument parser"""
    pparser = argparse.ArgumentParser(
        description='A console program which helps to create telegram bots'
    )
    pparser.add_argument('-s', '--serve', help='start the bot', action="store_true")
    pparser.add_argument('-c', '--create', help="create a tornado based telegram bot",
                        type=str, nargs='?', const='')
    pparser.add_argument('-cs', '--create_sertificate', help='create self-signed sertificate',
                        action="store_true")
    return pparser

# these will ease the life of
# the telegram bot developers
def set_webhook():
    # sets webHook to listen for new updates
    pass

def get_webhookInfo():
    # gets the webhook info 
    pass

def delete_webhook():
    # deletes the webHook
    pass

def create_sertificate(bot_name):
    # creates self signed ssl certificate
    cwd = os.getcwd()
    cert_path = input('Please specify the path for the sertificate [default: current dir]: ', )

    try:
        os.chdir(cert_path)
    except FileNotFoundError:
        print('Using default value for the path')
        cert_path = cwd
        pass

    rtncode = subprocess.call([
        "openssl",
        "req", "-newkey", "rsa:2048", "-sha256", "-nodes",
        "-keyout", "%s_private.key" % bot_name,
        "-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
    ])
    if not rtncode:
        print("Self-signed sertificate is created in '%s'" % os.path.abspath(cert_path))
        return cert_path
    os.chdir(cwd)
    return False


def create_with_webhook(bot_name, cert_path = False):
    # creates the telegram bot skeleton suited
    # to get updates by webHook
    cwd = os.getcwd()
    print('creating with webhook')
    os.mkdir(bot_name)
    os.chdir(os.path.abspath(bot_name))
    temp_dir = os.path.join(os.path.dirname(tbtbot.__file__), 'template')

    if cert_path:
        cert_path = os.path.abspath(cert_path)

    for entry in os.listdir(temp_dir):
        if os.path.isfile(os.path.join(temp_dir, entry)):
            with open(os.path.join(temp_dir, entry)) as f:
                with open(entry, 'w') as w:
                    if entry == '.env.example' and cert_path:
                        w.write(templatestrings.envtemplate % (
                            os.path.join(cert_path, bot_name + '_private.key'),
                            os.path.join(cert_path, bot_name + '_public.key')
                            ))
                    elif entry == 'configuration.py':
                        w.write(templatestrings.configtemplate)
                    else:
                        w.write(f.read())
    os.chdir(cwd)
    return


def create_with_getUpdates(bot_name):
    # creates the telegram bot skeleton without
    # webhook functionality for some reasons
    # for example when the host hasn't static ip
    cwd = os.getcwd()
    print('creating with getUpdates')
    os.mkdir(bot_name)
    os.chdir(os.path.abspath(bot_name))
    temp_dir = os.path.join(os.path.dirname(tbtbot.__file__), 'template2')

    for entry in os.listdir(temp_dir):
        if os.path.isfile(os.path.join(temp_dir, entry)):
            with open(os.path.join(temp_dir, entry)) as f:
                with open(entry, 'w') as w:
                    if entry == '.env.example':
                        w.write(templatestrings.env2template)
                    elif entry == 'configuration.py':
                        w.write(templatestrings.config2template)
                    else:
                        w.write(f.read())
    os.chdir(cwd)
    return


def create_bot(bot_name):

    if not bot_name:
        bot_name = input('Please, specify a name for your bot: ', )
        if not bot_name:
            exit("Can't create a bot without a name")
    updates_type = input('Ok, how do you want to get your updates?\n\
                        Through 1 webhooks / 2 long polling [1/2]: ', )

    if int(updates_type) not in [1,2]:
        exit('Unkown option, please retry')

    if int(updates_type) is 1:
        create_ssl = input('Want to create self-signed sertificate? [Yes/No]: ', )
        if create_ssl not in ['Yes', 'No']:
            exit('Unkown option, please retry')
        if create_ssl == 'Yes':
            cert_path = create_sertificate(bot_name)
            if cert_path is False:
                exit('Couldn\'t create sertificate')
            create_with_webhook(bot_name, cert_path)
        if create_ssl == 'No':
            create_with_webhook(bot_name)

    if int(updates_type) is 2:
        create_with_getUpdates(bot_name)

    print('DONE!')
    return


def main():
    # main entry point of the console program
    CMD_PARSER = get_parser()
    CMD_ARGS = CMD_PARSER.parse_args()

    if CMD_ARGS.create is not False:
        print('Creating bot')
        create_bot(CMD_ARGS.create)

    if CMD_ARGS.create_sertificate:
        print('Creating self-signed sertificate')
        create_sertificate('my_bot')

    if CMD_ARGS.serve:
        print('Serve')
    return False
