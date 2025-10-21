#!/usr/bin/env python3
"""
Recipe HTML Project QA Validator
================================
This script validates recipe HTML projects to ensure:
- All HTMLs follow the required schema
- Inventory is accurate and complete
- Index contains all recipes with valid links
- File naming is consistent
- No broken references

Usage:
    python recipe-qa-validator.py
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class RecipeSchemaParser(HTMLParser):
    """Parse HTML and validate Schema.org recipe markup"""
    
    def __init__(self):
        super().__init__()
        self.has_recipe_schema = False
        self.has_name = False
        self.has_description = False
        self.has_yield = False
        self.has_image = False
        self.ingredient_count = 0
        self.instruction_count = 0
        self.ingredients_on_parent = False
        self.instructions_on_parent = False
        self.current_tag = None
        self.in_ul_or_ol = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Check for recipe schema
        if 'itemtype' in attrs_dict and 'Recipe' in attrs_dict['itemtype']:
            self.has_recipe_schema = True
        
        # Check for required properties
        if 'itemprop' in attrs_dict:
            prop = attrs_dict['itemprop']
            
            if prop == 'name':
                self.has_name = True
            elif prop == 'description':
                self.has_description = True
            elif prop == 'recipeYield':
                self.has_yield = True
            elif prop == 'image':
                self.has_image = True
            elif prop == 'recipeIngredient':
                if tag == 'li':
                    self.ingredient_count += 1
                else:
                    # Found on parent element (BAD!)
                    self.ingredients_on_parent = True
            elif prop == 'recipeInstructions':
                if tag == 'li':
                    self.instruction_count += 1
                else:
                    # Found on parent element (BAD!)
                    self.instructions_on_parent = True
        
        # Track if we're in a list
        if tag in ['ul', 'ol']:
            self.in_ul_or_ol = True
            
    def handle_endtag(self, tag):
        if tag in ['ul', 'ol']:
            self.in_ul_or_ol = False
    
    def get_validation_result(self) -> Dict[str, any]:
        """Return validation results"""
        return {
            'has_schema': self.has_recipe_schema,
            'has_name': self.has_name,
            'has_description': self.has_description,
            'has_yield': self.has_yield,
            'has_image': self.has_image,
            'ingredient_count': self.ingredient_count,
            'instruction_count': self.instruction_count,
            'schema_errors': {
                'ingredients_on_parent': self.ingredients_on_parent,
                'instructions_on_parent': self.instructions_on_parent,
            }
        }


class RecipeProjectValidator:
    """Main validator for recipe HTML projects"""
    
    def __init__(self, github_folder: str, project_name: str):
        self.github_folder = Path(github_folder)
        self.project_name = project_name
        self.recipe_folder = self.github_folder / project_name
        
        # Find index file (lowercase project name with hyphens)
        index_name = project_name.lower().replace(' ', '-') + '.html'
        self.index_file = self.github_folder / index_name
        
        self.inventory_file = self.recipe_folder / 'recipe-inventory.md'
        
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.stats = {
            'total_recipes_in_inventory': 0,
            'completed_recipes_in_inventory': 0,
            'html_files_found': 0,
            'recipes_in_index': 0,
        }
    
    def validate_all(self) -> Tuple[Dict, Dict, Dict]:
        """Run all validation checks"""
        print(f"\n{'='*70}")
        print(f"🔍 Validating Recipe Project: {self.project_name}")
        print(f"{'='*70}\n")
        
        # Check project structure exists
        if not self._validate_project_structure():
            return self.errors, self.warnings, self.stats
        
        # Load inventory data
        inventory_recipes = self._load_inventory()
        
        # Load index data
        index_recipes = self._load_index()
        
        # Get HTML files
        html_files = self._get_html_files()
        
        # Run validations
        self._validate_schema_compliance(html_files)
        self._validate_file_naming(html_files)
        self._cross_reference_inventory_files_index(inventory_recipes, html_files, index_recipes)
        self._validate_alphabetical_order(index_recipes)
        
        return self.errors, self.warnings, self.stats
    
    def _validate_project_structure(self) -> bool:
        """Check that required files and folders exist"""
        print("📁 Checking project structure...")
        
        if not self.recipe_folder.exists():
            self.errors['structure'].append(f"Recipe folder not found: {self.recipe_folder}")
            return False
        
        if not self.inventory_file.exists():
            self.errors['structure'].append(f"Inventory file not found: {self.inventory_file}")
            return False
        
        if not self.index_file.exists():
            self.errors['structure'].append(f"Index file not found: {self.index_file}")
            return False
        
        print(f"   ✓ Recipe folder: {self.recipe_folder.name}")
        print(f"   ✓ Inventory file: {self.inventory_file.name}")
        print(f"   ✓ Index file: {self.index_file.name}\n")
        
        return True
    
    def _load_inventory(self) -> Dict[str, Dict]:
        """Parse inventory file and return recipe data"""
        print("📋 Loading inventory...")
        
        recipes = {}
        
        with open(self.inventory_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all recipe entries
        # Format: - [ ] or - [x] Recipe Name (p.XXX)
        pattern = r'- \[([ x])\] (.+?) \(p\.(\d+)\)'
        matches = re.findall(pattern, content)
        
        for completed, name, page in matches:
            is_complete = completed == 'x'
            recipes[name.strip()] = {
                'page': page,
                'completed': is_complete
            }
            self.stats['total_recipes_in_inventory'] += 1
            if is_complete:
                self.stats['completed_recipes_in_inventory'] += 1
        
        # Extract statistics from inventory
        completed_match = re.search(r'\*\*Completed:\*\* (\d+)', content)
        missing_match = re.search(r'\*\*Missing:\*\* (\d+)', content)
        
        if completed_match:
            claimed_completed = int(completed_match.group(1))
            if claimed_completed != self.stats['completed_recipes_in_inventory']:
                self.errors['inventory'].append(
                    f"Inventory statistics mismatch: Claims {claimed_completed} completed, "
                    f"but found {self.stats['completed_recipes_in_inventory']} marked as [x]"
                )
        
        if missing_match:
            claimed_missing = int(missing_match.group(1))
            actual_missing = self.stats['total_recipes_in_inventory'] - self.stats['completed_recipes_in_inventory']
            if claimed_missing != actual_missing:
                self.errors['inventory'].append(
                    f"Inventory statistics mismatch: Claims {claimed_missing} missing, "
                    f"but found {actual_missing} unchecked"
                )
        
        print(f"   ✓ Found {len(recipes)} recipes in inventory")
        print(f"   ✓ Completed: {self.stats['completed_recipes_in_inventory']}")
        print(f"   ✓ Missing: {self.stats['total_recipes_in_inventory'] - self.stats['completed_recipes_in_inventory']}\n")
        
        return recipes
    
    def _load_index(self) -> List[Dict]:
        """Parse index file and return recipe links"""
        print("📑 Loading index...")
        
        recipes = []
        
        with open(self.index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all recipe links
        # Format: <a href="Project Name/filename.html">Display Name</a>
        pattern = rf'<a href="{re.escape(self.project_name)}/([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, content)
        
        for filename, display_name in matches:
            recipes.append({
                'filename': filename,
                'display_name': display_name.strip(),
                'path': self.recipe_folder / filename
            })
            self.stats['recipes_in_index'] += 1
        
        print(f"   ✓ Found {len(recipes)} recipes in index\n")
        
        return recipes
    
    def _get_html_files(self) -> List[Path]:
        """Get all HTML files in recipe folder"""
        print("📄 Scanning HTML files...")
        
        html_files = list(self.recipe_folder.glob('*.html'))
        self.stats['html_files_found'] = len(html_files)
        
        print(f"   ✓ Found {len(html_files)} HTML files\n")
        
        return html_files
    
    def _validate_schema_compliance(self, html_files: List[Path]):
        """Validate Schema.org markup in all HTML files"""
        print("🔬 Validating Schema.org markup...")
        
        schema_issues = []
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parser = RecipeSchemaParser()
            parser.feed(content)
            result = parser.get_validation_result()
            
            # Check for issues
            issues = []
            
            if not result['has_schema']:
                issues.append("Missing Recipe schema (itemtype)")
            if not result['has_name']:
                issues.append("Missing recipe name (itemprop='name')")
            if not result['has_description']:
                issues.append("Missing description (itemprop='description')")
            if not result['has_yield']:
                issues.append("Missing yield (itemprop='recipeYield')")
            if not result['has_image']:
                issues.append("Missing image (itemprop='image')")
            if result['ingredient_count'] == 0:
                issues.append("No ingredients with itemprop='recipeIngredient'")
            if result['instruction_count'] == 0:
                issues.append("No instructions with itemprop='recipeInstructions'")
            if result['schema_errors']['ingredients_on_parent']:
                issues.append("❌ CRITICAL: itemprop='recipeIngredient' found on parent element (must be on <li> tags)")
            if result['schema_errors']['instructions_on_parent']:
                issues.append("❌ CRITICAL: itemprop='recipeInstructions' found on parent element (must be on <li> tags)")
            
            if issues:
                self.errors['schema'].append({
                    'file': html_file.name,
                    'issues': issues
                })
                schema_issues.append(html_file.name)
        
        if schema_issues:
            print(f"   ⚠️  Found schema issues in {len(schema_issues)} files\n")
        else:
            print(f"   ✓ All HTML files have valid schema\n")
    
    def _validate_file_naming(self, html_files: List[Path]):
        """Check that all filenames follow naming convention"""
        print("📝 Validating file naming...")
        
        naming_issues = []
        
        for html_file in html_files:
            filename = html_file.name
            
            # Check for spaces
            if ' ' in filename:
                self.errors['naming'].append(f"{filename}: Contains spaces (should use hyphens)")
                naming_issues.append(filename)
                continue
            
            # Check for uppercase letters (except .html extension)
            name_without_ext = filename[:-5]  # Remove .html
            if name_without_ext != name_without_ext.lower():
                self.errors['naming'].append(f"{filename}: Contains uppercase letters (should be all lowercase)")
                naming_issues.append(filename)
                continue
            
            # Check for special characters (allow only letters, numbers, hyphens)
            if not re.match(r'^[a-z0-9-]+\.html$', filename):
                self.warnings['naming'].append(f"{filename}: Contains special characters (should only have letters, numbers, hyphens)")
        
        if naming_issues:
            print(f"   ⚠️  Found naming issues in {len(naming_issues)} files\n")
        else:
            print(f"   ✓ All filenames follow naming convention\n")
    
    def _cross_reference_inventory_files_index(self, inventory_recipes: Dict, html_files: List[Path], index_recipes: List[Dict]):
        """Cross-reference inventory, HTML files, and index"""
        print("🔗 Cross-referencing inventory, files, and index...")
        
        # Get sets for comparison
        completed_in_inventory = {name for name, data in inventory_recipes.items() if data['completed']}
        html_filenames = {f.name for f in html_files}
        index_filenames = {r['filename'] for r in index_recipes}
        
        # Find completed recipes without HTML files
        for recipe_name in completed_in_inventory:
            # Try to find corresponding HTML file
            found = False
            for html_file in html_files:
                # Read HTML to check if title matches
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if recipe_name in content:
                    found = True
                    break
            
            if not found:
                self.warnings['cross_reference'].append(
                    f"Recipe marked complete in inventory but no matching HTML found: {recipe_name}"
                )
        
        # Find HTML files not in index
        for html_file in html_files:
            if html_file.name not in index_filenames:
                self.errors['cross_reference'].append(
                    f"HTML file exists but not in index: {html_file.name}"
                )
        
        # Find index entries with missing files
        for recipe in index_recipes:
            if not recipe['path'].exists():
                self.errors['cross_reference'].append(
                    f"Index links to non-existent file: {recipe['filename']}"
                )
        
        # Check for HTML files without matching index entry
        orphaned_files = html_filenames - index_filenames
        if orphaned_files:
            for filename in orphaned_files:
                self.errors['cross_reference'].append(
                    f"HTML file not linked in index: {filename}"
                )
        
        print(f"   ✓ Cross-reference complete\n")
    
    def _validate_alphabetical_order(self, index_recipes: List[Dict]):
        """Check that index is in alphabetical order"""
        print("🔤 Validating alphabetical order...")
        
        if not index_recipes:
            return
        
        prev_name = ""
        out_of_order = []
        
        for recipe in index_recipes:
            current_name = recipe['display_name']
            
            if prev_name and current_name.lower() < prev_name.lower():
                out_of_order.append(f"{current_name} comes after {prev_name}")
            
            prev_name = current_name
        
        if out_of_order:
            self.errors['alphabetical'].append("Index is not in alphabetical order:")
            self.errors['alphabetical'].extend(out_of_order)
            print(f"   ⚠️  Found {len(out_of_order)} ordering issues\n")
        else:
            print(f"   ✓ Index is properly alphabetized\n")
    
    def print_report(self):
        """Print formatted QA report"""
        print(f"\n{'='*70}")
        print("📊 QA VALIDATION REPORT")
        print(f"{'='*70}\n")
        
        print("STATISTICS:")
        print(f"  • Total recipes in inventory: {self.stats['total_recipes_in_inventory']}")
        print(f"  • Completed in inventory: {self.stats['completed_recipes_in_inventory']}")
        print(f"  • HTML files found: {self.stats['html_files_found']}")
        print(f"  • Recipes in index: {self.stats['recipes_in_index']}")
        print()
        
        # Count total issues
        total_errors = sum(len(v) if isinstance(v, list) else 1 for v in self.errors.values())
        total_warnings = sum(len(v) if isinstance(v, list) else 1 for v in self.warnings.values())
        
        if total_errors == 0 and total_warnings == 0:
            print("✅ ALL CHECKS PASSED! Project is ready for deployment.")
            return
        
        if self.errors:
            print(f"❌ ERRORS FOUND ({total_errors}):")
            print("-" * 70)
            for category, issues in self.errors.items():
                print(f"\n{category.upper()}:")
                if isinstance(issues, list):
                    for issue in issues:
                        if isinstance(issue, dict):
                            print(f"  • {issue['file']}:")
                            for detail in issue['issues']:
                                print(f"      - {detail}")
                        else:
                            print(f"  • {issue}")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({total_warnings}):")
            print("-" * 70)
            for category, issues in self.warnings.items():
                print(f"\n{category.upper()}:")
                for issue in issues:
                    print(f"  • {issue}")
            print()
        
        print(f"{'='*70}\n")


def get_available_projects(github_folder: str) -> List[str]:
    """Find all recipe projects in the GitHub folder"""
    github_path = Path(github_folder)
    
    projects = []
    for item in github_path.iterdir():
        if item.is_dir() and item.name not in ['.git', 'general', 'archive']:
            # Check if it has an inventory file
            inventory = item / 'recipe-inventory.md'
            if inventory.exists():
                projects.append(item.name)
    
    return sorted(projects)


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🍳 Recipe HTML Project QA Validator")
    print("="*70)
    
    # GitHub folder (hardcoded, but could be made configurable)
    github_folder = "/Users/michelle/Documents/GitHub/2vrxjtz5yr-ui.github.io"
    
    # Find available projects
    projects = get_available_projects(github_folder)
    
    if not projects:
        print("\n❌ No recipe projects found in the GitHub folder.")
        return
    
    # Display available projects
    print("\n📚 Available recipe projects:\n")
    for i, project in enumerate(projects, 1):
        print(f"  {i}. {project}")
    
    # Get user selection
    print("\n" + "-"*70)
    while True:
        try:
            choice = input("\nEnter project number to validate (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                print("\n👋 Goodbye!\n")
                return
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(projects):
                selected_project = projects[choice_num - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(projects)}")
        except ValueError:
            print("❌ Please enter a valid number or 'q' to quit")
    
    # Run validation
    validator = RecipeProjectValidator(github_folder, selected_project)
    errors, warnings, stats = validator.validate_all()
    validator.print_report()


if __name__ == "__main__":
    main()
