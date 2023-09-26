import requests
import json
from typing import Optional, Union, Callable, List
from bs4 import BeautifulSoup
from lib.logger import Logger


class RequestsHandler:
    '''
    Handler for fetch and scrape requests using Requests library,
    parses the respinse accordingly.
    '''

    def __init__(self, generate_headers: Callable, referers: List) -> None:
        '''Initialize the RequestsHandler with default headers.'''
        self.__headers = generate_headers(referers)
        self.__referers = referers
        self.__generate_headers = generate_headers
        self.__log = Logger(name=self.__class__.__name__)

    #
    #
    #

    def change_headers(self) -> None:
        '''Change the headers for subsequent requests.'''
        self.__headers = self.__generate_headers(self.__referers)

    #
    #
    #

    def set_cookies(self, cookies) -> None:
        '''Add cookies to the headers.'''
        self.__headers['Cookie'] = cookies

    #
    #
    #

    def __get_response(self, url: str) -> Optional[requests.Response]:
        '''
        Send a GET request to a URL.

        Args:
            url (str): The URL to send the request to.

        Returns:
            requests.Response: The response object from the request.

        '''
        try:
            response = requests.get(url, headers=self.__headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as err:
            self.__log.error(err)

            return None

    #
    #
    #

    def scrape_url(self, url: str) -> Optional[BeautifulSoup]:
        '''
        Scrape the HTML content of a URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the parsed HTML.

        '''

        response = self.__get_response(url)
        if response:
            return self.__parse_html(response)

        return None

    #
    #
    #

    def fetch_json(self, url: str) -> Optional[list]:
        '''
        Fetch JSON data from a URL.

        Args:
            url (str): The URL to fetch JSON data from.

        Returns:
            dict: A dictionary representing the parsed JSON data.

        '''
        response = self.__get_response(url)
        if response:
            return self.__parse_json(response)

        return None

    #
    #
    #

    def __parse_html(self, response) -> Optional[BeautifulSoup]:
        '''
        Parse the HTML content using BeautifulSoup.

        Args:
            response (requests.Response): The response object to parse.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the parsed HTML.

        '''
        try:
            soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
            return soup

        except Exception as err:
            self.__log.error(err)
            return None

    #
    #
    #

    def __parse_json(self, response) -> Optional[list]:
        '''
        Parse JSON data from the response.

        Args:
            response (requests.Response): The response object to parse.

        Returns:
            dict: A dictionary representing the parsed JSON data.

        '''
        try:
            json_data: Union[list, None] = json.loads(response.content.decode('utf-8'))

            return json_data

        except (json.JSONDecodeError, ValueError) as err:
            self.__log.error(err)
            return None
