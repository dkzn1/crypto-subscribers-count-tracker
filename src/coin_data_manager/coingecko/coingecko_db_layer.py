from datetime import datetime, timedelta
from typing import Any, Union
from sqlalchemy.orm import Session

from lib.base_classes.db_access_layer import DBAccessLayer

from models.coin_base_data import CoinBaseData
from models.coingecko_ratings import CoingeckoRatings
from models.unprocessed_coingecko_links import UnprocessedCoingeckoLinks

use_session = DBAccessLayer.use_session


class CoingeckoDBLayer(DBAccessLayer):
    """
    Database CRUD operations class for saving Coingecko-related data to the database.

    This class provides methods to interact with a database, including saving stablecoins, base data, market data,
    extended toplist data, Coingecko ratings, unprocessed links, and coin homepages.

    Methods:
        save_stablecoins: Save stablecoin data to the database.
        save_base_data: Save base coin data to the database.
        save_market_data: Save market data to the database.
        save_extended_toplist_data: Save extended toplist data to the database.
        save_coin_homepages: Save coin homepages to the database.

    Example Usage:
        db_operations = CoingeckoDBOperations()
        db_operations.save_stablecoins(stablecoins_data)
    """

    @use_session
    def save_stablecoins(self, stablecoins_data: list[dict[str, str]], session={}) -> None:
        """
        Save stablecoin data to the database.

        Args:
            stablecoins_data (list[dict[str, str]]): A list of stablecoin data dictionaries.
            session (Session, optional): An optional SQLAlchemy session. Defaults to an empty session, which is assigned by the decorator.

        Returns:
            None
        """
        Stablecoin = self.models.Stablecoin

        response = session.query(Stablecoin).all()

        stablecoin_ids: list[str] = [stablecoin.coin_id for stablecoin in response]

        for row_data in stablecoins_data:
            if row_data["coin_id"] in stablecoin_ids:
                continue

            session.add(Stablecoin(**row_data))

    #
    #
    #

    @use_session
    def save_base_data(self, coins_base_data: list[dict[str, str]], session={}) -> None:
        """
        Save base coin data to the database. Or update the existing data after 14 days.

        Args:
            coins_base_data (list[dict[str, str]]): A list of base coin data dictionaries.
            session (Session, optional): An optional SQLAlchemy session. Defaults to an empty session, which is assigned by the decorator.

        Returns:
            None
        """
        CoinBaseData = self.models.CoinBaseData

        existing_data = self.get_full_table(CoinBaseData)

        existing_data_dict = {coin.coin_id: coin for coin in existing_data}

        for coin_row in coins_base_data:
            coin_id = coin_row["coin_id"]
            new_coin = coin_id not in existing_data_dict

            if new_coin:
                session.add(CoinBaseData(**coin_row))

            else:
                existing_coin = existing_data_dict[coin_id]

                current_date = datetime.now()
                two_weeks = timedelta(days=14)

                update_after_2_weeks = current_date - existing_coin.date > two_weeks

                if not update_after_2_weeks:
                    continue

                for key, value in coin_row.items():
                    setattr(existing_coin, key, value)

    #
    #
    #

    @use_session
    def save_market_data(self, coins_market_data: list[dict[str, Union[str, int, float]]], session={}) -> None:
        """
        Save market data to the database.

        Args:
            coins_market_data (list[dict[str, Union[str, int, float]]]): A list of market data dictionaries.
            session (Session, optional): An optional SQLAlchemy session. Defaults to an empty session, which is assigned by the decorator.

        Returns:
            None
        """
        CoinMarketData = self.models.CoinMarketData

        existing_data = session.query(CoinMarketData).all()

        existing_data_dict = {coin.coin_id: coin for coin in existing_data}

        for coin_row in coins_market_data:
            coin_id = coin_row['coin_id']

            if coin_id in existing_data_dict:
                existing_coin = existing_data_dict[coin_id]

                for key, value in coin_row.items():
                    setattr(existing_coin, key, value)

            else:
                new_coin = CoinMarketData(**coin_row)
                session.add(new_coin)

    #
    #
    #

    @use_session
    def save_extended_toplist_data(self, extended_data: list[dict[str, Any]], session={}) -> None:
        """
        Save extended toplist data to the database.

        Args:
            extended_data (list[dict[str, Any]]): A list of extended toplist data dictionaries.
            session (Session, optional): An optional SQLAlchemy session. Defaults to an empty session, which is assigned by the decorator.

        Returns:
            None
        """
        m = self.models

        existing_base_data = session.query(m.CoinBaseData).all()
        existing_ratings = session.query(m.CoingeckoRatings).all()
        existing_unprocessed_links = session.query(m.UnprocessedCoingeckoLinks).all()

        for coin_row in extended_data:
            self.__save_categories(existing_base_data, coin_row['categories'])
            self.__save_coingecko_ratings(session, existing_ratings, coin_row['ratings'])
            self.__save_unprocessed_links(session, existing_unprocessed_links, coin_row['unprocessed_links'])

    #
    #
    #

    @staticmethod
    def __save_categories(existing_base_data: list[CoinBaseData], new_categories: dict[str, Any]) -> None:
        """
        Private helper method to save coin categories.

        Args:
            existing_base_data (list[CoinBaseData]): A list of existing base coin data.
            new_categories (dict[str, Any]): A dictionary of new categories data.

        Returns:
            None
        """
        existing_base_data_dict = {coin.coin_id: coin for coin in existing_base_data}

        coin_id = new_categories['coin_id']
        existing_coin = existing_base_data_dict[coin_id]

        if coin_id in existing_base_data_dict and not existing_coin.categories:
            setattr(existing_coin, 'categories', new_categories['categories'])

    #
    #
    #

    def __save_coingecko_ratings(self, session: Session, existing_ratings: list[CoingeckoRatings], new_ratings: dict[str, Any]) -> None:
        """
        Private helper method to save Coingecko ratings.

        Args:
            session (Session): SQLAlchemy session object.
            existing_ratings (list[CoingeckoRatings]): A list of existing Coingecko ratings data.
            new_ratings (dict[str, Any]): A dictionary of new Coingecko ratings data.

        Returns:
            None
        """
        existing_ratings_dict = {coin.coin_id: coin for coin in existing_ratings}

        coin_id = new_ratings['coin_id']

        if coin_id in existing_ratings_dict:
            existing_coin = existing_ratings_dict[coin_id]

            for key, value in new_ratings.items():
                if key != 'coin_id':
                    setattr(existing_coin, key, value)

        else:
            new_coin = self.models.CoingeckoRatings(**new_ratings)
            session.add(new_coin)

    #
    #
    #

    def __save_unprocessed_links(self, session: Session, existing_unprocessed_links: list[UnprocessedCoingeckoLinks], new_unprocessed_links: dict[str, Any]) -> None:
        """
        Private helper method to save unprocessed links.

        Args:
            session (Session): SQLAlchemy session object.
            existing_unprocessed_links (list[UnprocessedCoingeckoLinks]): A list of existing unprocessed links data.
            new_unprocessed_links (dict[str, Any]): A dictionary of new unprocessed links data.

        Returns:
            None
        """
        existing_unprocessed_links_dict = {coin.coin_id: coin for coin in existing_unprocessed_links}

        coin_id = new_unprocessed_links['coin_id']

        if coin_id not in existing_unprocessed_links_dict:
            new_row = self.models.UnprocessedCoingeckoLinks(**new_unprocessed_links)
            session.add(new_row)

    #
    #
    #

    @use_session
    def save_coin_homepages(self, coin_homepages: list[dict[str, Any]], session={}) -> None:
        """
        Save coin homepages to the database.

        Args:
            coin_homepages (list[dict[str, Any]]): A list of coin homepage data dictionaries.
            session (Session, optional): An optional SQLAlchemy session. Defaults to an empty session, which is assigned by the decorator.

        Returns:
            None
        """
        for coin_row in coin_homepages:
            new_coin = self.models.CoinHomepageLink(**coin_row)
            session.add(new_coin)
