from ..models.event import (
    GenerateEvent,
    MatrixEvent,
    MatrixAnswerEvent,
    ProgressEvent,
    ErrorEvent,
    ConversationEvent,
    ConversationResponseEvent)
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
        conversation_agent: The agent responsible for conversational interactions and intent detection.
        question_agent: The agent responsible for interpreting user input and extracting context.
        answer_agent: The agent responsible for generating the test matrix.
        report_agent: The agent responsible for validating and summarizing the result.
    """

    def __init__(self, timeout=300):
        super().__init__(timeout=timeout)
        self.conversation_agent = None
        self.report_agent = None
        self.answer_agent = None
        self.question_agent = None

    def __repr__(self):
        return f'<TestMindWorkflow timeout={self._timeout}>'

    @step
    async def setup(self, ctx: Context, ev: StartEvent) -> ConversationEvent:
        self.conversation_agent = ev.conversation_agent
        self.question_agent = ev.question_agent
        self.answer_agent = ev.answer_agent
        self.report_agent = ev.report_agent

        ctx.write_event_to_stream(ProgressEvent(msg="Initializing TestMind system..."))
        return ConversationEvent(input=ev.input)

    @step
    async def process_conversation(self, ctx: Context, ev: ConversationEvent) -> ConversationResponseEvent | GenerateEvent | ErrorEvent:
        """
        Processes user input through the conversation agent to determine if matrix generation is needed.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (ConversationEvent): The event containing raw user input.

        Returns:
            ConversationResponseEvent if conversation should continue,
            GenerateEvent if matrix generation should be triggered,
            ErrorEvent if there's an error.
        """
        logger.info(f'Processing conversation input: {ev.input}')
        ctx.write_event_to_stream(ProgressEvent(msg="Processing user input through conversation agent..."))

        if not self.conversation_agent:
            logger.error("Conversation agent not initialized")
            return ErrorEvent(message="System error: Conversation agent not available")

        conversation_context = await ctx.store.get('conversation_context', {})

        context_str = ""
        if conversation_context.get('previous_matrices'):
            context_str = f"\nPrevious matrices: {conversation_context['previous_matrices']}"

        result = await self.conversation_agent.achat(f"""
        User input: {ev.input}
        {context_str}
        
        Determine if this input should trigger matrix generation or continue conversation.
        
        CRITICAL: Only treat DIRECT COMMANDS as matrix generation requests. Look for these patterns:
        - Direct action commands: 'generate', 'create', 'build', 'make', 'show me', 'give me', 'provide'
        - Matrix-related terms: 'matrix', 'table', 'test case table', 'test matrix', 'test cases'
        - Example requests: 'example', 'sample', 'demonstration', 'illustration'
        - Testing terms: 'test cases', 'test scenarios', 'testing workflow', 'test plan'
        
        Questions, help requests, and general inquiries should be conversational.
        
        Examples that should trigger matrix generation (DIRECT COMMANDS):
        - "Generate an example test case table" → MATRIX_GENERATION
        - "Create a test matrix" → MATRIX_GENERATION
        - "Show me a test case table" → MATRIX_GENERATION
        
        Examples that should be CONVERSATIONAL:
        - "Can you help me generate a table today?" → CONVERSATION (offer help, ask for details)
        - "How do I create a test matrix?" → CONVERSATION (explain the process)
        - "Help me understand test cases" → CONVERSATION (explain concepts)
        
        If matrix generation is needed, respond with: MATRIX_GENERATION: [processed input]
        If conversation should continue, respond with: CONVERSATION: [your response]
        """)

        response_text = str(result)
        logger.info(f"Conversation agent response: {response_text}")

        if "MATRIX_GENERATION:" in response_text:
            matrix_input = response_text.split("MATRIX_GENERATION:")[1].strip()
            ctx.write_event_to_stream(ProgressEvent(msg="Matrix generation requested. Processing input..."))
            return GenerateEvent(input=matrix_input)
        elif "CONVERSATION:" in response_text:
            conversation_response = response_text.split("CONVERSATION:")[1].strip()
            return ConversationResponseEvent(
                response=conversation_response,
                should_generate_matrix=False,
                matrix_input=None,
                conversation_context=conversation_context
            )
        else:
            return ConversationResponseEvent(
                response=response_text,
                should_generate_matrix=False,
                matrix_input=None,
                conversation_context=conversation_context
            )

    @step
    async def handle_conversation_response(self, ctx: Context, ev: ConversationResponseEvent) -> StopEvent:
        """
        Handles conversation responses when matrix generation is not needed.

        Args:
            ctx (Context): The execution context for this workflow step.
            ev (ConversationResponseEvent): The conversation response event.

        Returns:
            StopEvent: A terminal event containing the conversation response.
        """
        logger.info(f"Handling conversation response: {ev.response}")
        ctx.write_event_to_stream(ProgressEvent(msg="Processing conversation response..."))

        await ctx.store.set('conversation_context', ev.conversation_context)

        return StopEvent(result={
            'status': 'conversation',
            'response': ev.response,
            'conversation_context': ev.conversation_context
        })


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

        if not self.question_agent:
            logger.error("Question agent not initialized")
            return ErrorEvent(message="System error: Question agent not available")

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
                    if persona and persona not in personas and persona != "":
                        personas.append(persona)
                elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. "):
                    persona = line[3:].strip()
                    if persona and persona not in personas and persona != "":
                        personas.append(persona)
                elif line and not line.startswith("**") and not line.startswith("Transitions:") and not line.startswith("CRITICAL") and not line.startswith("Example"):
                    persona = line.strip()
                    if persona and persona not in personas and len(persona) > 0 and persona != "":
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
                        elif "optional_for:" in part or "Optional for:" in part or "redundant_for:" in part or "Redundant for:" in part:
                            key = "optional_for:" if "optional_for:" in part else ("Optional for:" if "Optional for:" in part else ("redundant_for:" if "redundant_for:" in part else "Redundant for:"))
                            transition["redundant_for"] = part.split(key)[1].strip()

                    if len(transition) >= 4:
                        transitions.append(transition)

        logger.info(f"Parsed transitions: {transitions}")
        logger.info(f"Parsed personas: {personas}")
        logger.info(f"Number of transitions found: {len(transitions)}")
        logger.info(f"Number of personas found: {len(personas)}")

        if not result:
            logger.error('No result from question agent')
            return ErrorEvent(message='TestMind was unable to process your request. Please try again.')
            
        if not transitions:
            logger.error('No transitions extracted from input')
            return ErrorEvent(message='TestMind could not identify any transitions in your request. Please provide specific transition details like "from new to in-progress".')
            
        if not personas:
            logger.error('No personas extracted from input')
            return ErrorEvent(message='TestMind could not identify any personas in your request. Please provide specific personas like "manager, developer, hr".')

        if len(transitions) < 1 or not isinstance(transitions, list) or len(personas) < 1 or not isinstance(personas, list):
            return ErrorEvent(message="Invalid length of personas or transitions in your query to generate a table.")

        request = RequestSchema(transitions=transitions,
                                personas=personas)

        await ctx.store.set('user_input', ev.input)
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
                statistics = response_data.get('statistics', {})
                explanation = f"Matrix generated successfully with {len(test_cases)} test cases."
            elif response_str.strip().startswith('{'):
                response_data = json.loads(response_str)
                matrix_data = response_data.get('matrix', {})
                test_cases = response_data.get('test_cases', [])
                statistics = response_data.get('statistics', {})
                explanation = f"Matrix generated successfully with {len(test_cases)} test cases."
            else:
                matrix_data = {}
                statistics = {}
                explanation = f"Matrix generated. Response type: {type(response)}"
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"JSON parsing error: {e}")
            matrix_data = {}
            statistics = {}
            explanation = f"Matrix generated. Response type: {type(response)}"

        await ctx.store.set('matrix_statistics', statistics)

        conversation_context = await ctx.store.get('conversation_context', {})
        previous_matrices = conversation_context.get('previous_matrices', [])
        previous_matrices.append({
            'matrix_data': matrix_data,
            'statistics': statistics,
            'explanation': explanation
        })
        if len(previous_matrices) > 3:
            previous_matrices = previous_matrices[-3:]
        conversation_context['previous_matrices'] = previous_matrices
        await ctx.store.set('conversation_context', conversation_context)

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

        user_input = await ctx.store.get('user_input', '')
        matrix_statistics = await ctx.store.get('matrix_statistics', {})
        
        result = await self.report_agent.achat(f"""
        Original User Input: {user_input}
        
        Generated Matrix Data: {ev.matrix_data}
        Matrix Statistics: {matrix_statistics}
        Matrix Explanation: {ev.explanation}
        
        Please analyze this specific matrix and provide:
        1. A detailed summary of what was generated based on the user's actual input
        2. Matrix statistics breakdown including total combinations and their distribution
        3. An explanation of how the matrix addresses the user's specific requirements
        4. Practical recommendations for testing this specific workflow
        5. Quality assessment of the generated matrix
        
        Focus on the actual transitions, personas, and relationships provided by the user.
        Include the statistics in your Matrix Statistics section.
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
        await ctx.store.set('matrix_statistics', matrix_statistics)

        conversation_context = await ctx.store.get('conversation_context', {})
        # conversation_context['previous_matrices'] = []
        await ctx.store.set('conversation_context', conversation_context)
        
        return StopEvent(result={
            'summary': final_explanation,
            'recommendations': optional_recommendations,
            'matrix_data': ev.matrix_data,
            'matrix_statistics': matrix_statistics,
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
