"""
Implement the functionality here (and in sub-packages).
"""
import asyncio
from datetime import datetime

import discord
from discord.ext import commands, tasks
from frog_of_the_week import data_service

BOT = commands.Bot(command_prefix='!')

BOT_AUTHOR_NAME = 'Ruben'
TEST_MODE = True
SEND_WEEKDAY = 2
MESSAGE_CHANNEL_ID = 886275343411982378
TEST_MESSAGE_CHANNEL_ID = 869956823740993587

EMBED_TITLE = 'Frosch der Woche - {name}'
INTRODUCTION = 'Diese Woche ist Froschspezies Nummer {number} der Frosch der Woche!'
NAME_PRESENTATION = 'Ihr wissenschaftlicher Name ist {scientific_name}.'
CONSERVATION_STATUS_MESSAGE = 'Auf der IUCN Roten Liste hat diese Froschspezies den Status ' \
                              '\"{conservation_status}\"'
CREDITS = 'Bei Fragen oder Anmerkungen über mich wendet euch direkt hier an {bot_author_name} ' \
          'oder schaut euch an wie ich funktioniere:' \
          '\ngithub.com/rlipperts/frog-of-the-week\n(ACHTUNG: Angelsächsisch).'

DESCRIPTION_TEMPLATE = "{introduction} {name_presentation}\n\n{optionals}"

CONSERVATION_STATUS_MAP = {
    'NOT_EVALUATED': 'Nicht ausgewertet',
    'DATA_DEFICIENT': 'Unzureichende Datengrundlage',
    'LEAST_CONCERN': 'Nicht gefährdet',
    'NEAR_THREATENED': 'Potenziell gefährdet',
    'VULNERABLE': 'Gefährdet',
    'ENDANGERED': 'Stark gefährdet',
    'CRITICALLY_ENDANGERED': 'Vom Aussterben bedroht',
    'EXTINCT_IN_THE_WILD': 'In der Natur ausgestorben',
    'EXTINCT': 'Ausgestorben',
}


def build_conservation_status_message(data: list[str]) -> str:
    """
    Builds a string describing the conservation status of the species.
    :param data: Data containing conservation status information
    :return: Description of the conservation status (or empty if no data)
    """
    if data:
        return CONSERVATION_STATUS_MESSAGE.format(
            conservation_status=CONSERVATION_STATUS_MAP[data[0]])
    # no info found - return empty message
    return ''


def build_description(data: dict) -> str:
    """
    Builds a string consisting of an introduction, species description and conservation status.
    :param data: Frog data as provided by the data service
    :return: Description string
    """
    number = data['offset']
    scientific_name = data['results'][0]['species']

    # manage optional information
    summary = data_service.german_summary(scientific_name)
    conservation_status = build_conservation_status_message(data['results'][0]['threatStatuses'])
    if summary:
        if conservation_status:
            optionals = summary + '\n\n' + conservation_status
        else:
            optionals = summary
    else:
        optionals = conservation_status

    # merge the description elements
    description_without_data = \
        DESCRIPTION_TEMPLATE.format(introduction=INTRODUCTION, name_presentation=NAME_PRESENTATION,
                                    optionals=optionals).strip()
    return description_without_data.format(number=number, scientific_name=scientific_name)


def build_embed() -> discord.Embed:
    """
    Creates a discord.Embed message that contains information on a random frog.
    :return: The message
    """
    # todo: create a frog_data class and build it in the data service so we dont have to handle
    #  api-specific stuff here
    data = data_service.random_frog()
    scientific_name = data['results'][0]['species']
    # todo: somehow we never have a common name here, might be because of missing data
    common_name = data_service.german_common_name_from_data(data)

    title = EMBED_TITLE.format(name=common_name or scientific_name)
    description = build_description(data)
    image_url = data_service.frog_image_url(scientific_name)
    footer = CREDITS.format(bot_author_name=BOT_AUTHOR_NAME)

    embed = discord.Embed(title=title, description=description, color=0x6ea75a)
    embed.set_image(url=image_url)
    embed.set_footer(text=footer)
    return embed


@BOT.event
async def on_ready():
    """
    Discord interface function that is called when the bot successfully connected to a server.
    Starts the weekly loop upon connection.
    """
    print("Logged in as")
    print(BOT.user.name)
    print("------")
    weekly_loop.start()


# Loop weekly
@tasks.loop(hours=24 * 7)
# @tasks.loop(minutes=1)
async def weekly_loop():
    """
    Weekly repeated loop that sends the frog-of-the-week message.
    """
    print('in loop routine')
    channel_id = TEST_MESSAGE_CHANNEL_ID if TEST_MODE else MESSAGE_CHANNEL_ID
    message_channel = BOT.get_channel(channel_id)
    await message_channel.send(embed=build_embed())


# Align weekday
@weekly_loop.before_loop
async def before_weekly_loop():
    """
    Routine that is called before the loop. Aligns the loop on the wednesday weekday by checking
    once per our if it is wednesday and, if not, continuing to do so.
    """
    print('in before loop routine')
    if not TEST_MODE:  # when in test_mode directly start the loop
        for _ in range(24 * 7):  # loop the whole week
            if datetime.now().weekday() == SEND_WEEKDAY:  # check if it is the current weekday
                return
            await asyncio.sleep(60 * 60)  # wait an hour before looping again


def run():
    """
    Executes the discord bot.
    """
    print('starting the bot...')
    BOT.run(data_service.KEYS['discord_bot_token'])
