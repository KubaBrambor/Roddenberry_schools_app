import logging
import time
from typing import cast

import requests

from data_import.api.exceptions import APIRequestError, SchoolsDataError
from data_import.api.types import APIResponse, SchoolDict
from data_import.core.config import TIMEOUT, APISettings, RetrySettings

logger = logging.getLogger(__name__)


class HydraResponse:
    """
    Facilitate working with Hydra Web API responses
    """

    def __init__(self, response_json: APIResponse):
        self.raw: APIResponse = response_json

    @property
    def items(self) -> list[SchoolDict]:
        return cast(list[SchoolDict], self.raw.get("hydra:member", []))

    @property
    def next_page_url(self) -> str | None:
        view = cast(dict[str, str], self.raw.get("hydra:view", {}))
        return view.get("hydra:next")


class SchoolsAPIFetcher:
    def __init__(
        self,
        base_url: str = APISettings.API_SCHOOLS_URL,
        headers: dict[str, str] = APISettings.HEADERS,
    ):
        self.base_url: str = base_url
        self.headers: dict[str, str] = headers

    def api_request(self, params: dict[str, int]) -> APIResponse:
        """
        Helper to make API requests
        """
        delay = RetrySettings.INITIAL_DELAY
        max_retries = RetrySettings.MAX_RETRIES
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.base_url,
                    headers=self.headers,
                    params=params,
                    timeout=(TIMEOUT.CONNECT, TIMEOUT.READ),
                )
                response.raise_for_status()  # Raises HTTPError for bad status codes
                return cast(APIResponse, response.json())
            except requests.exceptions.RequestException as err:
                logger.error(
                    f"❌ API Request failed (attempt {attempt + 1}/{max_retries}): {err}"
                )
                if (attempt + 1) < max_retries:
                    logger.info(f"⏱️ Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay = min(
                        delay * 2, RetrySettings.MAX_DELAY
                    )  # exponential backoff
        raise APIRequestError(
            "API Request failed after all retries", attempts=max_retries
        )  # Raise custom exception after all retries

    def fetch_schools_page(self, page: int = 1) -> HydraResponse:
        """
        Fetch schools data from one page
        """
        params = {"page": page}

        try:
            data = self.api_request(params)
            hydra_response = HydraResponse(data)
            return hydra_response
        except APIRequestError as err:
            logging.critical(f"🚫 Fatal error fetching schools data: {err}")
            raise SchoolsDataError(str(err), page=page) from err

    def fetch_schools_segment(
        self, start_page: int, max_schools: int = APISettings.MAX_SCHOOLS_SEGMENT
    ) -> tuple[list[SchoolDict], int | None]:
        """
        Fetch a segment of schools data, up to max_schools
        Returns tuple of (schools_list, next_page_number)
        """
        schools: list[SchoolDict] = []
        current_page = start_page

        while current_page and len(schools) < max_schools:
            response = self.fetch_schools_page(page=current_page)

            # extract schools from response
            if response.items:
                new_schools = response.items
                schools.extend(new_schools)
                logger.info(
                    f"📋 Fetched {len(new_schools)} schools from page {current_page}"
                )
            else:
                logger.info(f"ℹ️ No schools found on page {current_page}")  # noqa: RUF001

            # check if page limit is reached
            if APISettings.PAGE_LIMIT and current_page >= APISettings.PAGE_LIMIT:
                current_page = None
                break

            if response.next_page_url:  # check if there are more pages in reponse
                current_page += 1
            else:  # no more pages - stopping...
                current_page = None

        logger.info(
            f"🏁 Finished fetching segment. Total schools in segment: {len(schools)}"
        )
        return schools, current_page
