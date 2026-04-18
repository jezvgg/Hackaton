from pydantic import BaseModel, Field


class OpenAPISettings(BaseModel):
    login: str
    password: str
    api_key: str

    @staticmethod
    def from_env() -> "OpenAPISettings":
        return OpenAPISettings(
            login = os.getenv("OPEN_API_LOGIN"),
            password = os.getenv("OPEN_API_PASSWORD"),
            api_key = os.getenv("API_KEY"),
        )