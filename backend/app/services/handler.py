import logging
from llama_index.core.workflow import StopEvent
from ..models.event import ErrorEvent
from ..core.workflow import TestMindWorkflow
from ..core.agent import question_agent, answer_agent, report_agent

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


    async def run(self, user_input: str) -> dict:
        """
        Run the TestMind workflow with the provided user input.

        Args:
            user_input (str): The raw input from the user.

        Returns:
            dict: The result of the workflow execution containing:
                - status: "success" or "error"
                - summary: Final explanation (if successful)
                - recommendations: Improvement suggestions (if successful)
                - matrix_data: Generated test matrix (if successful)
                - message: Error message (if error)
        """
        logger.info("Starting TestMind workflow execution...")


        try:
            handler = self.workflow.run(
                input=user_input,
                question_agent=question_agent,
                answer_agent=answer_agent,
                report_agent=report_agent
            )

            async for ev in handler.stream_events():
                if hasattr(ev, 'msg'):
                    logger.info(f"Progress: {ev.msg}")

            final_result = await handler

            if isinstance(final_result, StopEvent):
                logger.info("Workflow completed successfully.")
                return {
                    "status": "success",
                    "summary": final_result.result.get("summary", ""),
                    "recommendations": final_result.result.get("recommendations", ""),
                    "matrix_data": final_result.result.get("matrix_data", {})
                }

            elif isinstance(final_result, ErrorEvent):
                logger.warning("Workflow failed due to error event.")
                return {
                    "status": "error",
                    "message": final_result.message
                }

            elif isinstance(final_result, dict):
                # If the workflow returns a dict directly (e.g., from error handler), return it as is
                logger.info("Workflow returned a dict result.")
                return final_result

            else:
                logger.error(f"Unexpected result type from workflow: {type(final_result)}")
                return {
                    "status": "error",
                    "message": "Unknown workflow result."
                }

        except Exception as e:
            logger.exception("Unexpected error during workflow execution.")
            return {
                "status": "error",
                "message": f"Workflow execution failed: {str(e)}"
            }
