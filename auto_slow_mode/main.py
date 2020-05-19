import logging
import os
import sys
import time

from auto_slow_mode.bot import Bot


def main():
    # set logging / create log
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file = "logs/errors.log"
    logging.basicConfig(filename=file, filemode='w', level=logging.ERROR)

    if len(sys.argv) != 2:
        print("Usage: twitchbot <login_data.txt>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = list(filter(None, f.read().splitlines()))

    if len(lines) != 6:
        print(f"Missing Login-Data in file\nExpected:\nCLIENT_ID\nCLIENT_SECRET\nUSERNAME\nCHANNEL\nIRC_TOKEN\nUSER_ID")
        sys.exit(1)

    client_id = lines[0]
    client_secret = lines[1]
    user = lines[2].lower()
    channel = lines[3].lower()
    irc_token = lines[4]

    retries = 0
    sleep_time = 0

    while True:
        try:
            my_bot = Bot(client_id=client_id,
                         client_secret=client_secret,
                         user=user,
                         channel=channel,
                         irc_token=irc_token)

            my_bot.run()
        except Exception as e:
            retries += 1

            if sleep_time < 300:
                sleep_time = retries * 15

            logging.error(e)
            logging.error(f"\nRetry {retries}...\n")

            print(f"Error. Retry {retries} in {sleep_time} seconds...")
            time.sleep(sleep_time)


if __name__ == '__main__':
    main()
