from pydantic import BaseModel


class PersonaError(BaseModel):
    """
    Error payload for invalid persona input.

    Attributes:
        message (str): Human-readable error message.
        status (str): Error status identifier, usually set to "error".
    """
    message: str
    status: str = "error"


class TransitionError(BaseModel):
    """
    Error payload for invalid transition input.

    Attributes:
        message (str): Human-readable error message.
        status (str): Error status identifier, usually set to "error".
    """
    message: str
    status: str = "error"
