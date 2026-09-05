from pydantic import BaseModel, Field

class ClientInfo(BaseModel):
    ip_address: str | None
    user_agent: str | None
    

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit  