from pydantic import BaseModel, field_validator


class CleanBaseModel(BaseModel):

    @field_validator("*", mode="before")
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            v = v.strip()
            return v if v != "" else None
        return v
