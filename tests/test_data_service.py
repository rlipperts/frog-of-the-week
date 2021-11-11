"""
Tests of the data service which handles various APIs
These are not exhausting and do not handle every possible case, don't hate me for it.
"""
import requests  # type: ignore

from frog_of_the_week import data_service


def test_get_certain_frog():
    """
    Tests the basic api query's ability to return a specific frog.
    """
    data = data_service.get_frog_for_number(0)
    assert data['results'][0]['order'] == 'Anura'
    assert data['results'][0]['speciesKey'] == 2421431


def test_get_random_frog():
    """
    Tests the basic api query's ability to return random frogs.
    If you are veeeeeeeeery unlucky this test might fail due to twice getting the same frog.
    """
    data = data_service.random_frog()
    data2 = data_service.random_frog()
    assert data['results'][0]['speciesKey'] != data2['results'][0]['speciesKey']


def test_translate_to_german():
    """
    Test deepl translation function.
    """
    assert data_service.translate_to_german('Bread') == 'Brot'


def test_german_common_name():
    """
    Tests translation of the common name using the deepl API.
    """
    german_name = data_service.german_common_name_from_data(
        {'vernacularNames': [{'vernacularName': 'Bread', 'language': 'eng'}]})
    assert german_name == 'Brot'


def test_german_common_name_returns_empty_string_if_no_names():
    """
    Tests that there are no errors in absence of a common name.
    """
    assert data_service.german_common_name_from_data({}) == ''


def test_image_search_returns_image_url():
    """
    Tests that the image search function actually returns an url containing an image.
    """
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    url = data_service.frog_image_url('Bread')
    response = requests.head(url)
    assert response.headers["content-type"] in image_formats


def test_wikipedia_summary():
    """
    Test if the wikipedia summary function returns a string consisting of multiple words.
    """
    summary = data_service.wikipedia_summary('Bread')
    assert summary
    assert len(summary.split()) > 1


def test_german_summary_if_german_article():
    """
    Test if the german wikipedia summary function returns a string consisting of multiple words if
    there is a german wikipedia article for the search query.
    """
    summary = data_service.german_summary('Brot')
    assert summary
    assert len(summary.split()) > 1


def test_german_summary_if_no_german_article():
    """
    Test if the german wikipedia summary function returns a string consisting of multiple words if
    there is no german wikipedia article for the search query.
    """
    summary = data_service.german_summary('Wheat')
    assert summary
    assert len(summary.split()) > 1
