"""
Implement the functionality here (and in sub-packages).
"""
import discord, asyncio
from datetime import datetime
from discord.ext import commands, tasks
from frog_of_the_week import data_service


bot = commands.Bot(command_prefix='!')

bot_author_name = 'Ruben'
test_mode = True
send_weekday = 2
message_channel_id = 886275343411982378
test_message_channel_id = 869956823740993587

embed_title = 'Frosch der Woche - {name}'
introduction = 'Diese Woche ist Froschspezies Nummer {number} der Frosch der Woche!'
name_presentation = 'Ihr wissenschaftlicher Name ist {scientific_name}.'
conservation_status_message = 'Auf der IUCN Roten Liste hat diese Froschspezies den Status ' \
                              '\"{conservation_status}\"'
credits = 'Bei Fragen oder Anmerkungen über mich wendet euch direkt hier an {bot_author_name} ' \
          'oder schaut euch an wie ich funktioniere:' \
          '\ngithub.com/rlipperts/frog-of-the-week\n(ACHTUNG: Angelsächsisch).'

description_template = "{introduction} {name_presentation}\n\n{optionals}"

conservation_status_map = {
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
    if data:
        return conservation_status_message.format(
            conservation_status=conservation_status_map[data[0]])
    # no info found - return empty message
    return ''


def build_description(data: dict) -> str:
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
        description_template.format(introduction=introduction, name_presentation=name_presentation,
                                    optionals=optionals).strip()
    return description_without_data.format(number=number, scientific_name=scientific_name)


def build_embed() -> discord.Embed:
    # todo: create a frog_data class and build it in the data service so we dont have to handle
    #  api-specific stuff here
    data = data_service.random_frog()
    scientific_name = data['results'][0]['species']
    # todo: somehow we never have a common name here, might be because of missing data
    common_name = data_service.german_common_name_from_data(data)

    title = embed_title.format(name=common_name or scientific_name)
    description = build_description(data)
    image_url = data_service.frog_image_url(scientific_name)
    footer = credits.format(bot_author_name=bot_author_name)

    embed = discord.Embed(title=title, description=description, color=0x6ea75a)
    embed.set_image(url=image_url)
    embed.set_footer(text=footer)
    return embed


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("------")
    weekly_loop.start()


# Loop weekly
# @tasks.loop(hours = 24 * 7)
@tasks.loop(minutes = 1)
async def weekly_loop():
    print('in loop routine')
    channel_id = test_message_channel_id if test_mode else message_channel_id
    message_channel = bot.get_channel(channel_id)
    await message_channel.send(embed=build_embed())


# Align weekday
@weekly_loop.before_loop
async def before_weekly_loop():
    print('in before loop routine')
    if not test_mode:  # when in test_mode directly start the loop
        for _ in range(24 * 7):  # loop the whole week
            if datetime.now().weekday() == send_weekday:  # check if it is the current weekday
                return
            await asyncio.sleep(60 * 60)  # wait an hour before looping again


def run():
    print('starting the bot...')
    bot.run(data_service.keys['discord_bot_token'])
