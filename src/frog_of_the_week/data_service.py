"""
Module that provides data by interfacing various APIs.
This should probably be separated into a module for each low level API function and another one for
the higher-level data interface used by the bot.
"""
from pathlib import Path

import random
import requests
import wikipedia
import json
from google_images_search import GoogleImagesSearch
from deepl import Translator

from frog_of_the_week.exceptions import MissingApiKeyError


def load_keys(path: Path):
    with open(path, mode='r') as file:
        return json.load(file)


keys = load_keys(Path('data/keys.json'))
get_a_frog_api_call = \
    'https://api.gbif.org/v1/species/search/?highertaxon_key=952&limit=1&rank=SPECIES&offset='


def get_frog_for_number(number: int):
    return requests.get(get_a_frog_api_call + str(number)).json()


def random_frog():
    number_of_frogs = get_frog_for_number(0)['count']
    number_to_draw = random.randint(0, number_of_frogs - 1)
    chosen_frog = get_frog_for_number(number_to_draw)
    return chosen_frog


def translate_to_german(text: str) -> str:
    try:
        translator = Translator(keys['deepl_auth_key'])
        translated = translator.translate_text(text, target_lang="DE")
        return translated.text
    except KeyError as e:
        raise MissingApiKeyError('Missing Deepl API Key!') from e


def german_common_name_from_data(data: dict) -> str:
    names = data.get('vernacularNames', None)
    if names:
        name = names[0]['vernacularName']
        try:
            return translate_to_german(name)
        except KeyError:
            pass
    return ''


def frog_image_url(query: str) -> str:
    try:
        gis = GoogleImagesSearch(keys['google_api_key'], keys['google_search_engine_id'])
        params = {
            'q': '\"' + query + '\"',
            'num': 1,
            'safe': 'high',
        }
        gis.search(search_params=params)
        return next(iter(gis.results())).url
    except KeyError as e:
        raise MissingApiKeyError(
            'Could not find required google API key or search engine id') from e


def wikipedia_summary(query: str, lang: str = 'en'):
    try:
        wikipedia.set_lang(lang)
        return wikipedia.summary(query, auto_suggest=False)
    # no page found
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        return ''


def german_summary(query: str) -> str:
    # try to get the summary from a german wikipedia article
    summary = wikipedia_summary(query, 'de')
    if not summary:
        # get the summary from an english wikipedia article
        summary = wikipedia_summary(query)
        # translate it if it exists
        if summary:
            summary = translate_to_german(summary)
    # return the summary if it exists, else return empty string
    return summary or ''
