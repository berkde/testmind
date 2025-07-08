from typing import List, Dict, Tuple
from enum import Enum
from llama_index.core.tools import FunctionTool

class Status(str, Enum):
    ESSENTIAL = "Green"
    OPTIONAL = "Yellow"
    REDUNDANT = "Red"

def generate_matrix(transitions: List[Dict], personas: List[str]) -> Tuple[Dict, List[Dict]]:
    """
    Generate a test matrix from transitions and personas.
    
    Args:
        transitions: List of transition dictionaries with keys: from_state, to_state, essential_for, optional_for
        personas: List of persona strings
        
    Returns:
        Tuple of (matrix_dict, test_ids_list)
    """
    matrix = {}
    test_ids = []
    test_counter = 1

    for t in transitions:
        from_state = t["from_state"]
        to_state = t["to_state"]
        essential = t["essential_for"]
        optional = t.get("optional_for", [])
        transition_key = f"{from_state}→{to_state}"

        matrix[transition_key] = {}

        for persona in personas:
            if persona == essential:
                gid = f"G{test_counter}"
                matrix[transition_key][persona] = {"status": Status.ESSENTIAL, "id": gid}
                test_ids.append({"id": gid, "transition": transition_key, "by": persona})
                test_counter += 1
            elif persona in optional:
                matrix[transition_key][persona] = {"status": Status.OPTIONAL}
            else:
                matrix[transition_key][persona] = {"status": Status.REDUNDANT}

    return matrix, test_ids

# Create the tool with proper metadata
generate_matrix_tool = FunctionTool.from_defaults(
    fn=generate_matrix,
    name="generate_matrix",
    description="Generate a test matrix from transitions and personas. Input: transitions (list of dicts) and personas (list of strings). Output: tuple of (matrix_dict, test_ids_list)."
)