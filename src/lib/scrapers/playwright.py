from asyncio import create_task, as_completed
from typing import Callable, Awaitable, Coroutine, Any, Iterable, Dict, Union
from user_agent import generate_user_agent
from playwright.async_api._generated import Page, Browser
from playwright.async_api import async_playwright

from playwright.sync_api import sync_playwright
from functools import wraps

from .create_pw_headers import create_pw_headers


class Playwright:
    """
    Playwright utility class for web scraping with Playwright.

    This class provides methods for setting up Playwright, creating contexts, pages, and scraping data.

    Attributes:
        browser (Browser): An instance of the Playwright browser.
        queue (dict[str, Any]): A dictionary for managing queued tasks.

    Methods:
        __init__: Initializes a Playwright instance with a browser.
        use_sync_playwright: Decorator to use Playwright in a synchronous manner.
        use_async_playwright: Decorator to use Playwright in an asynchronous manner.
        create_context: Creates a new Playwright context with configurations.
        new_page: Creates a new Playwright page in the current context.
        scrape: Scrapes data using a provided job callback.
        create_tasks: Creates and runs asynchronous tasks for scraping multiple jobs concurrently.
        get_cookie_async: Retrieves a cookie asynchronously from a given URL.

    Example Usage:
        playwright = Playwright(browser)
        data = await playwright.scrape(job_callback)
    """

    def __init__(self, browser: Browser) -> None:
        '''
        Initialize a Scraper instance.

        Args:
            browser: An instance of the Playwright browser.
        '''
        self.__browser: Browser = browser
        self.__queue: dict = {}

    #
    #
    #

    @staticmethod
    def use_sync_playwright(func: Callable) -> Callable:
        """
        Decorator to use Playwright in a synchronous manner.

        This decorator creates a synchronous Playwright environment and launches a context manager for a Chromium browser to execute the decorated function synchronously.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function.

        Example Usage:
            @use_sync_playwright
            def my_sync_function(context, *args, **kwargs):
                Synchronous Playwright code here...
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            with sync_playwright() as p:
                headers: Dict[str, Any] = create_pw_headers()
                user_agent = generate_user_agent()

                browser = p.chromium.launch()
                context = browser.new_context(
                    **headers,
                    user_agent=user_agent,
                )

                result = func(context, *args, **kwargs)

                browser.close()

            return result

        return wrapper

    #
    #
    #

    @staticmethod
    def use_async_playwright(func: Callable) -> Callable:
        """
        Decorator to use Playwright in an asynchronous manner.

        This decorator creates an asynchronous Playwright environment and launches a context manager for a Chromium browser to execute the decorated function asynchronously.

        Args:
            func (Callable): The asynchronous function to be decorated.

        Returns:
            Callable: The decorated asynchronous function.

        Example Usage:
            @use_async_playwright
            async def my_async_function(*args, **kwargs, context=None):
                Asynchronous Playwright code here...
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_playwright() as pw:
                headers: Dict[str, Any] = create_pw_headers()
                user_agent = generate_user_agent()

                browser = await pw.chromium.launch()
                context = await browser.new_context(
                    **headers,
                    user_agent=user_agent,
                )

                result = await func(*args, **kwargs, context=context)

                await browser.close()

            return result

        return wrapper

    #
    #
    #

    async def create_context(self) -> None:
        '''
        Create a new Playwright context. And set it up with configurations

        Raises:
            PlaywrightError: If there is an error creating the context.
        '''
        headers: Dict[str, Any] = create_pw_headers()
        user_agent = generate_user_agent()
        self.context = await self.__browser.new_context(
            **headers,
            user_agent=user_agent,
        )

    #
    #
    #

    async def new_page(self) -> Page:
        '''
        Create a new Playwright page in the current context.

        Returns:
            Page: A new Playwright Page object which represents a new tab in
            the browser.

        Raises:
            PlaywrightError: If there is an error creating the page.
        '''
        page: Page = await self.context.new_page()
        page.set_default_navigation_timeout(60000)
        page.set_default_timeout(60000)

        return page

    #
    #
    #

    async def scrape(
        self,
        job_callback: Callable[[Callable[[], Awaitable[Page]]], Awaitable[str]],
    ) -> str:
        '''
        Scrape data using a provided job_callback.

        Returns:
            str: Scraping result returned by the job_callback.

        Raises:
            PlaywrightError: If there is an error during scraping.
        '''
        await self.create_context()
        data: str = await job_callback(self.new_page)
        await self.context.close()

        return data

    #
    #
    #

    async def create_tasks(
        self,
        jobs: Iterable[Callable[..., Coroutine[Any, Any, Any]]],
    ) -> None:
        '''
        Create and run asynchronous tasks for scraping multiple jobs
        concurrently.

        This method takes a list of job functions (coroutines) and creates
        tasks for each job.

        Raises:
            PlaywrightError: If there is an error during scraping.
        '''
        tasks: Iterable[Awaitable[Any]] = [create_task(self.scrape(job)) for job in jobs]

        for future in as_completed(tasks):
            await future

    #
    #
    #

    @staticmethod
    @use_async_playwright
    async def get_cookie_async(url: str, cookies_accept_element: Union[str, None] = None, context={}) -> str:
        """
        Get a cookie asynchronously from a given URL.

        Args:
            url (str): The URL to visit and retrieve cookies from.
            cookies_accept_element (Union[str, None], optional): Selector for the element to click for accepting cookies, if applicable (default: None).
            context (dict, optional): Additional context parameters (default: {}).

        Returns:
            str: The retrieved cookie value.

        Raises:
            PlaywrightError: If there is an error during the cookie retrieval process.
        """
        page = await context.new_page()
        await page.goto(url)

        if cookies_accept_element:
            await page.click(cookies_accept_element)

        cookies = await context.cookies()
        cookie = cookies[3]['value']

        return cookie
