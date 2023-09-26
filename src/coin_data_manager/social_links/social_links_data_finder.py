from typing import Union
import json
from bs4 import BeautifulSoup

from lib.base_classes.processors.data_finder import DataFinder
from models.unprocessed_coingecko_links import UnprocessedCoingeckoLinks
from models.coin_links import CoinSocialMediaLinks


class SocialLinksDataFinder(DataFinder):
    """
    Data finder class to support social links service operations with utility functions for data searching and extracting.

    Methods:
        extract_new_links: Extracts new social media links from unprocessed coin data.
        extract_platform_url: Extracts the platform URL from BeautifulSoup.

    Private Methods:
        __extract_links: Extracts social media links from unprocessed data.
    """

    def extract_new_links(self, existing_social_links: dict[str, CoinSocialMediaLinks], unprocessed_socials: list[UnprocessedCoingeckoLinks]) -> dict[str, dict[str, str]]:
        """
        Extract new social media links from unprocessed coin data.

        Args:
            existing_social_links (dict[str, CoinSocialMediaLinks]): Dictionary of existing social media links.
            unprocessed_socials (list[UnprocessedCoingeckoLinks]): List of unprocessed social media data.

        Returns:
            dict: A dictionary containing new links.
        """
        result = {coin_socials.coin_id: self.__extract_links(coin_socials) for coin_socials in unprocessed_socials if coin_socials.coin_id not in existing_social_links}

        return result

    #
    #
    #

    @staticmethod
    #
    def extract_platform_url(soup: BeautifulSoup, platform: str) -> Union[str, list[str], bool]:
        """
        Extracts the platform URL from BeautifulSoup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the coin's homepage.
            platform (str): The social media platform.

        Returns:
            Union[str, list[str], bool]: The extracted URL(s) or False if not found.
        """
        for a in soup.find_all('a'):
            href = a.get('href', '').lower()

            if platform in href:
                return href if platform != 'github' else [href]

        return False

    #
    #
    #

    @staticmethod
    #
    def __extract_links(coin_socials: UnprocessedCoingeckoLinks) -> dict[str, str]:
        """
        Extracts social media links from unprocessed data.

        Args:
            coin_socials (UnprocessedCoingeckoLinks): Unprocessed social media data.

        Returns:
            dict: A dictionary containing extracted links.
        """
        if not coin_socials.links:
            return {}

        links = json.loads(coin_socials.links)

        formatted_links = {**links}

        formatted_links['github'] = links['repos_url']['github']
        formatted_links['reddit'] = links['subreddit_url']

        for item in ['telegram', 'discord', 'twitter']:
            formatted_links[item] = ''

        for item in formatted_links['chat_url']:
            if 'discord.com/invite' in item or 'discordapp.com/invite' in item:
                formatted_links['discord'] = item
                break

        for item in ['repos_url', 'telegram_channel_identifier', 'subreddit_url', 'chat_url']:
            del formatted_links[item]

        return formatted_links
