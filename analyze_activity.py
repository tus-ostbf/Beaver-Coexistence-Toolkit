#!/usr/bin/env python3
"""
analyze_activity.py
A simple Python script to summarize beaver activity observations.

Reads a CSV file that follows the beaver_activity_template.csv format and prints:
- Total number of observations
- Frequency of each activity type
- Number of observations per month

Example usage:
    python analyze_activity.py beaver_observations_2024.csv
"""

import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python analyze_activity.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Initialize counters
    total_observations = 0
    activity_counter = Counter()
    monthly_counter = defaultdict(int)  # key: 'YYYY-MM', value: count
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            # Use DictReader to access columns by header names
            reader = csv.DictReader(f)
            # Ensure required columns exist
            required_cols = {'Date', 'Activity Type'}
            if not required_cols.issubset(reader.fieldnames):
                print(f"Error: CSV must contain columns: {required_cols}")
                sys.exit(1)
            
            for row in reader:
                total_observations += 1
                
                # Count activity type
                activity = row['Activity Type'].strip()
                activity_counter[activity] += 1
                
                # Parse date and count per month
                date_str = row['Date'].strip()
                try:
                    # Accept various date formats; adjust as needed
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_counter[month_key] += 1
                except ValueError:
                    # If date format doesn't match, skip monthly counting
                    pass
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
    
    # Print summary
    print("=== Beaver Activity Summary ===")
    print(f"Total observations: {total_observations}")
    print()
    
    print("Activity Type Frequency:")
    for activity, count in sorted(activity_counter.items()):
        print(f"  {activity}: {count}")
    print()
    
    print("Observations per Month:")
    if monthly_counter:
        for month, count in sorted(monthly_counter.items()):
            print(f"  {month}: {count}")
    else:
        print("  (No valid dates found)")
    print()
    
    # Additional simple stats: most common activity
    if activity_counter:
        most_common = activity_counter.most_common(1)[0]
        print(f"Most frequent activity: {most_common[0]} ({most_common[1]} occurrences)")

if __name__ == "__main__":
    main()