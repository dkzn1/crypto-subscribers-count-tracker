from sqlalchemy import create_engine

from models.base import Base
from models.coin_base_data import CoinBaseData
from models.coin_market_data import CoinMarketData
from models.coin_links import CoinSocialMediaLinks, CoinHomepageLink, CoinGithubLink
from models.coingecko_ratings import CoingeckoRatings
from models.stablecoin import Stablecoin
from models.unprocessed_coingecko_links import UnprocessedCoingeckoLinks
from models.coin_social_media_subs import CoinSocialMediaSubs
from models.coin_subscriber_trends import CoinSubscriberTrends
from models.log_entry import LogEntry


class DatabaseModels:
    """
    A container class for database model references.
    """

    def __init__(self) -> None:
        self.CoinBaseData = CoinBaseData
        self.CoinMarketData = CoinMarketData
        self.CoinSocialMediaLinks = CoinSocialMediaLinks
        self.CoinHomepageLink = CoinHomepageLink
        self.CoinGithubLink = CoinGithubLink
        self.Stablecoin = Stablecoin
        self.CoingeckoRatings = CoingeckoRatings
        self.UnprocessedCoingeckoLinks = UnprocessedCoingeckoLinks
        self.CoinSocialMediaSubs = CoinSocialMediaSubs
        self.CoinSubscriberTrends = CoinSubscriberTrends
        self.LogEntry = LogEntry


#


class Database:
    """
    Manages the SQLite database connection and provides access to database model classes.

    Attributes:
        engine (SQLAlchemy.engine): The SQLAlchemy database engine for SQLite.
        models (__DatabaseModels): An instance of the container class for database model references.

    Usage:
        To create an instance of the `Database` class and access database models, use the `db_singleton` object.
    """

    __sqlite_db_path: str = '/data/database.db'

    def __init__(self) -> None:
        """
        Initialize the Database Class

        Initializes the database connection and creates an instance of the `__DatabaseModels` class for accessing model classes.
        """
        self.__engine = create_engine(f'sqlite://{self.__sqlite_db_path}', echo=False)

        self.__models = DatabaseModels()

        Base.metadata.create_all(bind=self.engine)

    @property
    def engine(self):
        """Getter for the database engine."""
        return self.__engine

    @property
    def models(self):
        """Getter for the database models."""
        return self.__models


db_singleton = Database()
