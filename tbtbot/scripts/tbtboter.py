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



def get_parser():
    """command line argument parser"""
    pparser = argparse.ArgumentParser(
        description='A console program which helps to create telegram bots',
        usage='tbtboter [-h] create serve')
    pparser.add_argument('--create', type=str, 
                         help='name of the bot')
    pparser.add_argument('--create_ssl', type=str, 
                         help='create self-signed sertificate')
    pparser.add_argument('--serve', 
                         help='starts the bot')
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

def create_sertificate(cert_path, bot_name):
    # creates self signed ssl certificate
    cwd = os.getcwd()
    os.chdir(cert_path)
    if subprocess.call([
        "openssl",
        "req", "-newkey", "rsa:2048", "-sha256", "-nodes",
        "-keyout", "%s_private.key" % bot_name,
        "-x509", "-days", "365", "-out", "%s_public.pem" % bot_name
    ]):
        os.chdir(cwd)
        return True
    return False


def create_with_webhook(bot_name):
    # creates the telegram bot skeleton suited
    # to get updates by webHook
    print('creating with webhook')
    os.mkdir(bot_name)
    os.chdir(os.path.abspath(bot_name))
    temp_dir = os.path.join(os.path.dirname(tbtbot.__file__), 'template')
    for entry in os.listdir(temp_dir):
        if os.path.isfile(os.path.join(temp_dir, entry)):
            with open(os.path.join(temp_dir, entry)) as f:
                with open(entry, 'w') as w:
                    w.write(f.read())
    os.chdir('../')
    print('Done!')


def create_with_getUpdates():
    # creates the telegram bot skeleton without
    # webhook functionality for some reasons
    # for example when the host hasn't static ip
    pass


def main():
    # main entry point of the console program
    CMD_PARSER = get_parser()
    CMD_ARGS = CMD_PARSER.parse_args()
    if CMD_ARGS.create:
        print('Creating bot')
        create_with_webhook(CMD_ARGS.create)

    if CMD_ARGS.create_ssl:
        print('Creating self-signed sertificate')
        create_sertificate('./', 'my_bot')

    if CMD_ARGS.serve:
        print('Serve')
    return False
