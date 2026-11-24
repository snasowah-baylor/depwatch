from dataclasses import dataclass


@dataclass(frozen=True)
class UserFacingError:
    message: str
    status_code: int = 400
