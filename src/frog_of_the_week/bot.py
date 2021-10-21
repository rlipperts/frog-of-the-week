"""
Implement the functionality here (and in sub-packages).
"""
from pathlib import Path

import discord, asyncio
from datetime import datetime
from discord.ext import commands
from mfp_discord_bot import data_service



bot = commands.Bot(command_prefix='!')

bot_author_name = 'ruben'
send_weekday = 2
send_hour = 0
send_minute = 0
message_channel_id = 0000000000000  # channel ID to send images to

embed_title = 'Frosch der Woche - {scientific_name}'
introduction = 'Diese Woche ist Froschspezies Nummer {number} der Frosch der Woche!'
name_presentation = 'Ihr wissenschaftlicher Name ist {scientific_name}.'  # todo: common name
conservation_status_message = 'Auf der IUCN Roten Liste hat diese Froschspezies den Status ' \
                              '\"{conservation_status}\"'
credits = 'Bei Fragen oder Anmerkungen über mich wendet euch direkt hier an {bot_author_name} ' \
          'oder schaut euch an wie ich funktioniere: ' \
          'https://github.com/rlipperts/frog-of-the-week (ACHTUNG: Angelsächsisch).'

description_template = "{introduction} {name_presentation}\n\n{optionals}"

conservation_status_map = {
    'NOT_EVALUATED': 'Nicht ausgewertet',
    'DATA_DEFICIENT': 'Unzureichende Datengrundlage',
    'LEAST_CONCERN': 'Nicht gefährdet',
    'NEAR_THREATENED': 'Potenziell gefährdet',
    'VULNERABLE': 'Gefährdet',
    'ENDANGERED': 'Stark gefährdet',
    'CRITICALLY_ENDANGERED': 'Vom Aussterben bedroht',
    'EXTINCT_IN_THE_WILD': 'In der Natur usgestorben',
    'EXTINCT': 'Ausgestorben',
}


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


async def time_check():
    await bot.wait_until_ready()
    message_channel = bot.get_channel(message_channel_id)
    while not bot.is_closed:
        now = datetime.now()
        if now.weekday() == send_weekday and now.hour == send_hour and now.minute == send_minute:
            message = 'a'
            await message_channel.send(message)
            time = 90
        else:
            time = 1
        await asyncio.sleep(time)

def build_conservation_status_message(data: list[str]) -> str:
    if data:
        return conservation_status_message.format(
            conservation_status=conservation_status_map[data[0]])
    # no info found - return empty message
    return ''


def build_description(data: dict) -> str:
    number = data['offset']
    scientific_name = data['results'][0]['species']

    summary = data_service.get_summary(scientific_name)
    conservation_status = build_conservation_status_message(data['results'][0]['threatStatuses'])
    optionals = ''
    if summary:
        if conservation_status:
            optionals = summary + '\n\n' + conservation_status
        else:
            optionals = summary
    else:
        optionals = conservation_status

    description_without_data = \
        description_template.format(introduction=introduction, name_presentation=name_presentation,
                                    optionals=optionals).strip()
    return description_without_data.format(number=number, scientific_name=scientific_name)


def build_embed() -> discord.Embed:
    data = data_service.random_frog()
    scientific_name = data['results'][0]['species']
    common_name = data_service.german_common_name_from_data(data) or ''

    title = embed_title.format(scientific_name=scientific_name)
    description = build_description(data)
    image_url = data_service.frog_image_url(scientific_name)

    embed = discord.Embed(title=title, description=description, color=0x6ea75a)
    embed.set_image(url=image_url)
    return embed


# @bot.event
# async def on_message(message):
#     if message.content.startswith('!hello'):
#         embed = discord.Embed(title=embed_title, description="Desc", color=0x00ff00)
#         embed.add_field(name="Field1", value="hi", inline=False)
#         embed.add_field(name="Field2", value="hi2", inline=False)
#         await message.channel.send(embed=embed)


# bot.loop.create_task(time_check())
# bot.run('token')

# data = data_service.random_frog()
# print(data)
# name = data['results'][0]['species']
# description = build_description(data)
# print(description)
# print(data_service.frog_image_url(name))
