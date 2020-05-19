from abc import ABC

from twitchio.ext import commands
import asyncio


class Bot(commands.Bot, ABC):
    def __init__(self, client_id, client_secret, user, channel, irc_token, user_id):
        super().__init__(irc_token=irc_token, client_id=client_id,
                         client_secret=client_secret,
                         scopes="channel:moderate",
                         nick=user, prefix='!',
                         initial_channels=[channel])

        self.user_id = user_id
        self.username = user
        self.channel = channel
        self.self_user = None
        self.db = None
        self.ws = self._ws

        self._message_cnt = 0
        self._online = False
        self._flood_protection_activated = False

        # check flood period
        self.flood_check_intervall_in_seconds = 5

        # limit of messages while period "self.flood_check_intervall_in_seconds"
        self.flood_limit = 20

        # protection will be activated by counter 0
        self.flood_activation_counter = 3

        # deactivate slowmode after this period
        self.flood_protection_timeout_in_seconds = 30

        print(f"Connect as: {self.username}", flush=True)
        print(f"Connecting to {self.ws._host} (secured connection) ...\n", flush=True)

    async def event_ready(self):
        print(f"Successfully joined channel: {self.channel}\n", flush=True)

        # You must request specific capabilities before you can use them
        await self._ws.send_cap("membership")
        await self._ws.send_cap("tags")
        await self._ws.send_cap("commands")

        self._online = True
        await self.ws.send_privmsg(self.channel, f"Flood-Protection activated. Hello @all. Please be gentle! :)")

        asyncio.ensure_future(self.check_chat_flood())

    async def check_chat_flood(self):
        try:
            flood_activation_counter_ = self.flood_activation_counter

            while self._online:
                if self._flood_protection_activated:
                    await asyncio.sleep(self.flood_protection_timeout_in_seconds)
                    await self.go_unslow(5)
                    self._flood_protection_activated = False
                else:
                    await asyncio.sleep(self.flood_check_intervall_in_seconds)
                    print("Check flood")

                    if self._message_cnt > self.flood_limit:
                        if flood_activation_counter_ > 0:
                            flood_activation_counter_ -= 1
                            print(f"Flood Warning Counter - left: {flood_activation_counter_}")
                        else:
                            await self.go_slow(5)
                            self._flood_protection_activated = True
                            flood_activation_counter_ = self.flood_activation_counter
                    else:
                        flood_activation_counter_ = self.flood_activation_counter
                        print(f"No flood warning - resetted Flood Warning Counter to {flood_activation_counter_}")

                    self._message_cnt = 0


        except Exception as ex:
            print(ex)

    async def event_message(self, message):
        await self.handle_commands(message)
        self._message_cnt += 1

    async def go_slow(self, duration):
        await self.ws.send_privmsg(self.channel, f"/slow {duration}")

    async def go_unslow(self, duration):
        await self.ws.send_privmsg(self.channel, "/slowoff")
