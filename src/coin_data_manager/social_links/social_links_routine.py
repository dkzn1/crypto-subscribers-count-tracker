from typing import Any, Union, Callable
import time
from bs4 import BeautifulSoup

from lib.base_classes.routine import Routine


use_run_interval = Routine.run_interval_decorator


class SocialLinksRoutine(Routine):
    """
    Social Links Routine for scraping and updating social media links of coins.

    This routine scrapes and updates social media links for coins, completing missing links and validating existing ones.

    Methods:
        run: Executes the routine, scraping and updating social media links.

    Private Methods:
        __scrape_missing_links: Scrapes and updates missing social media links for coins.
        __find_social_media_links: Finds social media links on a coin's homepage.
        __google_search_link: Performs a Google search for a specific platform link.
        __rescrape_link: Retries a scraping job in case of failure.

    Attributes:
        __scrape: A Callable function for scraping data from a URL.
    """

    @use_run_interval('2 days')
    def run(self, _):
        """
        Execute the routine to scrape and update social media links.

        Args:
            _: Placeholder argument (not used).
        """
        self.__scrape = self._service.scrape
        db = self._db

        social_links_table = db.models.CoinSocialMediaLinks

        existing_links = db.get_full_table(social_links_table)
        existing_links_dict = self._formatter.to_table_by_coin_id_index(existing_links)

        unprocessed_socials = db.get_full_table(db.models.UnprocessedCoingeckoLinks)

        new_links = self._finder.extract_new_links(existing_links_dict, unprocessed_socials)

        complete_links = self.__scrape_missing_links(new_links)

        db.save_table_data(table=social_links_table, table_rows=complete_links)

        self._log.success()

    #
    #
    #

    def __scrape_missing_links(self, new_links: dict[str, dict[str, str]], rescrape_attempts: int = 4) -> list[dict]:
        """
        Scrapes and updates missing social media links for coins.

        Args:
            new_links (dict[str, dict[str, str]]): A dictionary of new social media links.
            rescrape_attempts (int): The number of rescrape attempts in case of scraping failure (default: 4).

        Returns:
            list[dict]: A list of updated social media links.
        """
        existing_homepages = self._db.get_full_table(self._db.models.CoinHomepageLink)

        existing_homepages_index = self._formatter.to_table_by_coin_id_index(existing_homepages)

        result_links = new_links
        for coin_id, coin_links in new_links.items():
            homepage = existing_homepages_index[coin_id].homepage_url if coin_id in existing_homepages_index else None

            if not homepage:
                continue

            soup = self.__scrape(homepage)

            if not soup:
                error_msg = f'Failed to scrape {coin_id} homepage: {homepage}'

                return self.__rescrape_link(job=self.__scrape_missing_links, job_params=[new_links], attempts=rescrape_attempts, error_msg=error_msg, return_val=[])

            updated_links = self.__find_social_media_links(coin_id, soup, coin_links)

            result_links[coin_id] = updated_links

        return self._formatter.format_links_update(result_links)

    #
    #
    #

    def __find_social_media_links(self, coin_id: str, soup: BeautifulSoup, coin_links: dict[str, Any]) -> dict[str, str]:
        """
        Finds social media links on a coin's homepage.

        Args:
            coin_id (str): The ID of the coin.
            soup (BeautifulSoup): A BeautifulSoup object representing the coin's homepage.
            coin_links (dict[str, Any]): A dictionary of coin's social media links.

        Returns:
            dict[str, str]: A dictionary of updated social media links.
        """
        updated_coin_links = coin_links
        del updated_coin_links['homepage']
        del updated_coin_links['github']

        for platform in updated_coin_links.keys():
            result = self._finder.extract_platform_url(soup, platform) if soup else None

            if result:
                updated_coin_links[platform] = result

            missing_link = not updated_coin_links[platform] or len(updated_coin_links[platform]) == 0

            invalid_link = True if missing_link else self._validator.validate_platform_url(platform, updated_coin_links[platform])

            if missing_link or invalid_link:
                search_result = self.__google_search_link(coin_id, platform)
                updated_coin_links[platform] = search_result

            updated_coin_links[platform] = self._formatter.format_platform_url(platform, updated_coin_links[platform])

        return updated_coin_links

    #
    #
    #

    def __google_search_link(self, coin_id: str, platform: str, rescrape_attempts: int = 4) -> Union[list[str], str]:
        """
        Performs a Google search for a specific platform link.

        Args:
            coin_id (str): The ID of the coin.
            platform (str): The social media platform to search for.
            rescrape_attempts (int): The number of rescrape attempts (default: 4).

        Returns:
            Union[list[str], str]: A list of search results (if found) or an empty string.
        """
        cfg = self._config

        url = cfg.create_google_search_url(coin_id, platform)

        soup = self.__scrape(url)

        time.sleep(1)

        error_msg = f'Failed to scrape google links for: {coin_id}, {platform}'

        if not soup:
            return self.__rescrape_link(job=self.__google_search_link, job_params=[coin_id, platform], attempts=rescrape_attempts, error_msg=error_msg, return_val='')

        search_results = soup.find('div', id='rso')

        if not search_results:
            return self.__rescrape_link(job=self.__google_search_link, job_params=[coin_id, platform], attempts=rescrape_attempts, error_msg=error_msg, return_val='')

        for a in search_results.find_all('a'):
            href = a.get('href', '').lower()

            if self._validator.validate_match(cfg.service_base_url[platform], href):
                return href

        return ''

    #
    #
    #

    def __rescrape_link(self, job: Callable, job_params: list[Any], attempts: int, error_msg: str, return_val: Any):
        """
        Retries a scraping job in case of failure.

        Args:
            job (Callable): The job function to be retried.
            job_params (list[Any]): List of job function parameters.
            attempts (int): The number of retry attempts.
            error_msg (str): Error message to log in case of repeated failure.
            return_val (Any): Default return value.

        Returns:
            Any: The result of the job function or the default return value.
        """
        time.sleep(1)
        if attempts > 0:
            return job(*job_params, attempts - 1)

        self._log.error(error_msg)

        return return_val
