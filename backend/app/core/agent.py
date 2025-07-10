from llama_index.core.agent import FunctionCallingAgent as FunctionAgent
from llama_index.llms.openai import OpenAI
from ..core.testcase_generator import generate_matrix_tool
from .config import get_settings, get_api_key

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

question_agent = FunctionAgent.from_tools(
    tools=[],
    llm=question_agent_llm,
    system_prompt="""
        You are a test matrix extraction assistant.

        Your ONLY job is to extract all possible transitions and personas from the user's description and output them in the following format:

        **Transitions:**
        1. from: [from_state], to: [to_state], essential_for: [persona], optional_for: [persona]
        ...

        **Personas:**
        - [persona1]
        - [persona2]

        DO NOT output tables, explanations, or any other text. Output ONLY in the above format, even if the input is unstructured or ambiguous. If you cannot extract, output empty sections in the format above.
    """
)

answer_agent = FunctionAgent.from_tools(
    tools=[generate_matrix_tool],
    llm=answer_agent_llm,
    system_prompt="""
        You are a matrix generation agent in a software testing system.

        Your task is to use the generate_matrix tool to create a test case matrix from the provided transitions and personas.

        IMPORTANT: You MUST call the generate_matrix function with the transitions and personas data.

        When you respond, you MUST return ONLY a valid JSON object with the following structure:
        {
          "matrix": { ... },
          "test_cases": [ ... ]
        }
        Do not return markdown, explanations, or any other text. Only output the JSON object."""
)

report_agent = FunctionAgent.from_tools(
    tools=[],
    llm=report_agent_llm,
    system_prompt="""
        You are the final validation layer in a software testing assistant system.

        Your role is to:
        - Review the generated test matrix.
        - Verify its correctness, consistency, and alignment with user inputs and expectations.
        - Return the validated matrix along with a clear and concise explanation to the user.

        Be precise and ensure the output is accurate, as this will be used for actionable test planning.   
      """
)
