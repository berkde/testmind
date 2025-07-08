from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from ..core.testcase_generator import generate_matrix
from .config import get_settings, get_api_key

from dotenv import load_dotenv

load_dotenv()

settings = get_settings()


question_agent_cfg = settings.question_agent
answer_agent_cfg = settings.answer_agent
report_agent_cfg = settings.report_agent

question_agent_llm = OpenAI(model=question_agent_cfg.model,
                            temperature=question_agent_cfg.temperature,
                            max_tokens=question_agent_cfg.max_tokens,
                            api_key=get_api_key())

answer_agent_llm = OpenAI(model=answer_agent_cfg.model,
                          temperature=answer_agent_cfg.temperature,
                          max_tokens=answer_agent_cfg.max_tokens,
                          api_key=get_api_key())

report_agent_llm = OpenAI(model=report_agent_cfg.model,
                          temperature=report_agent_cfg.temperature,
                          max_tokens=report_agent_cfg.max_tokens,
                          api_key=get_api_key())

question_agent = FunctionAgent(
    name="Question Agent",
    tools=[],
    llm=question_agent_llm,
    verbose=False,
    system_prompt="""
        You are a conversational AI assistant within a system that transforms natural language feature descriptions
        into structured software test cases. Your primary role is to interact with users,
        help them understand how the system works, and collect required inputs.

        When you receive input with transitions and personas, you MUST respond with the following EXACT format:

        **Transitions:**
        1. from: [from_state], to: [to_state], essential_for: [persona], optional_for: [persona]
        2. from: [from_state], to: [to_state], essential_for: [persona], optional_for: [persona]

        **Personas:**
        - [persona1]
        - [persona2]

        Do not add any other text or explanations. Just extract and format the transitions and personas exactly as shown above.
    """
)

answer_agent = FunctionAgent(
    name='Answer Agent',
    tools=[generate_matrix],
    llm=answer_agent_llm,
    verbose=False,  # Disable verbose mode for cleaner output
    system_prompt="""
        You are a matrix generation agent in a software testing system.

        Your task is to use the generate_matrix tool to create a test case matrix from the provided transitions and personas.

        IMPORTANT: Always try to call the generate_matrix tool first. If the tool fails or returns an error, provide a clear error message.

        The generate_matrix tool expects:
        - transitions: List of dictionaries with keys: "from_state", "to_state", "essential_for", "optional_for"
        - personas: List of strings representing user types

        When you receive input with transitions and personas:
        1. Call generate_matrix(transitions=transitions, personas=personas)
        2. If successful, return the tool result in JSON format
        3. If failed, explain what went wrong and provide debugging information

        CRITICAL: The tool returns a tuple (matrix, test_ids). You must convert this to JSON format:
        {
          "matrix": {matrix_data},
          "test_cases": {test_ids}
        }

        Always provide some response - never return empty or silent failures.
     """
)

report_agent = FunctionAgent(
    name='Report Agent',
    tools=[],
    llm=report_agent_llm,
    verbose=False,
    system_prompt="""
        You are the final validation layer in a software testing assistant system.

        Your role is to:
        - Review the generated test matrix.
        - Verify its correctness, consistency, and alignment with user inputs and expectations.
        - Return the validated matrix along with a clear and concise explanation to the user.

        Be precise and ensure the output is accurate, as this will be used for actionable test planning.   
      """
)
