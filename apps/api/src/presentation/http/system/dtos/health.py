from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Response body for health check.
    """

    status: str = Field(
        description="Status of the system",
        examples=["ok"],
    )
    uptime: str = Field(
        description="Uptime of the system",
        examples=["1h"],
    )
