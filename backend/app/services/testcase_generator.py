from typing import List, Dict, Tuple
from enum import Enum

class Status(str, Enum):
    ESSENTIAL = "Green"
    OPTIONAL = "Yellow"
    REDUNDANT = "Red"

def generate_matrix(transitions: List[Dict], personas: List[str]) -> Tuple[Dict, List[Dict]]:
    matrix = {}
    test_ids = []
    test_counter = 1

    for t in transitions:
        from_state = t["from"]
        to_state = t["to"]
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
