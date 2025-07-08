#!/usr/bin/env python3
"""
Demo script to show the complete TestMind matrix generation process
"""

import asyncio
import logging
from app.services.handler import TestMindHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def demo_matrix_generation():
    """Demonstrate the complete matrix generation process."""
    
    print("TestMind Matrix Generation Demo")
    print("=" * 60)

    test_input = """
    Generate a test matrix for the following transitions and personas.

    Transitions:
    - from: login, to: dashboard, essential_for: admin, optional_for: guest
    - from: dashboard, to: logout, essential_for: admin, optional_for: guest

    Personas:
    - admin
    - guest
    """
    
    print("Input:")
    print(test_input.strip())
    print("-" * 60)
    
    try:
        handler = TestMindHandler(timeout=300)
        
        print("Starting TestMind workflow...")
        print()

        result = await handler.run(test_input)
        
        print("Workflow completed!")
        print("=" * 60)

        status = result.get('status', 'success' if result.get('matrix_data') else 'unknown')
        print(f"Status: {status}")
        print()
        
        if status != 'error':
            print("Summary:")
            print(result.get('summary', 'No summary available'))
            print()
            
            print("Recommendations:")
            recommendations = result.get('recommendations', 'No recommendations available')
            if recommendations:
                print(recommendations)
            else:
                print("No specific recommendations provided.")
            print()
            
            print("Generated Test Matrix:")
            matrix_data = result.get('matrix_data', {})
            if matrix_data:
                print("┌─────────────────────┬─────────┬─────────┬─────────┐")
                print("│ Transition          │ Persona │ Status  │ Test ID │")
                print("├─────────────────────┼─────────┼─────────┼─────────┤")
                
                for transition, personas in matrix_data.items():
                    for persona, details in personas.items():
                        status = details.get('status', 'Unknown')
                        test_id = details.get('id', 'N/A')
                        print(f"│ {transition:<19} │ {persona:<7} │ {status:<7} │ {test_id:<7} │")
                
                print("└─────────────────────┴─────────┴─────────┴─────────┘")
                print()
                
                print("🔍 Matrix Analysis:")
                print(f"• Total transitions: {len(matrix_data)}")
                total_test_cases = sum(1 for transition_data in matrix_data.values() 
                                     for details in transition_data.values() 
                                     if details.get('id'))
                print(f"• Essential test cases: {total_test_cases}")
                optional_cases = sum(1 for transition_data in matrix_data.values() 
                                   for details in transition_data.values() 
                                   if details.get('status') == 'Yellow')
                print(f"• Optional test cases: {optional_cases}")
                
            else:
                print("  No matrix data available")
        else:
            print("Error:")
            print(result.get('message', 'Unknown error occurred'))
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_matrix_generation()) 