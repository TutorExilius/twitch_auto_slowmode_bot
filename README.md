# twitch_auto_slowmode_bot
A Twitch Auto Slow Mode bot as chat flood protection.


IRC Token generation (IRC_OAUTH_TOKEN): https://www.twitchapps.com/tmi/

____
Setup:  Add your twitch credentials in a textfile, structured like "login_data.txt".
____
Configurtion:
This bot is deafult configured. You can use your custoum configuration in following lined in bot.py:

def __init__(...):
  ...
  # check flood period
  self.flood_check_intervall_in_seconds = 5

  # limit of messages while period "self.flood_check_intervall_in_seconds"
  self.flood_limit = 20

  # protection will be activated by counter 0
  self.flood_activation_counter = 3

  # deactivate slowmode after this period
  self.flood_protection_timeout_in_seconds = 30
  ...
  
 
____    
Usage:  py -m twitch_auto_slowmode_bot.main login_data.txt
