import cyclopts
import httpx
import pydantic_settings
from pydantic import AnyUrl
from rich import console


class Settings(pydantic_settings.BaseSettings):
    skillventory_url: AnyUrl = "http://localhost:8080"


settings = Settings()
console = console.Console()

app = cyclopts.App(help="CLI tool to interact with a skillventory API")


@app.command(name="get")
def get_skill(*, url: AnyUrl = settings.skillventory_url, name: str) -> None:
    """Command that retrieves a skill from the API

    Args:
        url: URL of the skillventory API
        name: Name of the skill to retrieve
    """
    with console.status("Retriving data...", spinner="bouncingBar"):
        response = httpx.get(f"{url}v1/skills/name/{name}")
        response.raise_for_status()
        skill = response.json()
        console.print(f"Skill: {skill["skill_name"]}\nLevel of confidence: {skill["level_of_confidence"]}")


def cli():
    app()


if __name__ == "__main__":
    cli()
