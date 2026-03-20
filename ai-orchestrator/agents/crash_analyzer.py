#!/usr/bin/env python3
"""
TradeMe iOS Crash Analysis Agent

Specialized agent for analyzing crashes, parsing Firebase reports,
and generating targeted fixes for existing code in the TradeMe iOS app.

Responsibilities:
- Parse Firebase crash reports and extract key information
- Analyze existing TradeMe code to identify root causes
- Generate targeted patches instead of new modules
- Validate fixes against known crash patterns
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from shared_utils import (
    AgentConfig, FileManager, HandoffManager, ValidationManager,
    AgentRole, WorkflowStage, WorkflowContext
)

@dataclass
class CrashAnalysis:
    crash_type: str
    affected_files: List[str]
    root_cause: str
    fix_strategy: str
    proposed_changes: List[Dict[str, Any]]
    validation_steps: List[str]

@dataclass
class CodeFix:
    file_path: str
    line_number: Optional[int]
    original_code: str
    fixed_code: str
    explanation: str
    safety_checks: List[str]

class TradeMeCrashAnalyzer:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)

        # TradeMe codebase path
        self.trademe_root = "/Users/dbitros/Development/trademe"

        # Common iOS crash patterns
        self.crash_patterns = {
            'EXC_BREAKPOINT': self._analyze_exc_breakpoint,
            'EXC_BAD_ACCESS': self._analyze_exc_bad_access,
            'SIGABRT': self._analyze_sigabrt,
            'tableView_nil': self._analyze_tableview_nil,
            'viewDidLoad_timing': self._analyze_viewdidload_timing
        }

    def analyze_crash(self, context: WorkflowContext) -> CrashAnalysis:
        """
        Main entry point for crash analysis.

        Args:
            context: Workflow context containing crash details

        Returns:
            CrashAnalysis with root cause and proposed fixes
        """
        print(f"🔍 === TradeMe Crash Analysis Agent ===")
        print(f"🎯 Analyzing: {context.description}")

        # Extract crash information from description
        crash_info = self._parse_crash_description(context.description)

        # Find affected files in TradeMe codebase
        affected_files = self._find_affected_files(crash_info)

        # Analyze each file for crash patterns
        analysis_results = []
        for file_path in affected_files:
            file_analysis = self._analyze_file_for_crash(file_path, crash_info)
            if file_analysis:
                analysis_results.append(file_analysis)

        # Generate fix strategy
        fix_strategy = self._generate_fix_strategy(crash_info, analysis_results)

        # Create proposed code changes
        proposed_changes = self._generate_code_fixes(analysis_results, crash_info)

        return CrashAnalysis(
            crash_type=crash_info.get('crash_type', 'Unknown'),
            affected_files=affected_files,
            root_cause=self._determine_root_cause(crash_info, analysis_results),
            fix_strategy=fix_strategy,
            proposed_changes=proposed_changes,
            validation_steps=self._generate_validation_steps(crash_info)
        )

    def _parse_crash_description(self, description: str) -> Dict[str, Any]:
        """Extract crash information from the description."""
        crash_info = {}

        # Extract crash type
        crash_types = ['EXC_BREAKPOINT', 'EXC_BAD_ACCESS', 'SIGABRT']
        for crash_type in crash_types:
            if crash_type.lower() in description.lower():
                crash_info['crash_type'] = crash_type
                break

        # Extract class/method names
        class_pattern = r'(\w+ViewController|\w+Controller|\w+View)'
        classes = re.findall(class_pattern, description)
        crash_info['affected_classes'] = list(set(classes))

        # Extract method names
        method_pattern = r'(\w+\(\)|viewDidLoad|viewWillAppear|setUpSearchSuggestionsProvider)'
        methods = re.findall(method_pattern, description)
        crash_info['affected_methods'] = list(set(methods))

        # Extract specific issues
        if 'tableview before viewdidload' in description.lower():
            crash_info['issue_type'] = 'tableView_nil'
            crash_info['timing_issue'] = True

        if 'accessing' in description.lower() and 'before' in description.lower():
            crash_info['issue_type'] = 'viewDidLoad_timing'
            crash_info['timing_issue'] = True

        return crash_info

    def _find_affected_files(self, crash_info: Dict[str, Any]) -> List[str]:
        """Find the actual files in TradeMe codebase that are affected."""
        affected_files = []

        # Search for classes mentioned in crash
        for class_name in crash_info.get('affected_classes', []):
            # Find files containing this class
            search_pattern = f"class {class_name}"
            files = self._search_codebase(search_pattern)
            affected_files.extend(files)

        # If we know specific files from our analysis (like VLP-427)
        known_files = {
            'DiscoverViewController': 'TradeMeMain/View Controllers/Custom/Search/DiscoverViewController.swift',
            'AppSearchSuggestionsViewController': 'Feature/Search/Search/Suggestions/AppSearchSuggestionsViewController.swift'
        }

        for class_name in crash_info.get('affected_classes', []):
            if class_name in known_files:
                full_path = os.path.join(self.trademe_root, known_files[class_name])
                if os.path.exists(full_path):
                    affected_files.append(full_path)

        return list(set(affected_files))  # Remove duplicates

    def _search_codebase(self, pattern: str) -> List[str]:
        """Search the TradeMe codebase for a pattern."""
        files = []
        try:
            import subprocess
            result = subprocess.run(
                ['grep', '-r', '-l', pattern, self.trademe_root],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        except Exception as e:
            print(f"Warning: Could not search codebase: {e}")

        return files

    def _analyze_file_for_crash(self, file_path: str, crash_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a specific file for crash patterns."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            analysis = {
                'file_path': file_path,
                'issues_found': [],
                'line_numbers': [],
                'code_snippets': []
            }

            lines = content.split('\n')

            # Look for specific crash patterns
            issue_type = crash_info.get('issue_type')
            if issue_type and issue_type in self.crash_patterns:
                pattern_analysis = self.crash_patterns[issue_type](content, lines, crash_info)
                if pattern_analysis:
                    analysis.update(pattern_analysis)

            return analysis if analysis['issues_found'] else None

        except Exception as e:
            print(f"Warning: Could not analyze file {file_path}: {e}")
            return None

    def _analyze_tableview_nil(self, content: str, lines: List[str], crash_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tableView nil access patterns."""
        analysis = {
            'issues_found': [],
            'line_numbers': [],
            'code_snippets': []
        }

        # Look for tableView access in configuration didSet
        for i, line in enumerate(lines):
            if 'didset' in line.lower() and 'configuration' in line.lower():
                # Look for tableView usage in next few lines
                for j in range(i, min(i + 10, len(lines))):
                    if 'tableview' in lines[j].lower() and 'TGTableViewStyleManager' in lines[j]:
                        analysis['issues_found'].append('tableView accessed in configuration didSet before viewDidLoad')
                        analysis['line_numbers'].append(j + 1)  # 1-indexed
                        analysis['code_snippets'].append(lines[j].strip())

        return analysis

    def _analyze_viewdidload_timing(self, content: str, lines: List[str], crash_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze viewDidLoad timing issues."""
        analysis = {
            'issues_found': [],
            'line_numbers': [],
            'code_snippets': []
        }

        # Look for UI element access before viewDidLoad
        ui_elements = ['tableView', 'collectionView', 'scrollView', 'view.']

        for i, line in enumerate(lines):
            # Skip if we're already in viewDidLoad
            if 'func viewdidload' in line.lower():
                continue

            # Look for UI access in properties or early methods
            for element in ui_elements:
                if element in line.lower() and ('=' in line or 'TG' in line):
                    # Check if this is in a problematic context
                    if any(keyword in line.lower() for keyword in ['didset', 'init', 'configuration']):
                        analysis['issues_found'].append(f'{element} accessed before viewDidLoad')
                        analysis['line_numbers'].append(i + 1)
                        analysis['code_snippets'].append(line.strip())

        return analysis

    def _analyze_exc_breakpoint(self, content: str, lines: List[str], crash_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze EXC_BREAKPOINT crashes (usually nil access)."""
        return self._analyze_tableview_nil(content, lines, crash_info)

    def _analyze_exc_bad_access(self, content: str, lines: List[str], crash_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze EXC_BAD_ACCESS crashes."""
        # Implementation for bad access analysis
        return {'issues_found': [], 'line_numbers': [], 'code_snippets': []}

    def _analyze_sigabrt(self, content: str, lines: List[str], crash_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze SIGABRT crashes."""
        # Implementation for SIGABRT analysis
        return {'issues_found': [], 'line_numbers': [], 'code_snippets': []}

    def _determine_root_cause(self, crash_info: Dict[str, Any], analysis_results: List[Dict[str, Any]]) -> str:
        """Determine the root cause of the crash."""
        if crash_info.get('issue_type') == 'tableView_nil':
            return "tableView is being accessed before viewDidLoad has been called, causing it to be nil"

        if crash_info.get('timing_issue'):
            return "UI components are being accessed before the view controller's view lifecycle is ready"

        # Analyze the specific issues found
        all_issues = []
        for result in analysis_results:
            all_issues.extend(result.get('issues_found', []))

        if all_issues:
            return f"Multiple issues found: {'; '.join(all_issues)}"

        return "Unable to determine specific root cause from available information"

    def _generate_fix_strategy(self, crash_info: Dict[str, Any], analysis_results: List[Dict[str, Any]]) -> str:
        """Generate a strategy for fixing the crash."""
        if crash_info.get('issue_type') == 'tableView_nil':
            return """
1. Add nil-safety checks before accessing tableView
2. Defer tableView-dependent operations until after viewDidLoad
3. Use guard statements to prevent unsafe access
4. Consider moving initialization logic to viewDidLoad or later in the lifecycle
"""

        return "Add appropriate safety checks and lifecycle management"

    def _generate_code_fixes(self, analysis_results: List[Dict[str, Any]], crash_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific code fixes."""
        fixes = []

        for result in analysis_results:
            file_path = result['file_path']

            for i, issue in enumerate(result.get('issues_found', [])):
                if i < len(result.get('line_numbers', [])):
                    line_num = result['line_numbers'][i]
                    code_snippet = result.get('code_snippets', [''])[i] if i < len(result.get('code_snippets', [])) else ''

                    fix = self._generate_specific_fix(issue, code_snippet, crash_info)
                    if fix:
                        fixes.append({
                            'file_path': file_path,
                            'line_number': line_num,
                            'issue': issue,
                            'original_code': code_snippet,
                            'fixed_code': fix['fixed_code'],
                            'explanation': fix['explanation']
                        })

        return fixes

    def _generate_specific_fix(self, issue: str, original_code: str, crash_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a specific fix for an issue."""
        if 'tableView accessed in configuration didSet' in issue:
            # For VLP-427 specific fix
            if 'TGTableViewStyleManager' in original_code:
                return {
                    'fixed_code': f"guard let tableView = tableView else {{ return }}\n        {original_code}",
                    'explanation': "Added guard statement to ensure tableView is not nil before creating TGTableViewStyleManager"
                }

        if 'tableView accessed before viewDidLoad' in issue:
            return {
                'fixed_code': f"guard isViewLoaded else {{ return }}\n        {original_code}",
                'explanation': "Added isViewLoaded check to ensure view lifecycle is ready"
            }

        return None

    def _generate_validation_steps(self, crash_info: Dict[str, Any]) -> List[str]:
        """Generate steps to validate the fix."""
        return [
            "1. Build the project to ensure no compilation errors",
            "2. Run unit tests for affected view controllers",
            "3. Test the specific user flow that caused the crash",
            "4. Verify that tableView is properly initialized before use",
            "5. Monitor Firebase Crashlytics for crash rate reduction",
            "6. Test on different iOS versions and device types"
        ]

    def generate_crash_fix_report(self, context: WorkflowContext) -> str:
        """Generate a comprehensive crash fix report."""
        analysis = self.analyze_crash(context)

        report = f"""# Crash Analysis Report: {context.ticket_id}

## Crash Overview
- **Type**: {analysis.crash_type}
- **Root Cause**: {analysis.root_cause}

## Affected Files
{chr(10).join(f"- {file}" for file in analysis.affected_files)}

## Proposed Fixes
{chr(10).join(self._format_fix(fix) for fix in analysis.proposed_changes)}

## Fix Strategy
{analysis.fix_strategy}

## Validation Steps
{chr(10).join(analysis.validation_steps)}

---
*Generated by TradeMe iOS Crash Analysis Agent*
"""

        # Save report
        report_path = self.file_manager.get_agents_path(
            f"crash-analysis/{context.ticket_id}-crash-analysis.md"
        )
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, 'w') as f:
            f.write(report)

        print(f"📋 Crash analysis report saved: {report_path}")
        return report_path

    def _format_fix(self, fix: Dict[str, Any]) -> str:
        """Format a fix for the report."""
        return f"""
### {os.path.basename(fix['file_path'])}:{fix['line_number']}

**Issue**: {fix['issue']}

**Original Code**:
```swift
{fix['original_code']}
```

**Fixed Code**:
```swift
{fix['fixed_code']}
```

**Explanation**: {fix['explanation']}
"""

if __name__ == "__main__":
    # Test with VLP-427
    from shared_utils import create_workflow_context

    vlp_427_description = """VLP-427: Fix Firebase crash in DiscoverViewController.setUpSearchSuggestionsProvider - EXC_BREAKPOINT when accessing tableView before viewDidLoad in AppSearchSuggestionsViewController"""

    context = create_workflow_context("VLP-427", vlp_427_description)

    analyzer = TradeMeCrashAnalyzer()
    analysis = analyzer.analyze_crash(context)

    print("=== Crash Analysis Result ===")
    print(f"Type: {analysis.crash_type}")
    print(f"Root Cause: {analysis.root_cause}")
    print(f"Affected Files: {analysis.affected_files}")
    print(f"Proposed Changes: {len(analysis.proposed_changes)}")