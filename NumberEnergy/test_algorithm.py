#!/usr/bin/env python3
"""
Test script to verify the number analysis algorithm with amplification
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import the analysis function
from app import analyze_number_pairs

def test_phone_number():
    """Test the algorithm with the example phone number"""
    
    # Test case: 01155813195
    test_number = "01155813195"
    print(f"Testing phone number: {test_number}")
    print("=" * 50)
    
    # Analyze the number
    primary_result, pair_stats, grouped_stats, grouped_energy, ending_warning, group_to_pairs, detailed_group_rows = analyze_number_pairs(test_number)
    
    print("Primary Analysis Results:")
    print("-" * 30)
    for i, result in enumerate(primary_result):
        print(f"{i+1}. {result}")
    
    print("\nDetailed Group Analysis:")
    print("-" * 30)
    for row in detailed_group_rows:
        print(f"Pair: {row['pair']} | Group: {row['group']} | Energy: {row['energy']} | Amplification: {row['amplification']}x")
    
    print("\nGroup Statistics:")
    print("-" * 30)
    for group, stats in grouped_stats.items():
        print(f"{group}: {stats['count']} pairs ({stats['percent']}%)")
    
    print("\nEnergy Analysis:")
    print("-" * 30)
    for group, energy in grouped_energy.items():
        print(f"{group}: {energy}% total energy")
    
    if ending_warning:
        print(f"\nEnding Warning: {ending_warning}")
    
    print("\nExpected Results for 01155813195:")
    print("- After removing 0s: 155813195")
    print("- After removing 5s: 181319")
    print("- Pairs found: 18, 81, 13, 31, 19")
    print("- 18/81 should be 五鬼[1]显 (amplified by 1x 5)")
    print("- 13/31 should be 天医[1]显 (amplified by 1x 5)")
    print("- 19 should be 延年[1]显 (amplified by 1x 5)")

if __name__ == '__main__':
    test_phone_number()
