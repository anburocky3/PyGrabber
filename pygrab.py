#!/usr/bin/python3
import sys, os
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format

import requests
from lxml import html 

USERNAME = "<USERNAME>"
PASSWORD = "<PASSWORD>"

LOGIN_URL = "<LOGIN_URL>"
REDIRECT_URL = "<REDIRECT_URL>" #If Any (Optional)
URL = "<URL_TO_GRAB>"

def getRanges():
    range1 = input("Enter the grab range where you want to start (Range A): ? \n")
    range2 = input("Enter the grab range where you want to end (Range B): ? \n")
    return range1, range2

def main():
    print(chr(27) + "[2J")
    cprint('+-' + '-' * 75 + '-+ \n', 'yellow')
    cprint(figlet_format('\t \t \t Py GRABBER \n', font='banner3'),
       'green', attrs=['bold'])
    cprint('\t Version: 1.O |\t Author: Anbuselvan Rocky  |  www.anbuselvanrocky.in')
    cprint('+-' + '-' * 75 + '-+', 'yellow')
    cprint("Description :", 'green')
    cprint("This script bypasses Login authentication and grabs all secure content.")
    cprint('+-' + '-' * 75 + '-+ \n', 'yellow')

    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(
        LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

    resultRedirect = session_requests.get(
        REDIRECT_URL, headers=dict(referer=REDIRECT_URL))

    # Scrape url
    rangea, rangeb = getRanges()

    for x in range(int(rangea), int(rangeb)):
        resultPrb = session_requests.get(URL + str(x), headers=dict(referer=URL + str(x)))
        if resultPrb.text == "null<br /><br />":
            cprint("----------------------------------------------------------", 'yellow')
            cprint("#" + str(x) + " has NULL and has nothing to grab! Skipping . . .", 'red')
        else:
            if not os.path.exists('datas'):
                os.makedirs('datas')
                cprint("----------------------------------------------------------", 'yellow')
                cprint(" Looks, like you don't have data folder. \n", "red")
                cprint(" Don't worry! We have created it for you. Chill! \n", "green")
            file = open('datas/' + str(x) + ".html", "w")
            file.write(resultPrb.text)
            file.close()
            cprint("----------------------------------------------------------", 'yellow')
            cprint('#' + str(x)+" Has been created. Check your directory.", 'green')

    cprint("----------------------------------------------------------", 'yellow')


if __name__ == '__main__':
    main()
