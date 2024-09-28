from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True,
    )


class ApplicationSchema(_BaseModel):
    ...
