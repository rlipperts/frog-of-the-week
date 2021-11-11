"""
Module that provides data by interfacing various APIs.
This should probably be separated into a module for each low level API function and another one for
the higher-level data interface used by the bot.
"""

import random
import requests  # type: ignore
import wikipedia  # type: ignore
from google_images_search import GoogleImagesSearch  # type: ignore
from deepl import Translator  # type: ignore

from frog_of_the_week.exceptions import MissingApiKeyError
from frog_of_the_week.util import load_keys


KEYS = load_keys()
GET_A_FROG_API_CALL = \
    'https://api.gbif.org/v1/species/search/?highertaxon_key=952&limit=1&rank=SPECIES&offset='


def get_frog_for_number(number: int):
    """
    Returns frog data from the GBIF species API.
    :param number: Number of the species to query the API with
    :return: Data package received
    """
    return requests.get(GET_A_FROG_API_CALL + str(number)).json()


def random_frog():
    """
    Returns frog data from the GBIF species API for a random frog species.
    :return: Data package received
    """
    number_of_frogs = get_frog_for_number(0)['count']
    number_to_draw = random.randint(0, number_of_frogs - 1)
    chosen_frog = get_frog_for_number(number_to_draw)
    return chosen_frog


def translate_to_german(text: str) -> str:
    """
    Translates text to german using the Deepl API.
    :param text: String to translate
    :return: Translated text
    """
    try:
        translator = Translator(KEYS['deepl_auth_key'])
        translated = translator.translate_text(text, target_lang="DE")
        return translated.text
    except KeyError as error:
        raise MissingApiKeyError('Missing Deepl API Key!') from error


def german_common_name_from_data(data: dict) -> str:
    """
    Tries to find a common german species name.
    :param data: Data package containing species information
    :return: German common species name
    """
    names = data.get('vernacularNames', None)
    if names:
        print('found a name for this frog, translating it')
        name = names[0]['vernacularName']
        return translate_to_german(name)
    return ''


def frog_image_url(query: str) -> str:
    """
    Queries the google image search to get an image for the desired search term.
    :param query: Search term to use
    :return: Url of first image found
    """
    # this returns wrong images for whatever reason
    # try:
    #     wikipedia.set_lang('en')
    #     page = wikipedia.page(query, auto_suggest=False)
    #     return page.images.pop(0)
    # except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError, IndexError):
    #     pass
    try:
        gis = GoogleImagesSearch(KEYS['google_api_key'], KEYS['google_search_engine_id'])
        params = {
            'q': '\"' + query + '\"',
            'num': 1,
            'safe': 'high',
        }
        gis.search(search_params=params)
        return next(iter(gis.results())).url
    except KeyError as error:
        raise MissingApiKeyError(
            'Could not find required google API key or search engine id') from error


def wikipedia_summary(query: str, lang: str = 'en') -> str:
    """
    Searches wikipedia for a summary of given search term.
    :param query: Search term
    :param lang: Language of wikipedia pages to search
    :return: Summary string (empty if nothing found)
    """
    try:
        wikipedia.set_lang(lang)
        return wikipedia.summary(query, auto_suggest=False)
    # no page found
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        return ''


def german_summary(query: str) -> str:
    """
    Tries to obtain a short german description of given term.
    :param query: Search term
    :return: Summary string (empty if nothing found)
    """
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
