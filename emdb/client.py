from emdb.exceptions import EMDBInvalidIDError, EMDBNotFoundError, EMDBAPIError
from emdb.models.entry import EMDBEntry
from emdb.models.search import EMDBSearchResults
from emdb.utils import make_request


class EMDBClient:
    """
    High-level EMDB API client.

    Usage:
        client = EMDBClient()
        entry = client.get_entry("EMD-1234")
    """

    def get_entry(self, emdb_id: str) -> EMDBEntry:
        """
        Retrieve an EMDB entry by its ID.

        :param emdb_id: The EMDB ID of the entry to retrieve.
        :return: A dictionary containing the EMDB entry data.
        :raises EMDBNotFoundError: If the entry is not found.
        :raises EMDBInvalidIDError: If the provided EMDB ID is invalid.
        :raises EMDBAPIError: For other API-related errors.
        """
        if not emdb_id.startswith("EMD-"):
            raise EMDBInvalidIDError(emdb_id)

        endpoint = f"/entry/{emdb_id}"
        try:
            data = make_request(endpoint)
            return EMDBEntry.from_api(data, self)
        except EMDBNotFoundError as e:
            raise e
        except Exception as e:
            raise EMDBAPIError(f"Failed to retrieve entry {emdb_id}: {str(e)}")

    def search(self, query: str) -> "EMDBSearchResults":
        """
        Search for EMDB entries using a query string.

        :param query: The search query string.
        :return: An EMDBSearchResults object containing the search results.
        :raises EMDBAPIError: For API-related errors.
        """
        endpoint = f"/search/{query}"
        params = {
            "rows": 1000000,
            "fl": "emdb_id",
            "wt": "csv",
            "download": "false"
        }
        try:
            data = make_request(endpoint, params=params, restype="csv")
            return EMDBSearchResults.from_api(data, self)
        except Exception as e:
            raise EMDBAPIError(f"Search failed: {str(e)}")

