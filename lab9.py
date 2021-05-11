import argparse
import datetime
import smtplib
from bs4 import BeautifulSoup
import requests as requests

import mail_config


def send_email(message, receiver="kubaserdynski@gmail.com"):
    server = smtplib.SMTP(mail_config.main["SMPT Server"], 587)
    server.starttls()
    server.ehlo()
    server.login(mail_config.main["Username"], mail_config.main["Password"])
    message = f'Subject: Hello! It is {datetime.date.today()}' \
              f' and the time is {datetime.datetime.today().time()}\n' + message
    sender = mail_config.main["Username"]
    server.sendmail(sender, receiver, message)
    server.quit()


def cat_facts(how_many=1):
    response = requests.get('https://cat-fact.herokuapp.com/facts')
    facts = []
    for fact in response.json():
        facts.append(fact["text"])
    if how_many < 1 or how_many > len(facts):
        how_many = 5
    print(facts[:how_many])
    return facts[:how_many]


def list_researchers(letter, link="https://wiz.pwr.edu.pl/pracownicy?letter="):
    link += letter.upper()
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")
    divs = soup.find_all("div", class_="col-text text-content")
    to_print = []
    for div in divs:
        to_print.append(f'{div.a.contents[0]} - {div.p.contents[0]}')

    print(f"The list of researchers starting with the letter {letter}:")
    if len(to_print) == 0:
        print("No researchers :c")
    else:
        print(to_print)

    return to_print


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The idea of the application is to practice internet access")
    parser.add_argument('--mail', type=str, help="Sending an email")
    parser.add_argument('--receiver', type=str, help="Specify receiver for a mail")
    parser.add_argument("--cat-facts", type=int, help="How many cat facts to print")
    parser.add_argument('--teachers', help="First letter of the teachers' name")
    args = parser.parse_args()
    if args.mail:
        if args.receiver:
            send_email(args.mail, args.receiver)
        else:
            send_email(args.mail)

    if args.cat_facts:
        cat_facts(args.cat_facts)

    if args.teachers:
        list_researchers(args.teachers)
# --mail "hejo" --receiver jakub.seredynski.official@gmail.com --cat-facts 7 --teachers C
