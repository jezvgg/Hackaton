from pydantic import BaseModel, Field
from typing import Optional
import os


class OpenAPISettings(BaseModel):
    login: str
    password: str
    api_key: Optional[str]

    @staticmethod
    def from_env() -> "OpenAPISettings":
        return OpenAPISettings(
            login = os.getenv("OPEN_API_LOGIN"),
            password = os.getenv("OPEN_API_PASSWORD"),
            api_key = os.getenv("API_KEY"),
        )


    def get_upstream_request_kwargs(self) -> dict[str, object]:
        headers = {"Content-Type": "application/json"}
        kwargs: dict[str, Any] = {"headers": headers}

        if self.login and self.password:
            kwargs["auth"] = (
                self.login, 
                self.password
                )
            return kwargs

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        return kwargs