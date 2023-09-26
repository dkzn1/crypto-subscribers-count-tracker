from asyncio import run, gather

from db.db import db_singleton as db
from lib.twitter_api import twitter_api_singleton as twitter_api

from coin_data_manager.coingecko.coingecko_coordinator import CoingeckoCoordinator
from coin_data_manager.social_links.social_links_coordinator import SocialLinksCoordinator
from coin_subscribers_monitor.subscribers_monitor_coordinator import SubscribersMonitorCoordinator

from lib.scrapers.requests_handler import RequestsHandler
from lib.scrapers.generate_requests_headers import generate_requests_headers
from lib.scrapers.headers_config import referers


async def main() -> None:
    #
    req = RequestsHandler(generate_requests_headers, referers)

    coingecko = CoingeckoCoordinator(db, req.fetch_json, req.scrape_url)
    social_links = SocialLinksCoordinator(db, req.scrape_url)
    subscribers_monitor = SubscribersMonitorCoordinator(db, twitter_api, req.scrape_url, req.fetch_json)

    tasks = [coingecko.run_service(), social_links.run_service(), subscribers_monitor.run_service()]

    await gather(*tasks)


if __name__ == "__main__":
    run(main())
