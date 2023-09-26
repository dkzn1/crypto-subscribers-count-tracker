# import tweepy
# from dotenv import load_dotenv
# import os

# from lib.logger import Logger

# load_dotenv()


class TwitterAPI:
    """
    A class for interacting with the Twitter API.

    Attributes:
        api (tweepy.API): A Tweepy API instance for making Twitter API requests.
    """

    def __init__(self) -> None:
        """
        Initialize the TwitterAPI class.

        Reads Twitter API credentials from environment variables and
        sets up authentication using Tweepy.
        """

        # =================================
        # Disabled for the demo version, because Twitter API tokens are needed to function.
        # =================================

        # consumer_key = os.getenv("CONSUMER_KEY")
        # consumer_secret = os.getenv("CONSUMER_SECRET")
        # access_token = os.getenv("ACCESS_TOKEN")
        # access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)

        # self.__api = tweepy.API(auth)
        # self.__log = Logger(name=self.__class__.__name__)

    #
    #
    #

    def get_user_followers_count(self, account_name: str) -> int:
        """
        Get the number of followers for a Twitter user.

        Args:
            account_name (str): The Twitter handle (username) of the user.

        Returns:
            int: The number of followers of the user.
        """

        # Disabled for the demo version
        return 0

        # try:
        #     user = self.__api.get_user(screen_name=account_name)

        #     followers_count = user.followers_count

        #     return followers_count

        # except Exception as e:
        #     self.__log.error(e)

        #     return 0


twitter_api_singleton = TwitterAPI()
