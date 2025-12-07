"""
Currency Symbol Replacement Helper Script
This script helps identify and replace hardcoded currency symbols (₹) with the global format_currency() function.

Usage:
    python currency_replacer.py --scan  # Scan for hardcoded symbols
    python currency_replacer.py --file <filepath> --replace  # Replace in specific file
    python currency_replacer.py --all --replace  # Replace in all files (be careful!)
"""

import re
import os
import argparse
from pathlib import Path


class CurrencyReplacer:
    """Helper to replace hardcoded currency symbols with format_currency() calls."""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.patterns = {
            # Pattern 1: f"₹{amount:,.2f}" - Most common format
            'f_string_format': (
                r'f"₹\{([^}]+):,\.2f\}"',
                r'format_currency(\1)'
            ),
            # Pattern 2: "₹0.00" - Static zero values
            'static_zero': (
                r'"₹0\.00"',
                r'format_currency(0)'
            ),
            # Pattern 3: setPrefix("₹ ") - Spinbox prefix
            'spinbox_prefix': (
                r'setPrefix\("₹ "\)',
                r'setPrefix(f"{get_currency_symbol()} ")'
            ),
            # Pattern 4: Table headers like "Price (₹)" or "Amount (₹)"
            'table_headers': (
                r'\(₹\)',
                r'({get_currency_symbol()})'
            ),
            # Pattern 5: .replace('₹', '') - String cleaning
            # Skip this pattern as it's used for parsing existing values
            
            # Pattern 6: QLabel("Text: ₹0.00") - Labels with text prefix
            'label_with_text': (
                r'QLabel\("([^"]+): ₹0\.00"\)',
                r'QLabel(f"\1: {format_currency(0)}")'
            ),
            # Pattern 7: setText(f"Text: ₹{value:,.2f}")
            'settext_format': (
                r'setText\(f"([^"]+): ₹\{([^}]+):,\.2f\}"\)',
                r'setText(f"\1: {format_currency(\2)}")'
            ),
            # Pattern 8: Simple f"₹{var}" without formatting
            'simple_f_string': (
                r'f"₹\{([^:}]+)\}"',
                r'f"{get_currency_symbol()}{{\1}}"'
            ),
        }
        
        # Scan all Python files in the project (excluding utility scripts)
        self.exclude_files = {
            'currency_replacer.py',
            'detect_currency_symbols.py',
        }
        
        self.import_line = (
            "from travel_billing_software.config.config import "
            "format_currency, get_currency_symbol"
        )
    
    def scan_file(self, filepath):
        """Scan a file for hardcoded currency symbols."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            matches = []
            for name, (pattern, _) in self.patterns.items():
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    matches.append({
                        'line': line_num,
                        'pattern': name,
                        'text': match.group(0)
                    })
            
            return matches
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
            return []
    
    def replace_in_file(self, filepath, dry_run=True):
        """Replace currency symbols in a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_made = []
            
            # Check if import already exists
            has_import = self.import_line in content or \
                        'from travel_billing_software.config.config import format_currency' in content
            
            # Apply replacements
            for name, (pattern, replacement) in self.patterns.items():
                matches = list(re.finditer(pattern, content))
                if matches:
                    content = re.sub(pattern, replacement, content)
                    replacements_made.append(f"{name}: {len(matches)} replacements")
            
            # Add import if needed and replacements were made
            if replacements_made and not has_import:
                # Find the import section
                import_section_end = 0
                for line in content.split('\n'):
                    if line.startswith('import ') or line.startswith('from '):
                        import_section_end = content.find(line) + len(line)
                
                if import_section_end > 0:
                    content = (content[:import_section_end] + '\n' + 
                             self.import_line + '\n' + 
                             content[import_section_end:])
                    replacements_made.append("Added import statement")
            
            if not dry_run and content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Updated {filepath}")
            
            return replacements_made
            
        except Exception as e:
            print(f"✗ Error processing {filepath}: {e}")
            return []
    
    def scan_project(self):
        """Scan entire project for currency symbols."""
        print("🔍 Scanning for hardcoded currency symbols...\n")
        
        total_matches = 0
        files_with_issues = []
        
        # Find all Python files in the project
        for python_file in self.project_root.rglob('*.py'):
            # Skip excluded files
            if python_file.name in self.exclude_files:
                continue
            
            # Skip __pycache__ and build directories
            if '__pycache__' in str(python_file) or 'build' in str(python_file):
                continue
            
            matches = self.scan_file(python_file)
            if matches:
                files_with_issues.append((python_file, matches))
                total_matches += len(matches)
        
        # Print results
        print(f"Found {total_matches} hardcoded currency symbols in {len(files_with_issues)} files:\n")
        
        for filepath, matches in files_with_issues:
            print(f"📄 {filepath.relative_to(self.project_root)}")
            for match in matches[:5]:  # Show first 5 matches
                print(f"   Line {match['line']}: [{match['pattern']}] {match['text']}")
            if len(matches) > 5:
                print(f"   ... and {len(matches) - 5} more")
            print()
        
        return files_with_issues
    
    def process_file(self, filepath, dry_run=True):
        """Process a single file."""
        print(f"Processing: {filepath}")
        replacements = self.replace_in_file(filepath, dry_run)
        
        if replacements:
            mode = "Would replace" if dry_run else "Replaced"
            print(f"  {mode}:")
            for r in replacements:
                print(f"    - {r}")
        else:
            print(f"  No changes needed")
        
        return len(replacements) > 0


def main():
    parser = argparse.ArgumentParser(description='Currency Symbol Replacement Helper')
    parser.add_argument('--scan', action='store_true', 
                       help='Scan project for hardcoded symbols')
    parser.add_argument('--file', type=str,
                       help='Process specific file')
    parser.add_argument('--all', action='store_true',
                       help='Process all files')
    parser.add_argument('--replace', action='store_true',
                       help='Actually make replacements (default is dry-run)')
    
    args = parser.parse_args()
    
    # Find project root
    current_dir = Path(__file__).parent
    project_root = current_dir
    
    replacer = CurrencyReplacer(project_root)
    
    if args.scan:
        replacer.scan_project()
    
    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            filepath = project_root / args.file
        
        if filepath.exists():
            replacer.process_file(filepath, dry_run=not args.replace)
        else:
            print(f"Error: File not found: {filepath}")
    
    elif args.all:
        files = replacer.scan_project()
        
        if not args.replace:
            print("\n⚠️  This was a dry-run. Use --replace to actually modify files.")
            return
        
        confirm = input(f"\n⚠️  This will modify {len(files)} files. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
        
        print("\n🔧 Replacing currency symbols...\n")
        for filepath, _ in files:
            replacer.process_file(filepath, dry_run=False)
        
        print("\n✅ Done! Review changes and test thoroughly.")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
