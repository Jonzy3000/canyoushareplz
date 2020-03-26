import os
import logging
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
from canYouShare import CanYouShare
import schedule
import time

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


def start_day_schedule():
    schedule.every(0).to(9 * 60).minutes.do(send_meet)


before = time.time()
test = 15


def check_works():
    schedule.every(0).to(test).seconds.do(send_meet)


def setup_schedules():
    schedule.every().monday.at('09:30').do(start_day_schedule)
    schedule.every().tuesday.at('09:30').do(start_day_schedule)
    schedule.every().wednesday.at('09:30').do(start_day_schedule)
    schedule.every().thursday.at('09:30').do(start_day_schedule)
    schedule.every().friday.at('09:30').do(start_day_schedule)
    schedule.every(test).seconds.do(check_works)


def send_meet():
    canYouShare = CanYouShare("general")
    message = canYouShare.get_message_payload()
    now = time.time()
    global before
    print("Time since last message clock 🕔 ", now - before)
    before = now
    print("\n\n")
    slack_web_client.chat_postMessage(**message)

    return schedule.CancelJob


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    setup_schedules()
    while True:
        schedule.run_pending()
        time.sleep(1)
