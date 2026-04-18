from pydantic import BaseModel, Field


class WebServerSettings(BaseModel):
    host: str
    port: int

    @staticmethod
    def from_env() -> "WebServerSettings":
        return WebServerSettings(
            host = os.getenv("HOST", "0.0.0.0"),
            port = int(os.getenv("PORT", "8003"))
        )
    