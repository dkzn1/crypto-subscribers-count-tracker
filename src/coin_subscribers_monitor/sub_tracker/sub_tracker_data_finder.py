import re
from typing import Union

from lib.base_classes.processors.data_finder import DataFinder

from models.coin_links import CoinSocialMediaLinks


class SubTrackerDataFinder(DataFinder):
    """
    DataFinder class that provides ulitity methods for finding or extracting purposes for the SubTrackerRoutine.

    Methods:
        get_coin_platforms: Extract social media platform URLs for a coin.
        extract_discord_members_count: Extract the number of members from a Discord server description.
        extract_twitter_accountname: Extract the Twitter account name from a Twitter URL.
    """

    @staticmethod
    #
    def get_coin_platforms(coin_socials: CoinSocialMediaLinks) -> dict[str, Union[str, None]]:
        """
        Extract social media platform URLs for a coin.

        Args:
            coin_socials (CoinSocialMediaLinks): Coin's social media links.

        Returns:
            dict: A dictionary containing platform names and their respective URLs.
        """
        return {'reddit': coin_socials.reddit, 'twitter': coin_socials.twitter, 'telegram': coin_socials.telegram, 'discord': coin_socials.discord}

    #
    #
    #

    @staticmethod
    #
    def extract_discord_members_count(input_string: str) -> int:
        """
        Extract the number of members from a Discord server description.

        Args:
            input_string (str): The input string containing server information.

        Returns:
            int: The number of members.
        """
        pattern_1 = r'(\d+) members'
        pattern_2 = r'(\d+) other members'

        match_1 = re.search(pattern_1, input_string)
        if match_1:
            return int(match_1.group(1))

        match_2 = re.search(pattern_2, input_string)
        if match_2:
            return int(match_2.group(1))

        return 0

    #
    #
    #

    @staticmethod
    #
    def extract_telegram_sub_count(input_string: str) -> int:
        """
        Extract the number of subscribers from a Telegram channel description.

        Args:
            input_string (str): The input string containing server information.

        Returns:
            int: The number of members.
        """
        formatted_str = input_string.replace(' ', '')

        match = re.search(r'^\d+', formatted_str)

        if match:
            return int(match.group(0))

        return int(formatted_str)

    #
    #
    #

    @staticmethod
    #
    def extract_twitter_accountname(url: str) -> Union[str, None]:
        """
        Extract the Twitter account name from a Twitter URL.

        Args:
            url (str): The Twitter URL.

        Returns:
            Union[str, None]: The Twitter account name or None if not found.
        """
        pattern = r"https://twitter\.com/([A-Za-z0-9_]+)"

        match = re.search(pattern, url)

        if match:
            account_name = match.group(1)
            return account_name
        else:
            return None
