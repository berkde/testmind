from fastapi import FastAPI
from fastapi import Body
from ..models.schemas import ResponseSchema

app = FastAPI()

@app.post("/generate-matrix", response_model=ResponseSchema)
async def generate_matrix(user_input: str = Body(...)):
    """
    Endpoint to receive project context as raw string (via transitions/personas) and generate a state transition matrix.
    Currently returns mock data.
    """

    #  Mock matrix for Post Drafted -> Post Published Transition from "Post New Ideas" App
    mock_matrix = (
        {
            "PostDraftedToPostPublished": {
                "RegisteredUser": {"status": "Essential", "id": "G1"},
                "Visitor": {"status": "Prohibited", "id": "R1"},
            },
        },
        [
            {"id": "G1", "transition": "PostDraftedToPostPublished", "by": "system"},
            {"id": "R1", "transition": "PostDraftedToPostPublished", "by": "system"},
        ],
    )

    return ResponseSchema(
        status="success",
        llm_text_response="Mock matrix generated successfully for Post Drafted to Post Published transition.",
        generated_matrix=mock_matrix
    )