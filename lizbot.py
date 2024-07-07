# This example requires the 'message_content' intent.
from datetime import datetime
import time
import threading
import weather
import env

import discord
import requests
import json
import asyncio
from random import choice, randint, shuffle
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cards = [
    "The Fool(0)",
    "The Magician(I)",
    "The High Priestess(II)",
    "The Empress(III)",
    "The Emporer(IV)",
    "The Heirophant(V)",
    "The Lovers(VI)",
    "The Chariot(VII)",
    "Strength(VIII)",
    "The Hermit(IX)",
    "Wheel of Fortune(X)",
    "Justice(XI)",
    "The Hanged Man(XII)",
    "Death(XIII)",
    "Temperance(XIV)",
    "The Devil(XV)",
    "The Tower(XVI)",
    "The Star(XVII)",
    "The Moon(XVIII)",
    "The Sun(XIX)",
    "Judgement(XX)",
    "The World(XXI)",
    "King of Swords",
    "Queen of Swords",
    "Knight of Swords",
    "Page of Swords",
    "One of Swords",
    "Two of Swords",
    "Three of Swords",
    "Four of Swords",
    "Five of Swords",
    "Six of Swords",
    "Seven of Swords",
    "Eight of Swords",
    "Nine of Swords",
    "Ten of Swords",
    "King of Batons",
    "Queen of Batons",
    "Knight of Batons",
    "Page of Batons",
    "One of Batons",
    "Two of Batons",
    "Three of Batons",
    "Four of Batons",
    "Five of Batons",
    "Six of Batons",
    "Seven of Batons",
    "Eight of Batons",
    "Nine of Batons",
    "Ten of Batons",
    "King of Coins",
    "Queen of Coins",
    "Knight of Coins",
    "Page of Coins",
    "One of Coins",
    "Two of Coins",
    "Three of Coins",
    "Four of Coins",
    "Five of Coins",
    "Six of Coins",
    "Seven of Coins",
    "Eight of Coins",
    "Nine of Coins",
    "Ten of Coins",
    "King of Cups",
    "Queen of Cups",
    "Knight of Cups",
    "Page of Cups",
    "One of Cups",
    "Two of Cups",
    "Three of Cups",
    "Four of Cups",
    "Five of Cups",
    "Six of Cups",
    "Seven of Cups",
    "Eight of Cups",
    "Nine of Cups",
    "Ten of Cups",
]

usercards = []


class Lizbot(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        shuffle(cards)
        # threading.Timer(interval=1, function=self.checkTime).start()
        # print(sched_event)

    # def checkTime(self):
    # This function runs periodically every 1 second
    # threading.Timer(interval=1, function=self.checkTime).start()

    # now = datetime.now()

    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)

    # if current_time == "02:11:00":  # check if matches with the desired time
    # print("sending message")

    async def on_message(self, message: discord.Message):
        user_message = message.content
        if not user_message:
            print("(Message was empty because intents were not enabled probably)")
            return

        # dont respond to self
        if message.author.id == self.user.id:
            return

        # dont respond to pk bots
        if message.author.id == 1115685378704277585:
            return
        # ignore messages without proxy
        if user_message[0] != "?":
            return
        # delete proxy
        user_message = user_message[1:]

        try:
            print(user_message)
            print("getting response")
            response: str = get_response(message, user_message)
            # import time
            # time.sleep(1)
            if response is None:
                await message.channel.send("Sorry, I don't know that command")
            await message.channel.send(response)
        except Exception as e:
            print(e)


def get_response(message: discord.message, user_input: str) -> str:
    lowered: str = user_input.lower()
    print(lowered)

    if lowered == "":
        return "Well you're awfully silent..."

    hello_msgs = [
        "hello",
        "hi",
        "hihi",
        "howdy",
        "hiya",
        "hey",
        "greetings",
        "yo",
        "salutations",
    ]
    for hmsg in hello_msgs:

        if hmsg in lowered:
            greetings = [
                "Hello there",
                "Hi",
                "Greetings",
                "Hihi",
                "Howdy",
                "Yo",
                "Salutations",
            ]
            return greetings[randint(0, 6)]

    # checkin_msgs = [
    # "how are you",
    # "how are you?",
    # "how are you doing?",
    # "how are you doing",
    # "how are you feeling?",
    # "how are you feeling",
    # "how is lizbot",
    # "how is lizbot?",
    # "how's lizbot",
    # "how's lizbot?",
    # ]
    # for cmsg in checkin_msgs:

    # if cmsg in lowered:
    # checkinresp = [
    # "Good, Thanks!",
    # "I'm well! Thanks for asking!",
    # "I'm wonderful, thanks for asking!",
    # "Excellent! Thank you ^-^",
    # ]
    # return checkinresp[randint(0, 3)]

    goodbye_msgs = [
        "goodbye",
        "bye",
        "see ya",
        "later",
        "see ya later",
        "see you later",
        "bye bye",
        "byebye",
    ]
    for gbmsg in goodbye_msgs:

        if gbmsg in lowered:
            farewells = [
                "farewell Traveler!",
                "farewell!",
                "later! ^-^",
                "see ya! :3",
                "Bye!",
                "Bye now! ^-^",
                "byebye! ^-^",
            ]
            return farewells[randint(0, 6)]

    joke_in = [
        "tell me a joke",
        "joke",
        "tell a joke",
        "what's a good joke",
        "what's a good joke?",
        "know any jokes",
        "know a good joke?",
    ]
    for jini in joke_in:

        if jini in lowered:
            jokes = [
                "What do kids play when their mom is using the phone? Bored games.",
                "What do you call an ant who fights crime? A vigilANTe!",
                "Why did the teddy bear say no to dessert? Because she was stuffed.",
                "Why did the scarecrow win a Nobel prize? Because she was outstanding in her field.",
                "What kind of shoes do frogs love? Open-toad!",
                "What did the ghost call his Mum and Dad? His transparents.",
                "What was a more useful invention than the first telephone? The second telephone.",
                "What\’s a snake\’s favorite subject in school? Hiss-tory.",
                "What animal is always at a baseball game? A bat.",
            ]
            return jokes[randint(0, 8)]

    if "roll a d4" in lowered:
        return f"You rolled: {randint(1, 4)}"
    if "roll a d6" in lowered:
        return f"You rolled: {randint(1, 6)}"
    if "roll a d8" in lowered:
        return f"You rolled: {randint(1, 8)}"
    if "roll a d10" in lowered:
        return f"You rolled: {randint(1, 10)}"
    if "roll a d12" in lowered:
        return f"You rolled: {randint(1, 12)}"
    if "roll a d20" in lowered:
        return f"You rolled: {randint(1, 20)}"
    if "flip a coin" in lowered:
        coinresults = ["heads", "tails"]
        return coinresults[randint(0, 1)]
    if "give lizard a job" in lowered:
        return "🪲 Lazy little lizard laboring for luxury."
    if "hug" in lowered:
        embrace = ["*hugs*" "thank you ^-^", "*hugs* wow! ^-^", "yay, hugs! *hugs*"]
        return embrace[randint(0, 2)]
    if "pat" in lowered:
        patresp = ["Yip! :3", "Hehe! ^-^", "wow! *nuzzles ur hand*", "*gasp* yay! :3"]
        return patresp[randint(0, 4)]
    if "pet" in lowered:
        petresp = [
            "*nuzzles ur hand*",
            "*sighs contentedly*",
            "*happy creature noises*",
            "*happy lizard noises*",
        ]
        return petresp[randint(0, 3)]
    if "embarrass" in lowered:
        flustered = [
            "asdfghjkl",
            "weiouhwt",
            "qdliuvs",
            "rafkiyv argli",
            "Wahhh >.<",
            "*blushing*",
            "*is flustered*",
            "araraarar...",
            "Bweh! >.<",
        ]
        return flustered[randint(0, 8)]
    if "bite" in lowered:
        bitersp = ["owwie!", "eep!", "ah!", "bweh!"]
        return bitersp[randint(0, 3)]
    if "shake" in lowered:
        shakersp = ["@-@ wuhhh....", "ahhh...@-@", "whhyy....@-@"]
        return shakersp[randint(0, 2)]
    if "spin" in lowered:
        return "<a:spin:1123474502521724990>"
    if "meow" in lowered:
        return "meow! :3"
    if "bark" in lowered:
        dog_noises = ["woof!", "bark!", "arf!", "bow-wow."]
        return dog_noises[randint(0, 3)]
    # elif 'time' in lowered:
    # times = ['Time to get a watch!', 'I don\'t know, ask alexa 🙄', 'I can\'t read! :3']
    # return times[randint(0,2)]
    if "magic8ball" in lowered:
        ballres = [
            "Yes, definitely",
            "It is certain",
            "Without a doubt",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Yes",
            "Definitely",
            "Don’t count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
        ]
        return ballres[randint(1, 20)]
    if "command list" in lowered:
        directory = "?magic8ball\n?flip a coin\n?roll a d4, d6, d8, d10, d12, or d20\n?inspire\n?joke\n?date&time\n?localweather\n?shake\n?bite\n?embarrass\n?hug\n?pat\n?give lizard a job\n"
        return directory
    # recognize command "?inspire"
    if "inspire" in lowered:
        # function "get_quote" (arguments:message is discord message)
        quote: str = get_quote()
        print(quote)
        return quote

    if "localweather" in lowered:
        responses: str = weather.get_weather()
        print(responses)
        return responses

    if "date&time" in lowered:
        response: str = dateTime()
        print(response)
        return response

    if "shuffle" in lowered:
        initdeck(message)
        for user in usercards:
            if user["id"] == message.author.id:
                print(user["deck"])
                shuffle(user["deck"])
                print(user["deck"])
                return "The deck is shuffled."

    if "draw" in lowered:
        inversion = ""
        if randint(0, 1) == 1:
            inversion = " inverted"
        initdeck(message)
        for user in usercards:
            if user["id"] == message.author.id:
                user["hand"].append(user["deck"][0])
                user["deck"].pop(0)
                print(message.author.name)
                print(user["hand"] + inversion)
                print(user["deck"])
                return user["hand"][-1] + inversion

    if "reset deck" in lowered:
        initdeck(message)
        for user in usercards:
            if user["id"] == message.author.id:
                user["deck"] += user["hand"]
                user["hand"].clear()
                shuffle(user["deck"])
                return "Deck reset."


def initdeck(message: discord.message):
    if {"id": message.author.id} not in usercards:
        usercards.append({"id": message.author.id, "hand": [], "deck": cards})


def get_quote() -> str:
    # ask zenquotes API for random quote
    response: str = requests.get("https://zenquotes.io/api/random")
    print(response)
    # json_data is ...unsure...(argument: response as string)
    json_data = json.loads(response.text)
    # variable "quote" is variable json_data [quote] quote " -"(dash) Json_data [quote] author
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    # Print quote with author to the terminal
    return quote


def dateTime():
    print(time.ctime())
    return time.ctime()


def cum():
    return "cum"


intents = discord.Intents.default()
intents.message_content = True

client = Lizbot(intents=intents)
client.run(env.DISCORD_CLIENT_SECRET)
