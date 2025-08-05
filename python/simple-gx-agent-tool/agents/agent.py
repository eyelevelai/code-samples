import typing
from PIL.Image import Image

from smolagents import Tool, ToolCallingAgent
from smolagents.models import OpenAIServerModel

from config import agent_settings
from settings import AgentSettings


class Agent(ToolCallingAgent):
    def __init__(
        self,
        settings: AgentSettings = agent_settings,
        name: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        tools: typing.Optional[typing.List[Tool]] = None,
        verbosity: typing.Optional[int] = 0,
    ):
        if tools is None:
            tools = []

        model = OpenAIServerModel(settings.model_id)

        super().__init__(  # type: ignore
            name=name,
            description=description,
            tools=tools,
            model=model,
            max_steps=settings.max_steps,
            verbosity_level=verbosity,
        )

    def process(
        self,
        prompt: str,
        images: typing.Optional[typing.List[Image]] = None,
    ) -> typing.Any:
        return super().run(  # type: ignore
            prompt,
            images=images,
        )
