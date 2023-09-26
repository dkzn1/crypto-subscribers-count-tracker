from lib.base_classes.config import Config


class SocialLinksConfig(Config):
    """
    Configuration settings needed for Social Links service operations.
    """

    @staticmethod
    #
    def create_google_search_url(coin_id: str, platform: str) -> str:
        """
        Create a google search query url for a given coin ID and platform.

        Args:
            coin_id (str): The ID of the coin.
            platform (str): The platform to search on.

        Returns:
            str: Google URL.
        """
        services = {'telegram': 'telegram+channel', 'discord': 'discord+server', 'twitter': 'twitter', 'reddit': 'reddit', 'github': 'github'}

        search_query = f'{coin_id}+{services[platform]}'

        return f'https://www.google.com/search?q={search_query}'

    #
    #
    #

    # Root urls for social media platforms
    service_base_url: dict[str, list[str]] = {'telegram': ['t.me/s', 'telegram.me'], 'discord': ['discord.com/invite/', 'discordapp.com/invite/'], 'twitter': ['https://twitter.com/'], 'reddit': ['https://www.reddit.com/r/'], 'github': ['https://github.com/']}
