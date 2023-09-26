import time
from lib.base_classes.routine import Routine
from models.coin_links import CoinSocialMediaLinks

use_run_interval = Routine.run_interval_decorator


class SubTrackerRoutine(Routine):
    """
    SubTrackerRoutine is a routine for tracking social media subscribers of cryptocurrency coins.

    Methods:
        run: Executes the routine for tracking coin subscribers for different social media platforms.

    Private Methods:
        __get_sub_data: Retrieve social media subscriber data for each coin.
        __get_coin_subs: Retrieve subscriber counts for each platform associated with a coin.
        __get_platform_subs:  Retrieve subscriber count for a specific social media platform.
        __handle_failed_request: __handle_failed_request

    Attributes:
        __scrape: Scrapes a given website url and returns the html data.
        __fetch: Fetches JSON data from a given web API url.
        __get_twitter_user_followers_count: Retrieves follower count for a twitter user.
    """

    @use_run_interval('24 hours')
    def run(self, _):
        """
        The main routine function for running the SubTracker routine.

        Args:
            _: Placeholder for any unused arguments.

        Returns:
            None
        """
        db = self._db

        self.__scrape = self._service.scrape
        self.__fetch = self._service.fetch
        self.__get_twitter_user_followers_count = self._service.twitter.get_user_followers_count

        result = self.__get_sub_data()
        rows = self._formatter.to_sub_table_rows(result)

        db.save_subs_data(table_rows=rows)

        self._log.success()

    #
    #
    #

    def __get_sub_data(self) -> dict[str, dict[str, int]]:
        """
        Retrieve social media subscriber data for each coin.

        Returns:
            dict: A dictionary containing coin IDs and their respective subscriber counts.
        """
        db = self._db

        socials = db.get_full_table(db.models.CoinSocialMediaLinks)
        socials_dict = self._formatter.to_table_by_coin_id_index(socials)

        result = {coin_id: self.__get_coin_subs(coin_socials) for coin_id, coin_socials in socials_dict.items()}

        return result

    #
    #
    #

    def __get_coin_subs(self, coin_socials: CoinSocialMediaLinks) -> dict[str, int]:
        """
        Retrieve subscriber counts for each platform associated with a coin.

        Args:
            coin_socials (CoinSocialMediaLinks): Coin's social media links.

        Returns:
            dict: A dictionary containing platform names and their respective subscriber counts.
        """
        platforms = self._finder.get_coin_platforms(coin_socials)

        coin_subs = {}

        for platform, url in platforms.items():
            if not url:
                coin_subs[platform] = 0

            else:
                coin_subs[platform] = self.__get_platform_subs(platform, url)
                time.sleep(1)

        return coin_subs

    #
    #
    #

    def __get_platform_subs(self, platform: str, url: str, request_attempts: int = 4) -> int:
        """
        Retrieve subscriber count for a specific social media platform.

        Args:
            platform (str): The social media platform name.
            url (str): The URL of the platform's profile or page.
            request_attempts (int): The number of request attempts in case of failure.

        Returns:
            int: The subscriber count for the platform.
        """
        f = self._finder

        if platform == 'reddit':
            url_addon = 'about.json'
            reddit_url = f'{url}{"" if url.endswith("/") else "/"}{url_addon}'

            response = self.__fetch(reddit_url)

            if not response:
                return self.__handle_failed_request(platform, url, request_attempts)

            subscribers_count = response['data']['subscribers']

            return subscribers_count

        elif platform == 'twitter':
            account_name = f.extract_twitter_accountname(url)
            count = self.__get_twitter_user_followers_count(account_name)

            # if not count:
            #     return self.__handle_failed_request(platform, url, request_attempts)

            return count

        elif platform == 'telegram':
            time.sleep(1)

            soup = self.__scrape(url)

            if not soup:
                return self.__handle_failed_request(platform, url, request_attempts)

            elements = soup.find_all('div', class_='tgme_page_extra')

            for div in elements:
                extracted_subscribers = f.extract_telegram_sub_count(div.text)
                return extracted_subscribers

        elif platform == 'discord':
            soup = self.__scrape(url)

            if not soup:
                return self.__handle_failed_request(platform, url, request_attempts)

            elements = soup.find_all('meta')

            for tag in elements:
                is_valid_element = 'content' in tag.attrs and 'members' in tag['content']

                if is_valid_element:
                    return f.extract_discord_members_count(tag['content'])

        return 0

    #
    #
    #

    def __handle_failed_request(self, platform: str, url: str, attempts: int) -> int:
        """
        Handle failed platform request by retrying or returning zero after 4 attempts.

        Args:
            platform (str): The social media platform name.
            url (str): The URL of the platform's profile or page.
            attempts (int): The number of remaining retry attempts.

        Returns:
            int: The subscriber count (zero if failed).
        """
        while attempts > 0:
            time.sleep(30)
            return self.__get_platform_subs(platform, url, attempts - 1)

        self._log.warn('fetch_failure')

        return 0
