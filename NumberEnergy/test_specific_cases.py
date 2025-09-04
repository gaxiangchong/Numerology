#!/usr/bin/env python3
"""
Test specific cases to understand the 5 amplification requirement
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import the analysis function
from app import analyze_number_pairs

def test_specific_cases():
    """Test specific cases to understand the requirement"""
    
    test_cases = [
        "153",  # Should be 天医[1]显 (13 with 1x 5 amplification)
        "1553", # Should be 天医[1]显显 (13 with 2x 5 amplification)
        "155813195", # Your example
        "01155813195", # Your full example
    ]
    
    for test_number in test_cases:
        print(f"\nTesting: {test_number}")
        print("=" * 40)
        
        # Analyze the number
        primary_result, pair_stats, grouped_stats, grouped_energy, ending_warning, group_to_pairs, detailed_group_rows = analyze_number_pairs(test_number)
        
        print("Results:")
        for i, result in enumerate(primary_result):
            print(f"  {i+1}. {result}")
        
        print("\nDetailed Analysis:")
        for row in detailed_group_rows:
            print(f"  Pair: {row['pair']} | Group: {row['group']} | Energy: {row['energy']} | Amplification: {row['amplification']}x")

if __name__ == '__main__':
    test_specific_cases()
