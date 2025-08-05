import typing

from pydantic import BaseModel


class AgentSettings(BaseModel):
    api_key: str = ""
    imports: typing.List[str] = [
        "csv",
        "glob",
        "io",
        "json",
        "markdown",
        "numpy",
        "os",
        "pandas",
        "posixpath",
        "open",
        "builtins.open",
        "utils.safe_open",
    ]
    max_steps: int = 7
    model_id: str = "o4-mini"


class ServiceSettings(BaseModel):
    api_key: str
    bucket_id: int
    base_url: typing.Optional[str] = None
    upload_url: str = "https://upload.eyelevel.ai"
