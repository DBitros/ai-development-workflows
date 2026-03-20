#!/usr/bin/env python3
"""
TradeMe iOS Architect Agent

Responsible for:
- Analyzing requirements against TradeMe iOS architecture patterns
- Validating module dependency constraints (Tuist)
- Ensuring Universal API pattern compliance (97% adoption)
- Validating Dependencies framework usage
- Reviewing platform service integration patterns
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from shared_utils import (
    AgentConfig, FileManager, HandoffManager, ValidationManager,
    AgentRole, WorkflowStage, WorkflowContext, load_architecture_context
)

@dataclass
class ArchitectureAnalysis:
    compliance_status: Dict[str, bool]
    recommendations: List[str]
    constraints: List[str]
    integration_patterns: List[str]
    risk_assessment: Dict[str, str]

class TradeMeArchitect:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)
        self.handoff_manager = HandoffManager(self.config, self.file_manager)
        self.validation_manager = ValidationManager(self.config, self.file_manager)

        # Load architecture context
        self.architecture_context = load_architecture_context(self.file_manager)

        # Agent identity
        self.role = AgentRole.ARCHITECT
        self.agent_config = self.config.get_agent_config(self.role)

    def analyze_ticket(self, context: WorkflowContext) -> ArchitectureAnalysis:
        """
        Perform comprehensive architecture analysis of a ticket.
        """
        print(f"🏛️  TradeMe iOS Architect analyzing: {context.ticket_id}")
        print(f"📝 Description: {context.description}")

        # Step 1: Extract architectural implications from description
        architectural_implications = self._extract_architectural_implications(context.description)

        # Step 2: Validate against TradeMe patterns
        compliance_status = self._validate_trademe_patterns(architectural_implications)

        # Step 3: Identify integration patterns needed
        integration_patterns = self._identify_integration_patterns(architectural_implications)

        # Step 4: Assess risks and constraints
        risk_assessment = self._assess_risks(architectural_implications)

        # Step 5: Generate recommendations
        recommendations = self._generate_recommendations(
            architectural_implications, compliance_status, integration_patterns
        )

        # Step 6: Identify constraints
        constraints = self._identify_constraints(architectural_implications)

        analysis = ArchitectureAnalysis(
            compliance_status=compliance_status,
            recommendations=recommendations,
            constraints=constraints,
            integration_patterns=integration_patterns,
            risk_assessment=risk_assessment
        )

        return analysis

    def _extract_architectural_implications(self, description: str) -> Dict[str, Any]:
        """Extract architectural implications from the ticket description."""
        implications = {
            "new_services": [],
            "ui_components": [],
            "data_storage": [],
            "api_integration": [],
            "platform_services": [],
            "module_type": None,
            "design_system": None,
            "state_management": [],
            "navigation": [],
            "testing_requirements": []
        }

        description_lower = description.lower()

        # Detect service creation
        if any(word in description_lower for word in ['service', 'manager', 'client', 'api']):
            implications["new_services"].append("Platform or shared service likely needed")

        # Detect UI work
        if any(word in description_lower for word in ['ui', 'view', 'screen', 'component', 'swiftui', 'uikit']):
            implications["ui_components"].append("UI components needed")
            if 'swiftui' in description_lower:
                implications["design_system"] = "Tangram2 (modern SwiftUI)"
            elif 'uikit' in description_lower:
                implications["design_system"] = "TMUILibrary (legacy UIKit)"

        # Detect data requirements
        if any(word in description_lower for word in ['cache', 'storage', 'persist', 'database', 'coredata']):
            implications["data_storage"].append("Data persistence layer needed")

        # Detect API work
        if any(word in description_lower for word in ['api', 'network', 'request', 'response', 'endpoint']):
            implications["api_integration"].append("API integration required")
            implications["platform_services"].append("TMAPIClient integration")

        # Detect state management needs
        if any(word in description_lower for word in ['state', 'async', 'reactive', 'rxswift', 'combine']):
            implications["state_management"].append("Chassis framework with Async<T> pattern")

        # Detect navigation requirements
        if any(word in description_lower for word in ['navigation', 'coordinator', 'routing', 'flow']):
            implications["navigation"].append("Navigation pattern required")

        return implications

    def _validate_trademe_patterns(self, implications: Dict[str, Any]) -> Dict[str, bool]:
        """Validate against TradeMe iOS architecture patterns."""
        compliance = {
            "universal_api_pattern": True,
            "dependencies_framework": True,
            "module_hierarchy": True,
            "platform_service_access": True,
            "design_system_usage": True,
            "state_management_pattern": True,
            "testing_integration": True
        }

        # Validate Universal API pattern for new services
        if implications["new_services"]:
            compliance["universal_api_pattern"] = True  # Must follow triple module pattern

        # Validate Dependencies framework usage
        compliance["dependencies_framework"] = True  # Required for all new services

        # Validate module hierarchy
        compliance["module_hierarchy"] = True  # Must respect Platform → Shared → Feature

        # Validate platform service access
        if implications["platform_services"]:
            compliance["platform_service_access"] = True  # Via API abstractions only

        # Validate design system usage
        if implications["design_system"]:
            compliance["design_system_usage"] = True  # Correct system identified

        # Validate state management
        if implications["state_management"]:
            compliance["state_management_pattern"] = True  # Chassis + Async<T>

        return compliance

    def _identify_integration_patterns(self, implications: Dict[str, Any]) -> List[str]:
        """Identify required integration patterns."""
        patterns = []

        if implications["new_services"]:
            patterns.append("Triple Module Pattern: {Service}/{ServiceApi}/{ServiceTests}")
            patterns.append("Universal API Architecture with Dependencies framework")

        if implications["ui_components"]:
            patterns.append("SwiftUI-UIKit integration via established bridge patterns")

        if implications["platform_services"]:
            patterns.append("Platform service access via API protocols only")
            patterns.append("RxSwift-Combine bridge for reactive programming")

        if implications["state_management"]:
            patterns.append("Chassis framework with Async<T> pattern for smooth UI transitions")

        if implications["data_storage"]:
            patterns.append("TMLogger integration for debugging and monitoring")

        if implications["api_integration"]:
            patterns.append("TMAPIClient integration with error handling via TMErrorHandling")

        return patterns

    def _assess_risks(self, implications: Dict[str, Any]) -> Dict[str, str]:
        """Assess architectural risks."""
        risks = {}

        if implications["new_services"]:
            risks["module_dependencies"] = "HIGH: Must ensure .shared modules only depend on other .shared modules (build-breaking)"

        if implications["platform_services"]:
            risks["service_integration"] = "MEDIUM: Platform services use RxSwift, UI likely uses Combine - bridge required"

        if implications["ui_components"] and implications["data_storage"]:
            risks["state_management"] = "MEDIUM: Complex state management across UI and data layers"

        if not implications["design_system"]:
            risks["design_consistency"] = "LOW: Design system not clearly identified - may need guidance"

        return risks

    def _generate_recommendations(self, implications: Dict[str, Any],
                                compliance: Dict[str, bool],
                                patterns: List[str]) -> List[str]:
        """Generate architecture recommendations."""
        recommendations = []

        # Module placement recommendations
        if implications["new_services"]:
            recommendations.append(
                "📦 Create new service following Triple Module Pattern in Platform layer"
            )
            recommendations.append(
                "🔧 Use Dependencies framework for dependency injection (187 existing usages)"
            )

        # UI recommendations
        if implications["ui_components"]:
            if implications["design_system"] == "Tangram2 (modern SwiftUI)":
                recommendations.append("🎨 Use Tangram2 for modern SwiftUI components (.shared type)")
            else:
                recommendations.append("🎨 Use TangramUI bridge components or TMUILibrary for UIKit")

        # State management recommendations
        if implications["state_management"]:
            recommendations.append("⚡ Implement Chassis framework with Async<T> pattern")

        # Testing recommendations
        recommendations.append("🧪 Include Quick/Nimble testing with universal placeholder pattern")

        # Architecture validation
        recommendations.append("✅ Validate against architecture checklist after implementation")

        return recommendations

    def _identify_constraints(self, implications: Dict[str, Any]) -> List[str]:
        """Identify architectural constraints."""
        constraints = []

        # Build system constraints
        constraints.append("🚨 CRITICAL: .shared modules can ONLY depend on other .shared modules")

        # Platform service constraints
        if implications["platform_services"]:
            constraints.append("🔒 Platform services must be accessed via API abstractions only")

        # Dependencies framework constraint
        constraints.append("⚠️  Must use Dependencies framework - custom DI solutions violate 97% adoption")

        # Module hierarchy constraints
        constraints.append("📊 Respect Platform (25) → Shared (26) → Feature (36) hierarchy")

        # Tuist constraints
        constraints.append("🏗️  All changes must be compatible with Tuist 4.55.9 build system")

        return constraints

    def create_architecture_analysis_document(self, context: WorkflowContext,
                                            analysis: ArchitectureAnalysis) -> str:
        """Create the architecture analysis document."""
        timestamp = context.metadata.get('created_at', 'Unknown')

        doc = f"""# Architecture Analysis: {context.ticket_id}

## Ticket Information
- **ID**: {context.ticket_id}
- **Description**: {context.description}
- **Analysis Date**: {timestamp}
- **Analyzed by**: TradeMe iOS Architect Agent

## Executive Summary

This analysis validates the architectural implications of implementing "{context.description}" against the TradeMe iOS architecture patterns and constraints.

## Compliance Status

"""
        for aspect, status in analysis.compliance_status.items():
            status_emoji = "✅" if status else "❌"
            doc += f"- **{aspect.replace('_', ' ').title()}**: {status_emoji} {'Compliant' if status else 'Non-compliant'}\n"

        doc += f"""

## Required Integration Patterns

"""
        for pattern in analysis.integration_patterns:
            doc += f"- {pattern}\n"

        doc += f"""

## Architecture Recommendations

"""
        for recommendation in analysis.recommendations:
            doc += f"- {recommendation}\n"

        doc += f"""

## Critical Constraints

"""
        for constraint in analysis.constraints:
            doc += f"- {constraint}\n"

        doc += f"""

## Risk Assessment

"""
        for risk_type, risk_desc in analysis.risk_assessment.items():
            doc += f"- **{risk_type.replace('_', ' ').title()}**: {risk_desc}\n"

        doc += f"""

## Next Steps

1. **Research Phase**: Investigate existing patterns in codebase for similar functionality
2. **Requirements Creation**: Create Layer 3 requirements document following 7-layer methodology
3. **Implementation Planning**: Design Layer 5 implementation with compliance validation
4. **Code Generation**: Generate Swift code following identified patterns

## Validation Checkpoints

- [ ] Module dependencies validated against Tuist constraints
- [ ] Universal API pattern compliance confirmed
- [ ] Dependencies framework integration verified
- [ ] Platform service access patterns validated
- [ ] Design system integration confirmed
- [ ] State management patterns aligned with Chassis framework
- [ ] Testing strategy includes Quick/Nimble with placeholder patterns

---

*Generated by TradeMe iOS Architect Agent*
*Part of TradeMe Multi-Agent Development System*

## References

- [🎯 Architecture Quick Reference](.claude/ARCHITECTURE-QUICK-REFERENCE.md)
- [📚 Comprehensive iOS Architecture Guide](specifications/0-foundations/tech-stack-docs/trademe-platform/comprehensive-ios-architecture.md)
- [✅ Architecture Validation Checklist](.claude/validation/trademe-ios-architecture-checklist.md)
"""

        # Save the analysis document
        analysis_filename = f"{context.ticket_id}-architecture-analysis.md"
        analysis_path = self.file_manager.write_specification("architecture", analysis_filename, doc)

        print(f"📋 Architecture analysis saved: {analysis_path}")
        return analysis_path

    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Execute the architect agent workflow."""
        print(f"\n🏛️  === TradeMe iOS Architect Agent ===")
        print(f"Analyzing: {context.ticket_id}")

        # Perform architecture analysis
        analysis = self.analyze_ticket(context)

        # Create and save architecture analysis document
        analysis_path = self.create_architecture_analysis_document(context, analysis)

        print(f"✅ Architecture analysis complete: {analysis_path}")

        # Update context
        context.artifacts["architecture_analysis"] = analysis_path
        context.completed_stages.append(WorkflowStage.ARCHITECTURE_ANALYSIS)
        context.current_stage = WorkflowStage.REQUIREMENTS_RESEARCH

        # Create handoff to researcher
        handoff_summary = f"""
Architecture analysis completed for {context.ticket_id}.

**Key Findings:**
- Compliance status: {len([k for k, v in analysis.compliance_status.items() if v])}/{len(analysis.compliance_status)} aspects compliant
- {len(analysis.integration_patterns)} integration patterns identified
- {len(analysis.recommendations)} recommendations generated
- {len(analysis.constraints)} critical constraints identified

**Critical Constraints:**
{chr(10).join(f"- {constraint}" for constraint in analysis.constraints[:3])}

The ticket appears to require {', '.join(analysis.integration_patterns[:2]) if analysis.integration_patterns else 'standard patterns'}.
"""

        next_actions = [
            "Research existing codebase patterns for similar functionality",
            "Analyze 25,976+ Swift files across 100+ modules for relevant implementations",
            "Create Layer 3 requirements document following 7-layer methodology",
            "Identify legacy integration constraints and bridge patterns",
            "Document platform service dependencies and API requirements"
        ]

        handoff_path = self.handoff_manager.create_handoff(
            AgentRole.ARCHITECT, AgentRole.RESEARCHER,
            context, handoff_summary, next_actions
        )

        print(f"📋 Handoff created: {handoff_path}")
        print(f"🔄 Ready for Research Agent to begin requirements analysis")

        return context

def main():
    """Test the architect agent."""
    if len(sys.argv) < 3:
        print("Usage: python architect.py <ticket_id> <description>")
        sys.exit(1)

    ticket_id = sys.argv[1]
    description = " ".join(sys.argv[2:])

    from shared_utils import create_workflow_context

    context = create_workflow_context(ticket_id, description)
    architect = TradeMeArchitect()

    try:
        result_context = architect.execute(context)
        print(f"\n✅ Architect analysis complete for {ticket_id}")
        print(f"📋 Artifacts: {result_context.artifacts}")
    except Exception as e:
        print(f"❌ Error in architect analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()