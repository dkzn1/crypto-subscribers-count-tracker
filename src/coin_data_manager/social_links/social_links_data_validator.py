from lib.base_classes.processors.data_validator import DataValidator


class SocialLinksDataValidator(DataValidator):
    """
    Data validator class to support social links service operations with utility functions for data validation.

    Methods:
        validate_platform_url: Validates a social media link.
        validate_match: Checks if a given term matches in the href.

    Private Methods:
        __remove_domain_prefixes: Removes domain prefixes from URLs.
    """

    def validate_platform_url(self, domain: str, link: str) -> bool:
        """
        Validates a social media link.

        Args:
            domain (str): The social media platform.
            link (str): The link to be validated.

        Returns:
            bool: True if the link is valid, False otherwise.
        """
        if not link or domain == 'github':
            return False

        domain_base_links = {'reddit': 'https://www.reddit.com', 'telegram': 'https://www.telegram.com', 'discord': 'https://discord.com', 'twitter': 'https://twitter.com'}

        clean_base_link = self.__remove_domain_prefixes(domain_base_links[domain])

        clean_link = self.__remove_domain_prefixes(link)

        return len(clean_base_link) >= len(clean_link)

    #
    #
    #

    @staticmethod
    #
    def validate_match(base_url: str, href: str) -> bool:
        """
        Checks if a given term matches in the href.

        Args:
            base_url (str): The base URL.
            href (str): The href to be checked.

        Returns:
            bool: True if the term is found in the href, False otherwise.
        """
        for term in base_url:
            if term in href:
                return True

        return False

    #
    #
    #

    @staticmethod
    #
    def __remove_domain_prefixes(dom: str) -> str:
        """
        Removes domain prefixes from URLs.

        Args:
            dom (str): The URL with domain prefixes.

        Returns:
            str: The cleaned URL.
        """
        protocols = ['http://', 'https://', 'www.', '/']

        clean_domain = dom
        for protocol in protocols:
            clean_domain = clean_domain.replace(protocol, '')

        return clean_domain
