from fastapi import FastAPI
from ..models.schemas import RequestSchema, ResponseSchema

app = FastAPI()

@app.post("/generate-matrix", response_model=ResponseSchema)
async def generate_matrix(request: RequestSchema):
    """
    Endpoint to receive project context (via transitions/personas) and generate a state transition matrix.
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