#!/usr/bin/env python3
"""
Demo script to show complex TestMind matrix generation with essential, optional, and redundant personas
"""

import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.handler import TestMindHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def demo_complex_matrix_generation():
    """Demonstrate complex matrix generation with all persona types."""
    
    print("TestMind Complex Matrix Generation Demo")
    print("=" * 70)

    test_input = """
    Generate a test matrix for the following transitions and personas.

    Transitions:
    - from: login, to: dashboard, essential_for: admin, optional_for: manager
    - from: dashboard, to: settings, essential_for: admin, optional_for: manager
    - from: settings, to: reports, essential_for: admin, optional_for: analyst
    - from: reports, to: logout, essential_for: admin, optional_for: manager

    Personas:
    - admin
    - manager
    - analyst
    - guest

    Note: Guest persona is not mentioned in any transitions, so it should appear as redundant (Red status) in the matrix.
    """
    
    print("Input:")
    print(test_input.strip())
    print("-" * 70)
    
    try:
        handler = TestMindHandler(timeout=300)
        
        print("Starting TestMind workflow...")
        print()

        result = await handler.run(test_input)
        
        print("Workflow completed!")
        print("=" * 70)

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
                                   if details.get('status') == 'Optional')
                print(f"• Optional test cases: {optional_cases}")
                prohibited_cases = sum(1 for transition_data in matrix_data.values() 
                                     for details in transition_data.values() 
                                     if details.get('status') == 'Prohibited')
                print(f"• Prohibited test cases: {prohibited_cases}")

                matrix_statistics = result.get('matrix_statistics', {})
                if matrix_statistics:
                    print("\n📊 Matrix Statistics:")
                    print(f"• Total combinations: {matrix_statistics.get('total_combinations', 0)}")
                    print(f"• Essential combinations (Green): {matrix_statistics.get('essential_combinations', 0)}")
                    print(f"• Optional combinations (Yellow): {matrix_statistics.get('optional_combinations', 0)}")
                    print(f"• Prohibited combinations (Red): {matrix_statistics.get('prohibited_combinations', 0)}")
                
                print("Persona Coverage Analysis:")
                all_personas = set()
                for transition_data in matrix_data.values():
                    all_personas.update(transition_data.keys())
                
                for persona in sorted(all_personas):
                    persona_stats = []
                    for transition, transition_data in matrix_data.items():
                        if persona in transition_data:
                            status = transition_data[persona].get('status', 'Unknown')
                            persona_stats.append(f"{transition}: {status}")
                    
                    print(f"  • {persona}: {', '.join(persona_stats)}")
                
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
    asyncio.run(demo_complex_matrix_generation()) 