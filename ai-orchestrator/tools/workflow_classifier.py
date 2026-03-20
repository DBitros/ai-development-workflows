#!/usr/bin/env python3
"""
Workflow Classification Tool

Determines whether a request is:
1. New Feature Development - Creates new modules/functionality
2. Bug Fix/Crash Fix - Targets existing code for fixes
3. Enhancement - Improves existing functionality

This classifier helps route requests to the appropriate workflow.
"""

import re
from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

class WorkflowType(Enum):
    FEATURE_DEVELOPMENT = "feature_development"
    BUG_FIX = "bug_fix"
    CRASH_FIX = "crash_fix"
    ENHANCEMENT = "enhancement"
    REFACTORING = "refactoring"

@dataclass
class ClassificationResult:
    workflow_type: WorkflowType
    confidence: float  # 0.0 to 1.0
    reasoning: List[str]
    suggested_codebase_paths: List[str]
    crash_indicators: Dict[str, str]  # For crash fixes

class WorkflowClassifier:
    def __init__(self):
        # Keywords that indicate different workflow types
        self.bug_keywords = [
            'fix', 'crash', 'error', 'exception', 'bug', 'issue', 'failure',
            'broken', 'not working', 'fails', 'crashing', 'exc_breakpoint',
            'exc_bad_access', 'sigabrt', 'nil', 'unhandled', 'stackoverflow'
        ]

        self.crash_keywords = [
            'crash', 'crashlytics', 'firebase', 'exc_breakpoint', 'exc_bad_access',
            'sigabrt', 'signal', 'abort', 'terminated', 'exception', 'fatal',
            'stack trace', 'backtrace'
        ]

        self.feature_keywords = [
            'add', 'create', 'new', 'implement', 'build', 'develop',
            'introduce', 'feature', 'functionality', 'capability'
        ]

        self.enhancement_keywords = [
            'improve', 'enhance', 'optimize', 'update', 'upgrade',
            'refactor', 'modernize', 'streamline', 'polish'
        ]

    def classify(self, description: str, context: Dict = None) -> ClassificationResult:
        """
        Classify a workflow request based on description and optional context.

        Args:
            description: The ticket description or request
            context: Optional context like crash reports, screenshots, etc.
        """
        description_lower = description.lower()
        context = context or {}

        # Initialize scoring
        scores = {
            WorkflowType.BUG_FIX: 0.0,
            WorkflowType.CRASH_FIX: 0.0,
            WorkflowType.FEATURE_DEVELOPMENT: 0.0,
            WorkflowType.ENHANCEMENT: 0.0,
            WorkflowType.REFACTORING: 0.0
        }

        reasoning = []
        suggested_paths = []
        crash_indicators = {}

        # Check for crash-specific indicators
        crash_score = self._score_crash_indicators(description_lower, context)
        if crash_score > 0:
            scores[WorkflowType.CRASH_FIX] = crash_score
            reasoning.append(f"Crash indicators detected (score: {crash_score:.2f})")
            crash_indicators = self._extract_crash_indicators(description, context)

        # Check for bug fix indicators
        bug_score = self._score_keywords(description_lower, self.bug_keywords)
        if bug_score > 0:
            scores[WorkflowType.BUG_FIX] = max(scores[WorkflowType.BUG_FIX], bug_score)
            reasoning.append(f"Bug fix keywords found (score: {bug_score:.2f})")

        # Check for feature development indicators
        feature_score = self._score_keywords(description_lower, self.feature_keywords)
        if feature_score > 0:
            scores[WorkflowType.FEATURE_DEVELOPMENT] = feature_score
            reasoning.append(f"Feature development keywords found (score: {feature_score:.2f})")

        # Check for enhancement indicators
        enhancement_score = self._score_keywords(description_lower, self.enhancement_keywords)
        if enhancement_score > 0:
            scores[WorkflowType.ENHANCEMENT] = enhancement_score
            reasoning.append(f"Enhancement keywords found (score: {enhancement_score:.2f})")

        # Extract potential file/class references
        suggested_paths = self._extract_code_references(description)
        if suggested_paths:
            reasoning.append(f"Found code references: {', '.join(suggested_paths)}")

        # Determine the highest scoring workflow type
        max_type = max(scores.keys(), key=lambda k: scores[k])
        max_score = scores[max_type]

        # Default to feature development if no clear indicators
        if max_score == 0:
            max_type = WorkflowType.FEATURE_DEVELOPMENT
            max_score = 0.5
            reasoning.append("No clear indicators found, defaulting to feature development")

        return ClassificationResult(
            workflow_type=max_type,
            confidence=max_score,
            reasoning=reasoning,
            suggested_codebase_paths=suggested_paths,
            crash_indicators=crash_indicators
        )

    def _score_crash_indicators(self, description: str, context: Dict) -> float:
        """Score crash-specific indicators."""
        score = 0.0

        # Check for crash keywords in description
        crash_matches = sum(1 for keyword in self.crash_keywords if keyword in description)
        score += crash_matches * 0.2

        # Check for iOS crash signatures
        ios_crash_patterns = [
            r'exc_breakpoint', r'exc_bad_access', r'sigabrt',
            r'viewdidload', r'tableview.*nil', r'accessing.*before.*loaded'
        ]

        for pattern in ios_crash_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                score += 0.3

        # Check context for crash-related data
        if context.get('firebase_crash_report'):
            score += 0.5
        if context.get('crash_count', 0) > 0:
            score += 0.3
        if context.get('crash_screenshots'):
            score += 0.2

        return min(score, 1.0)  # Cap at 1.0

    def _score_keywords(self, text: str, keywords: List[str]) -> float:
        """Score based on keyword matches."""
        matches = sum(1 for keyword in keywords if keyword in text)
        # Score proportional to matches, capped at 1.0
        return min(matches * 0.15, 1.0)

    def _extract_crash_indicators(self, description: str, context: Dict) -> Dict[str, str]:
        """Extract specific crash information."""
        indicators = {}

        # Extract class/method names
        class_pattern = r'(\w+ViewController|\w+Controller|\w+View)'
        classes = re.findall(class_pattern, description, re.IGNORECASE)
        if classes:
            indicators['affected_classes'] = ', '.join(set(classes))

        # Extract method names
        method_pattern = r'(\w+\(\)|viewDidLoad|viewWillAppear|setUpSearchSuggestionsProvider)'
        methods = re.findall(method_pattern, description, re.IGNORECASE)
        if methods:
            indicators['affected_methods'] = ', '.join(set(methods))

        # Extract crash types
        crash_types = ['EXC_BREAKPOINT', 'EXC_BAD_ACCESS', 'SIGABRT']
        for crash_type in crash_types:
            if crash_type.lower() in description.lower():
                indicators['crash_type'] = crash_type
                break

        # Add context information
        if context.get('crash_count'):
            indicators['crash_count'] = str(context['crash_count'])
        if context.get('user_count'):
            indicators['affected_users'] = str(context['user_count'])

        return indicators

    def _extract_code_references(self, description: str) -> List[str]:
        """Extract potential file/class references from description."""
        references = []

        # Extract class names (ending with Controller, View, etc.)
        class_patterns = [
            r'(\w+ViewController)',
            r'(\w+Controller)',
            r'(\w+View)',
            r'(\w+Manager)',
            r'(\w+Service)',
            r'(\w+Provider)'
        ]

        for pattern in class_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            references.extend(matches)

        # Extract potential file paths
        file_pattern = r'(\w+/\w+/\w+\.swift)'
        file_matches = re.findall(file_pattern, description)
        references.extend(file_matches)

        return list(set(references))  # Remove duplicates

def classify_workflow(description: str, **context) -> ClassificationResult:
    """Convenience function to classify a workflow."""
    classifier = WorkflowClassifier()
    return classifier.classify(description, context)

# Example usage for VLP-427
if __name__ == "__main__":
    # Test with VLP-427 description
    vlp_427_description = """VLP-427: Fix Firebase crash in DiscoverViewController.setUpSearchSuggestionsProvider - EXC_BREAKPOINT when accessing tableView before viewDidLoad in AppSearchSuggestionsViewController"""

    context = {
        'crash_count': 536,
        'user_count': 106,
        'firebase_crash_report': True,
        'crash_screenshots': True
    }

    result = classify_workflow(vlp_427_description, **context)

    print("=== Workflow Classification Result ===")
    print(f"Type: {result.workflow_type.value}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Suggested paths: {result.suggested_codebase_paths}")
    print(f"Crash indicators: {result.crash_indicators}")