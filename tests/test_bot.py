"""
Tests of the discord bot functionality
"""
from frog_of_the_week import bot


def test_embed():
    """
    Test if the bot builds a correct embed
    Todo: This should mock the data service to only test the embed building function!
    """
    embed = bot.build_embed()
    assert embed.description
    assert embed.image
