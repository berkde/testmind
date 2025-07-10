from typing import Dict, List, Tuple, Annotated, Literal, Optional
from pydantic import BaseModel, StringConstraints


class Transition(BaseModel):
    from_state: Annotated[str, StringConstraints(min_length=3, max_length=255)]
    to_state: Annotated[str, StringConstraints(min_length=3, max_length=255)]
    essential_for: Annotated[str, StringConstraints(min_length=2, max_length=255)]
    optional_for: Annotated[str, StringConstraints(min_length=2, max_length=255)]


class RequestSchema(BaseModel):
    """
    Request schema used to receive request payload from web client apps.

    Attributes:
        transitions (List[Transition]): List of state transitions.
        personas (List[str]): List of persona names.
    """

    transitions: Annotated[
        List[Transition],
        StringConstraints(min_length=1)
    ]
    personas: Annotated[
        list[Annotated[str, StringConstraints(min_length=2, max_length=255)]],
        StringConstraints(min_length=1)
    ]


class ResponseSchema(BaseModel):
    """
    Response schema for web client apps.

    Attributes:
        status: Indicates whether the LLM was able to generate a useful response.
        llm_text_response: Natural language response (may explain the issue if failed).
        generated_matrix: Optional tuple of metadata and rows (only present if status == 'success').
                          matrix: Dict[transition_key, Dict[persona, Dict[status, id?]]]
                          test_ids: List[Dict[id, transition, by]]
        reason: Explanation code for why the response failed (optional).
        suggestions: Optional list of next-step suggestions for the user.
    """

    status: Literal["success", "unsatisfied"]
    llm_text_response: Annotated[str, StringConstraints(min_length=1)]
    generated_matrix: Optional[
        Tuple[
            Dict[str, Dict[str, Dict[str, str]]],
            List[Dict[str, str]]
        ]
    ] = None
    reason: Optional[Literal["low_confidence", "off_topic", "unanswerable"]] = None
    suggestions: Optional[List[Annotated[str, StringConstraints(min_length=1)]]] = None


class BaseError(BaseModel):
    """Base schema for error payloads.

    Attributes:
        status: int       (e.g 400, 500)
        error_type: str   (e.g., 'invalid_persona', 'invalid_transition')
        message: str
    """
    status: Literal["error"] = "error"
    error_type: str
    message: str


class PersonaError(BaseError):
    error_type: Literal["invalid_persona"] = "invalid_persona"


class TransitionError(BaseError):
    error_type: Literal["invalid_transition"] = "invalid_transition"


class LLMUnsatisfiedError(BaseModel):
    """
    Schema returned when the LLM cannot confidently answer a user query.

    Attributes:
        message: Informational message explaining the issue.
        suggestions: Optional list of fallback suggestions or actions.
    """
    message: Annotated[str, StringConstraints(min_length=5, max_length=1024)]
    suggestions: Annotated[
        List[Annotated[str, StringConstraints(min_length=1)]],
        StringConstraints(min_length=0)
    ] = []


class UserInputSchema(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1)]
