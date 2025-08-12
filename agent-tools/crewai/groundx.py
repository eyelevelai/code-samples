import time, typing
from pydantic import BaseModel, Field, PrivateAttr

from crewai.tools import BaseTool  # type: ignore[index]
from groundx import GroundX, SearchResponse


# Example usage:
# from groundx import GroundXTool
# gx = GroundXTool(api_key=GROUNDX_API_KEY, bucket_id=GROUNDX_BUCKET_ID)


class GroundXToolInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "Keyword-based query to retrieve content from a RAG database.\n"
            "Use exact keywords expected to be present explicitly in the searchable data.\n"
            "To limit the search to a particular file, explicitly reference the filename in your query (e.g., 'payments.csv issuing_country transactions')."
            "Adjust the 'n' parameter to retrieve more content if needed (maximum 100)."
        ),
    )
    n: typing.Optional[int] = Field(
        default=None,
        description=("Number of results to retrieve (default 50, maximum 100)."),
    )


class GroundXTool(BaseTool):
    name: str = "groundx_retriever"
    description: str = (
        "Uses keyword search to retrieve relevant content from a RAG database.\n"
        "Your query should include explicit keywords likely to appear verbatim in the searchable content.\n"
        "If you need to restrict the results to a specific file, explicitly include the filename (e.g., 'payments.csv') within your query keywords.\n"
        "Adjust the 'n' parameter to retrieve more content if needed (maximum 100)."
    )
    args_schema: typing.Type[BaseModel] = GroundXToolInput
    _bucket_id: int = PrivateAttr()
    _client: GroundX = PrivateAttr()

    def __init__(
        self,
        api_key: str,  # GroundX API key
        bucket_id: int,  # GroundX bucket ID
    ):
        super().__init__()  # type: ignore[index]

        self._bucket_id = bucket_id
        self._client = GroundX(api_key=api_key)

    def _run(self, query: str, n: int = 50) -> str:
        print(f"query\n\t[{query}]")
        assert isinstance(query, str), "Your search query must be a string"

        if n > 100:
            n = 100

        retrievals: typing.Optional[SearchResponse] = None
        for _ in range(3):
            try:
                retrievals = self._client.search.content(
                    id=self._bucket_id,
                    query=query,
                    n=n,
                    relevance=0,
                    verbosity=0,
                    request_options={
                        "additional_headers": {"Accept-Encoding": "gzip"},
                        "timeout_in_seconds": 60,
                    },
                )
                if retrievals.search.results is None:
                    print(f"\tgx\t[{query}]\tresults [{retrievals.search.count}]")
                else:
                    print(
                        f"\tgx\t[{query}]\tresults [{len(retrievals.search.results)}]"
                    )
                break
            except Exception as e:
                print(e)
                print(type(e))
                time.sleep(5)

        if retrievals is None:
            raise Exception("retrievals is None")

        return f"\nRetrieved Documents:\n\n===\n{str(retrievals.search.text)}\n===\n"
