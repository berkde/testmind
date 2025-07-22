import logging
from llama_index.core.workflow import StopEvent
from ..models.event import ErrorEvent
from ..core.workflow import TestMindWorkflow
from ..core.agent import conversation_agent, question_agent, answer_agent, report_agent

logger = logging.getLogger(__name__)

class TestMindHandler:
    """
    Handler class to manage the execution of the TestMind workflow.
    
    This class provides a clean interface for running the TestMind workflow
    with proper error handling, progress monitoring, and result formatting.
    """

    def __init__(self, timeout: int = 300):
        """
        Initialize the TestMind handler.
        
        Args:
            timeout (int): Workflow timeout in seconds. Defaults to 300.
        """
        self.workflow = TestMindWorkflow(timeout=timeout)


    async def run(self, user_input: str, conversation_context: dict = None) -> dict:
        """
        Run the TestMind workflow with the provided user input.

        Args:
            user_input (str): The raw input from the user.
            conversation_context (dict, optional): The user's session context.

        Returns:
            dict: The result of the workflow execution containing:
                - status: "success" or "error"
                - summary: Final explanation (if successful)
                - recommendations: Improvement suggestions (if successful)
                - matrix_data: Generated test matrix (if successful)
                - message: Error message (if error)
                - conversation_context: Updated session context
        """
        logger.info("Starting TestMind workflow execution...")

        try:
            handler = self.workflow.run(
                input=user_input,
                conversation_agent=conversation_agent,
                question_agent=question_agent,
                answer_agent=answer_agent,
                report_agent=report_agent,
                conversation_context=conversation_context or {}
            )

            async for ev in handler.stream_events():
                if hasattr(ev, 'msg'):
                    logger.info(f"Progress: {ev.msg}")

            final_result = await handler

            updated_context = None
            if hasattr(self.workflow, 'conversation_context'):
                updated_context = self.workflow.conversation_context
            elif conversation_context is not None:
                updated_context = conversation_context
            else:
                updated_context = {}

            if isinstance(final_result, StopEvent):
                logger.info("Workflow completed successfully.")
                result_status = final_result.result.get("status", "success")
                
                if result_status == "conversation":
                    return {
                        "status": "conversation",
                        "response": final_result.result.get("response", ""),
                        "conversation_context": final_result.result.get("conversation_context", updated_context)
                    }
                else:
                    return {
                        "status": "success",
                        "summary": final_result.result.get("summary", ""),
                        "recommendations": final_result.result.get("recommendations", ""),
                        "matrix_data": final_result.result.get("matrix_data", {}),
                        "matrix_statistics": final_result.result.get("matrix_statistics", {}),
                        "conversation_context": updated_context
                    }

            elif isinstance(final_result, ErrorEvent):
                logger.warning("Workflow failed due to error event.")
                return {
                    "status": "error",
                    "message": "We couldn't process your request. Please check your input and try again.",
                    "conversation_context": updated_context
                }

            elif isinstance(final_result, dict):
                logger.info("Workflow returned a dict result.")
                result = dict(final_result)
                if 'status' not in result:
                    if 'matrix_data' in result:
                        result['status'] = 'success'
                    elif 'response' in result:
                        result['status'] = 'conversation'
                    else:
                        result['status'] = 'error'
                        result['message'] = result.get('message', 'Unknown error')
                if result['status'] == 'success' and 'summary' not in result:
                    result['summary'] = ''
                if result['status'] == 'conversation' and 'summary' not in result:
                    result['summary'] = ''
                result['conversation_context'] = updated_context
                return result

            else:
                logger.error(f"Unexpected result type from workflow: {type(final_result)}")
                return {
                    "status": "error",
                    "message": "Unknown workflow result.",
                    "conversation_context": updated_context
                }

        except Exception as e:
            logger.exception("Unexpected error during workflow execution.")
            return {
                "status": "error",
                "message": "Sorry, something went wrong while processing your request. Please try again later.",
                "conversation_context": conversation_context or {}
            }
