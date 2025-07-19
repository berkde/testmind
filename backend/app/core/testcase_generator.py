from typing import List, Dict, Tuple
from enum import Enum
from llama_index.core.tools import FunctionTool
from logging import getLogger

logger = getLogger(__name__)

class Status(str, Enum):
    ESSENTIAL = "Essential"
    OPTIONAL = "Optional"
    PROHIBITED = "Prohibited"

def generate_matrix(transitions: List[Dict], personas: List[str]) -> Tuple[Dict, List[Dict], Dict]:
    """
    Generate a test matrix from transitions and personas.
    
    Args:
        transitions: List of transition dictionaries with keys: from_state, to_state, essential_for, optional_for
        personas: List of persona strings
        
    Returns:
        Tuple of (matrix_dict, test_ids_list, statistics_dict)
    """
    matrix = {}
    test_ids = []
    test_counter = 1
    statistics = {
        'total_combinations': 0,
        'essential_combinations': 0,
        'optional_combinations': 0,
        'prohibited_combinations': 0,
        'total_transitions': len(transitions),
        'total_personas': len(personas)
    }

    logger.info(f"Generating test matrix for {len(transitions)} transitions")
    logger.info(f"Generating test matrix for {len(personas)} personas")

    for t in transitions:
        from_state = t["from_state"]
        to_state = t["to_state"]
        essential = t["essential_for"]
        optional = t.get("optional_for", "")
        transition_key = f"{from_state}→{to_state}"

        matrix[transition_key] = {}

        for persona in personas:
            statistics['total_combinations'] += 1
            
            if persona == essential:
                gid = f"G{test_counter}"
                matrix[transition_key][persona] = {"status": Status.ESSENTIAL, "id": gid}
                test_ids.append({"id": gid, "transition": transition_key, "by": persona})
                test_counter += 1
                statistics['essential_combinations'] += 1
            elif persona == optional:
                matrix[transition_key][persona] = {"status": Status.OPTIONAL}
                statistics['optional_combinations'] += 1
            else:
                matrix[transition_key][persona] = {"status": Status.PROHIBITED}
                statistics['prohibited_combinations'] += 1

    logger.info(f"Generated test matrix size {len(matrix)}")
    logger.info(f"test ids: {test_ids}")
    logger.info(f"statistics: {statistics}")

    return matrix, test_ids, statistics

generate_matrix_tool = FunctionTool.from_defaults(
    fn=generate_matrix,
    name="generate_matrix",
    description="Generate a test matrix from transitions and personas. Input: transitions (list of dicts) and personas (list of strings). Output: tuple of (matrix_dict, test_ids_list, statistics_dict)."
)