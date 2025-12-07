"""
Currency Symbol Detection Script
Scans all Python files in the project and reports hardcoded ₹ symbols.
Outputs: relative path, line number, and the line content.
"""

import os
import re
from pathlib import Path


def find_currency_symbols(root_dir):
    """
    Find all hardcoded ₹ symbols in Python files.
    
    Args:
        root_dir: Root directory to start searching from
        
    Returns:
        List of dictionaries containing file path, line number, and line content
    """
    results = []
    root_path = Path(root_dir)
    
    # Pattern to match ₹ symbol (can be in strings, f-strings, etc.)
    pattern = re.compile(r'₹')
    
    # Find all Python files
    python_files = list(root_path.rglob('*.py'))
    
    print(f"Scanning {len(python_files)} Python files...\n")
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, start=1):
                if pattern.search(line):
                    # Get relative path from project root
                    rel_path = file_path.relative_to(root_path)
                    
                    results.append({
                        'file': str(rel_path),
                        'line': line_num,
                        'content': line.rstrip()
                    })
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
    
    return results


def print_results(results):
    """
    Print results in a formatted way.
    
    Args:
        results: List of result dictionaries
    """
    if not results:
        print("✅ No hardcoded ₹ symbols found!")
        return
    
    print(f"Found {len(results)} instances of hardcoded ₹ symbol:\n")
    print("=" * 100)
    
    # Group by file for better readability
    current_file = None
    
    for result in sorted(results, key=lambda x: (x['file'], x['line'])):
        if current_file != result['file']:
            if current_file is not None:
                print()  # Empty line between files
            current_file = result['file']
            print(f"\n📄 {result['file']}")
            print("-" * 100)
        
        print(f"   Line {result['line']:4d}: {result['content']}")
    
    print("\n" + "=" * 100)
    print(f"\nTotal: {len(results)} instances found")
    
    # Statistics by file
    print("\n📊 Statistics by file:")
    file_counts = {}
    for result in results:
        file_counts[result['file']] = file_counts.get(result['file'], 0) + 1
    
    for file, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {count:3d} instances: {file}")


def export_to_file(results, output_file='currency_symbols_report.txt'):
    """
    Export results to a text file.
    
    Args:
        results: List of result dictionaries
        output_file: Output file name
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Currency Symbol Detection Report\n")
        f.write("=" * 100 + "\n\n")
        
        current_file = None
        
        for result in sorted(results, key=lambda x: (x['file'], x['line'])):
            if current_file != result['file']:
                if current_file is not None:
                    f.write('\n')
                current_file = result['file']
                f.write(f"\nFile: {result['file']}\n")
                f.write("-" * 100 + "\n")
            
            f.write(f"Line {result['line']:4d}: {result['content']}\n")
        
        f.write("\n" + "=" * 100 + "\n")
        f.write(f"\nTotal: {len(results)} instances found\n")
        
        # Statistics
        f.write("\nStatistics by file:\n")
        file_counts = {}
        for result in results:
            file_counts[result['file']] = file_counts.get(result['file'], 0) + 1
        
        for file, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{count:3d} instances: {file}\n")
    
    print(f"\n📝 Report exported to: {output_file}")


def main():
    """Main function to run the detection."""
    # Get the script's directory (project root)
    script_dir = Path(__file__).parent
    
    print("🔍 Currency Symbol Detection Tool")
    print("=" * 100)
    print(f"Scanning directory: {script_dir}\n")
    
    # Find all currency symbols
    results = find_currency_symbols(script_dir)
    
    # Print results to console
    print_results(results)
    
    # Export to file
    if results:
        export_to_file(results)
        
        # Print suggestions
        print("\n💡 Suggestions:")
        print("   1. Replace f\"₹{amount:,.2f}\" with format_currency(amount)")
        print("   2. Replace \"₹0.00\" with format_currency(0)")
        print("   3. Replace setPrefix(\"₹ \") with setPrefix(f\"{get_currency_symbol()} \")")
        print("\n   Use currency_replacer.py script for automated replacement.")


if __name__ == '__main__':
    main()
