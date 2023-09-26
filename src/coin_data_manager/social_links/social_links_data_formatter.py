from lib.base_classes.processors.data_formatter import DataFormatter


class SocialLinksDataFormatter(DataFormatter):
    """
    Data formatter class to support social links service operations with utility functions for data formatting.

    Methods:
        format_links_update: Formats social media links for update in the database.
        format_platform_url: Formats the platform URL.
    """

    @staticmethod
    #
    def format_links_update(links):
        """
        Formats social media links for update in the database.

        Args:
            links: Social media links.

        Returns:
            list: A list of dictionaries containing formatted links.
        """
        formatted_links = [{'coin_id': key, **value} for key, value in links.items()]

        return formatted_links

    #
    #
    #

    @staticmethod
    #
    def format_platform_url(platform: str, url: str) -> str:
        """
        Formats the platform URL.

        Args:
            platform (str): The social media platform.
            url (str): The URL to be formatted.

        Returns:
            str: The formatted URL.
        """
        if platform == 'telegram':
            return url.replace('/s/', '/')

        if platform == 'reddit' and not url.endswith('/'):
            return url + '/'

        return url
