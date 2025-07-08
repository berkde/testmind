from llama_index.core.workflow import Event
from pydantic import Field

from .schemas import RequestSchema, Transition


class GenerateEvent(Event):
    """
    Event to trigger the initial generation flow from raw input text.

    This event is created when the workflow setup is complete and the system
    is ready to process the user's raw input. It serves as the entry point
    for the main processing pipeline, carrying the unprocessed user input
    to the next workflow step.

    Attributes:
        input (str): The raw user input provided by the user that needs to be
                     processed and structured for matrix generation.

    Example:
        >>> event = GenerateEvent(
        ...     input="Create a test matrix for user login with admin and guest roles"
        ... )

    Note:
        This event is typically created in the setup step after receiving
        the StartEvent and is passed to the collect_user_input step for
        further processing and validation.
    """
    input: str = Field(..., description="Raw user input to be processed for test matrix generation")


class MatrixEvent(Event):
    """
    Event that wraps structured input used for matrix generation.

    This event is created after the raw user input has been processed and
    validated. It contains the structured data (transitions and personas)
    that will be used to generate the test matrix. This event ensures
    that all required data is properly formatted before matrix generation.

    Attributes:
        request_input (RequestSchema): Structured input containing validated
                                       transitions and personas data ready for
                                       matrix generation.

    Example:
        >>> event = MatrixEvent(
        ...     request_input=RequestSchema(
        ...         transitions=[Transition(
        ...             from_state="login",
        ...             to_state="dashboard",
        ...             essential_for="admin",
        ...             optional_for="guest"
        ...         )],
        ...         personas=["admin", "guest"]
        ...     )
        ... )

    Note:
        This event is created after successful validation of user input
        and contains the structured data that will be passed to the
        matrix generation step.
    """
    request_input: RequestSchema = Field(..., description="Structured input containing transitions and personas for matrix generation")


class MatrixAnswerEvent(Event):
    """
    Event that holds the generated matrix and its explanation.

    This event is created after the test matrix has been successfully
    generated. It contains both the structured matrix data and a natural
    language explanation of the results. This event serves as the output
    from the matrix generation step and input to the validation step.

    Attributes:
        matrix_data (dict): Generated matrix structure mapping personas to
                            transitions with their respective statuses and
                            test case identifiers.
        explanation (str): LLM-generated explanation of the matrix that
                           describes the test coverage and rationale.

    Example:
        >>> event = MatrixAnswerEvent(
        ...     matrix_data={"login->dashboard": {"admin": {"status": "Essential", "id": "G1"}}},
        ...     explanation="Matrix generated with 3 essential test cases for admin access"
        ... )

    Note:
        This event contains the core output of the matrix generation process
        and will be used by the report agent to create final recommendations
        and validation feedback.
    """
    matrix_data: dict = Field(..., description="Generated test matrix mapping transitions to personas with status and test IDs")
    explanation: str = Field(..., description="Natural language explanation of the generated test matrix")


class ProgressEvent(Event):
    """
    Event used to emit progress updates to the frontend or logs.

    This event is used throughout the workflow to provide real-time
    feedback about the current processing status. It helps users and
    developers understand what step is currently being executed and
    provides transparency into the workflow's progress.

    Attributes:
        msg (str): A descriptive message describing the current workflow
                   state, action being performed, or status update.

    Example:
        >>> event = ProgressEvent(
        ...     msg="Processing user input and extracting transitions..."
        ... )

    Note:
        These events are streamed to provide real-time feedback and
        can be used by the frontend to show progress indicators or
        by logging systems to track workflow execution.
    """
    msg: str = Field(..., description="Progress message describing current workflow state or action")


class ErrorEvent(Event):
    """
    Event triggered when a user input or system error prevents the workflow from continuing.

    This event is used to gracefully handle issues encountered during processing,
    such as missing or invalid input. Instead of raising an exception that halts
    the entire workflow, this event provides a structured way to communicate
    the issue back to the user or frontend system.

    Attributes:
        message (str): A descriptive and actionable error message that explains
                       what went wrong and optionally guides the user on how to fix it.

    Example:
        >>> event = ErrorEvent(
        ...     message="Missing transitions. Please describe at least one state change."
        ... )

    Note:
        This event is typically returned from a workflow step when validation fails
        or required information is missing. It enables the UI or chatbot to respond
        gracefully, keeping the interaction open and user-friendly.
    """
    message: str = Field(..., description="A descriptive error message to inform the user of the issue.")

