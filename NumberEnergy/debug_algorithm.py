#!/usr/bin/env python3
"""
Debug script to understand the 5 amplification logic
"""

import os
import sys

# Add the mysite directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Change to the mysite directory
os.chdir(os.path.join(os.path.dirname(__file__), 'mysite'))

# Import the analysis function
from app import convert_alpha_to_numbers

def debug_number_conversion():
    """Debug the number conversion process"""
    
    test_number = "01155813195"
    print(f"Original number: {test_number}")
    
    # Convert to numbers
    number_str = convert_alpha_to_numbers(test_number)
    print(f"After alpha conversion: {number_str}")
    
    # Show positions and characters
    print("\nCharacter positions:")
    for i, char in enumerate(number_str):
        print(f"Position {i}: '{char}'")
    
    # Identify 0s and 5s
    zeros = []
    fives = []
    for i, char in enumerate(number_str):
        if char == '0':
            zeros.append(i)
        elif char == '5':
            fives.append(i)
    
    print(f"\nZeros at positions: {zeros}")
    print(f"Fives at positions: {fives}")
    
    # Show what happens when we remove 0s and 5s
    filtered = []
    for i, char in enumerate(number_str):
        if char not in {'0', '5'}:
            filtered.append(char)
    
    filtered_str = ''.join(filtered)
    print(f"\nAfter removing 0s and 5s: {filtered_str}")
    
    # Show pairs
    print(f"\nPairs found:")
    for i in range(len(filtered_str) - 1):
        pair = filtered_str[i:i+2]
        print(f"Pair {i}: {pair}")
    
    # For each pair, show which 5s come before it
    print(f"\n5s before each pair:")
    for i in range(len(filtered_str) - 1):
        pair = filtered_str[i:i+2]
        # Find original positions of this pair
        pair_start_in_original = None
        pair_end_in_original = None
        
        # Map back to original positions
        filtered_index = 0
        for orig_index, char in enumerate(number_str):
            if char not in {'0', '5'}:
                if filtered_index == i:
                    pair_start_in_original = orig_index
                if filtered_index == i + 1:
                    pair_end_in_original = orig_index
                filtered_index += 1
        
        # Count 5s before this pair
        fives_before = 0
        for five_pos in fives:
            if five_pos < pair_start_in_original:
                fives_before += 1
        
        print(f"Pair {pair} (orig pos {pair_start_in_original}-{pair_end_in_original}): {fives_before} fives before")

if __name__ == '__main__':
    debug_number_conversion()
