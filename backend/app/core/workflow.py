from ..models.event import (
    GenerateEvent,
    MatrixEvent,
    MatrixAnswerEvent,
    ProgressEvent,
    ErrorEvent)
from llama_index.core.workflow import (
    Context,
    StartEvent,
    StopEvent,
    Workflow,
    step
)

import re
import json

from ..models.schemas import RequestSchema

from logging import getLogger

logger = getLogger(__name__)


class TestMindWorkflow(Workflow):
    """
    A workflow to process user input and generate a test matrix using multiple agents.

    Attributes:
        question_agent: The agent responsible for interpreting user input and extracting context.
        answer_agent: The agent responsible for generating the test matrix.
        report_agent: The agent responsible for validating and summarizing the result.
    """

    def __init__(self, timeout=300):
        super().__init__(timeout=timeout)
        self.report_agent = None
        self.answer_agent = None
        self.question_agent = None

    def __repr__(self):
        return f'<TestMindWorkflow timeout={self._timeout}>'

    @step
    async def setup(self, ctx: Context, ev: StartEvent) -> GenerateEvent:
        self.question_agent = ev.question_agent
        self.answer_agent = ev.answer_agent
        self.report_agent = ev.report_agent

        ctx.write_event_to_stream(ProgressEvent(msg="Initializing TestMind system..."))
        return GenerateEvent(input=ev.input)

    @step
    async def collect_user_input(self, ctx: Context, ev: GenerateEvent) -> MatrixEvent | ErrorEvent:
        """
        Processes the input string using the question agent to extract transitions and personas.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (GenerateEvent): The event containing raw input data.

        Returns:
            MatrixEvent if input is valid, otherwise ErrorEvent.
        """
        logger.info(f'Collecting user input: {ev.input}')
        ctx.write_event_to_stream(ProgressEvent(msg="Processing validated input for matrix generation..."))
        logger.info("Processing validated input for matrix generation...")

        result = await self.question_agent.achat(ev.input)

        if hasattr(result, 'response'):
            logger.info(f"Response content: {result.response}")
        if hasattr(result, 'raw'):
            logger.info(f"Raw content: {result.raw}")

        response_text = str(result)
        logger.info(f"Parsing response text: {response_text}")

        transitions = []
        personas = []

        if ("**Transitions:**" in response_text and "**Personas:**" in response_text) or ("Transitions:" in response_text and "Personas:" in response_text):
            if "**Personas:**" in response_text:
                personas_section = response_text.split("**Personas:**")[1].split("\n")
            else:
                personas_section = response_text.split("Personas:")[1].split("\n")
                
            for line in personas_section:
                line = line.strip()
                if line.startswith("- ") or line.startswith("* "):
                    persona = line[2:].strip()
                    if persona and persona not in personas:
                        personas.append(persona)
                elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. "):
                    persona = line[3:].strip()
                    if persona and persona not in personas:
                        personas.append(persona)
                elif line and not line.startswith("**") and not line.startswith("Transitions:"):
                    persona = line.strip()
                    if persona and persona not in personas and len(persona) > 0:
                        personas.append(persona)

            if "**Transitions:**" in response_text:
                transitions_section = response_text.split("**Transitions:**")[1].split("**Personas:**")[0]
            else:
                transitions_section = response_text.split("Transitions:")[1].split("Personas:")[0]
                
            for line in transitions_section.split("\n"):
                line = line.strip()
                if ("from:" in line and "to:" in line and "essential_for:" in line) or ("From:" in line and "To:" in line and "Essential for:" in line):
                    parts = line.split(",")
                    transition = {}
                    for part in parts:
                        part = part.strip()
                        if "from:" in part or "From:" in part:
                            key = "from:" if "from:" in part else "From:"
                            transition["from_state"] = part.split(key)[1].strip()
                        elif "to:" in part or "To:" in part:
                            key = "to:" if "to:" in part else "To:"
                            transition["to_state"] = part.split(key)[1].strip()
                        elif "essential_for:" in part or "Essential for:" in part:
                            key = "essential_for:" if "essential_for:" in part else "Essential for:"
                            transition["essential_for"] = part.split(key)[1].strip()
                        elif "optional_for:" in part or "Optional for:" in part:
                            key = "optional_for:" if "optional_for:" in part else "Optional for:"
                            transition["optional_for"] = part.split(key)[1].strip()
                    
                    if len(transition) >= 4:
                        transitions.append(transition)

        logger.info(f"Parsed transitions: {transitions}")
        logger.info(f"Parsed personas: {personas}")

        if not result or not transitions or not personas:
            logger.error('Invalid agent response or parsing failed')
            return ErrorEvent(message='TestMind was unable to interpret your request, Try rephrasing.')

        if len(transitions) < 1 or not isinstance(transitions, list) or len(personas) < 1 or not isinstance(personas, list):
            return ErrorEvent(message="Invalid length of personas or transitions in your query to generate a table.")

        request = RequestSchema(transitions=transitions,
                                personas=personas)

        ctx.write_event_to_stream(ProgressEvent(msg="Request input processed. Passing to matrix generator..."))
        logger.info("Request input processed. Passing to matrix generator...")

        return MatrixEvent(request_input=request)

    @step
    async def generate_test_matrix(self, ctx: Context, ev: MatrixEvent) -> MatrixAnswerEvent:
        """
        Creates the table of transitions and personas based on the provided input.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (MatrixEvent): The event containing transitions and personas data.

        Returns:
            MatrixAnswerEvent
        """
        request = ev.request_input
        logger.info(
            f'Generating test matrix for {len(request.personas)} personas and {len(request.transitions)} transitions.')

        ctx.write_event_to_stream(ProgressEvent(msg="Generating test matrix from validated input..."))

        response = await self.answer_agent.achat(f"""
        Please generate a structured test matrix from the following input.

        Transitions: {request.transitions}

        Personas: {request.personas}

        """)

        logger.info(f"Answer agent response type: {type(response)}")
        logger.info(f"Answer agent response: {response}")

        ctx.write_event_to_stream(
            ProgressEvent(msg="Test matrix generated. Preparing final response...")
        )

        response_str = str(response)
        logger.info(f"Response string: {response_str}")

        try:
            json_match = re.search(r'\{.*}', response_str, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                response_data = json.loads(json_str)
                matrix_data = response_data.get('matrix', {})
                test_cases = response_data.get('test_cases', [])
                explanation = f"Matrix generated successfully with {len(test_cases)} test cases."
            elif response_str.strip().startswith('{'):
                response_data = json.loads(response_str)
                matrix_data = response_data.get('matrix', {})
                test_cases = response_data.get('test_cases', [])
                explanation = f"Matrix generated successfully with {len(test_cases)} test cases."
            else:
                matrix_data = {}
                explanation = f"Matrix generated. Response type: {type(response)}"
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"JSON parsing error: {e}")
            matrix_data = {}
            explanation = f"Matrix generated. Response type: {type(response)}"

        return MatrixAnswerEvent(
            matrix_data=matrix_data,
            explanation=explanation,
        )

    @step
    async def validate_and_report(self, ctx: Context, ev: MatrixAnswerEvent) -> StopEvent:
        """
        Tests and Approves the validity of the generated test matrix data.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (MatrixAnswerEvent): The event containing matrix data, explanation and optional_recommendations data.

        Returns:
            StopEvent
        """
        logger.info(f"Validating test matrix with {len(ev.matrix_data)} transitions.")
        ctx.write_event_to_stream(ProgressEvent(msg="Validating generated matrix and explanation..."))

        result = await self.report_agent.achat(f"""
            Matrix Data: {ev.matrix_data}
            Explanation: {ev.explanation}
            Please Provide Recommendations and Guidelines to improve the results if necessary.
        """)

        logger.info(f"Validation result received: {result}")

        if isinstance(result, dict):
            final_explanation = result.get('explanation', ev.explanation)
            optional_recommendations = result.get('optional_recommendations', '')
        else:
            final_explanation = str(result)
            optional_recommendations = ''

        await ctx.store.set('optional_recommendations', optional_recommendations)
        await ctx.store.set('final_explanation', final_explanation)
        await ctx.store.set('matrix_data', ev.matrix_data)

        return StopEvent(result={
            'summary': final_explanation,
            'recommendations': optional_recommendations,
            'matrix_data': ev.matrix_data,
        })

    @step
    async def handle_error(self, ctx: Context, ev: ErrorEvent) -> StopEvent:
        """
        Handles ErrorEvent by converting it to a StopEvent, marking the workflow as terminated due to error.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (ErrorEvent): The error event to handle.

        Returns:
            StopEvent: A terminal event containing the error message.
        """
        logger.error(f"Workflow terminated due to error: {ev.message}")
        ctx.write_event_to_stream(ProgressEvent(msg=f"Workflow stopped due to error: {ev.message}"))
        return StopEvent(result={
            'status': 'error',
            'message': ev.message
        })
