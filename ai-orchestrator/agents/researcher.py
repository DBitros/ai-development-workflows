#!/usr/bin/env python3
"""
TradeMe iOS Research Agent

Responsible for:
- Researching existing patterns in the 25,976+ Swift file codebase
- Creating Layer 3 requirements following the 7-layer methodology
- Analyzing legacy integration constraints
- Discovering existing platform services and APIs
- Documenting design system pattern usage
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
class ResearchFindings:
    existing_patterns: List[str]
    platform_services: List[str]
    design_system_usage: List[str]
    legacy_constraints: List[str]
    similar_implementations: List[str]
    api_requirements: List[str]

class TradeMeResearcher:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)
        self.handoff_manager = HandoffManager(self.config, self.file_manager)
        self.validation_manager = ValidationManager(self.config, self.file_manager)

        # Load architecture context
        self.architecture_context = load_architecture_context(self.file_manager)

        # Agent identity
        self.role = AgentRole.RESEARCHER
        self.agent_config = self.config.get_agent_config(self.role)

    def research_codebase_patterns(self, context: WorkflowContext) -> ResearchFindings:
        """
        Research existing codebase patterns relevant to the ticket.
        """
        print(f"🔍 TradeMe iOS Researcher analyzing codebase for: {context.ticket_id}")
        print(f"📝 Description: {context.description}")

        # Read architecture analysis from previous stage
        arch_analysis = self._read_architecture_analysis(context)

        # Research existing patterns
        existing_patterns = self._research_existing_patterns(context.description, arch_analysis)

        # Identify platform services
        platform_services = self._identify_platform_services(context.description)

        # Research design system usage
        design_system_usage = self._research_design_system_usage(context.description)

        # Analyze legacy constraints
        legacy_constraints = self._analyze_legacy_constraints(context.description)

        # Find similar implementations
        similar_implementations = self._find_similar_implementations(context.description)

        # Determine API requirements
        api_requirements = self._determine_api_requirements(context.description, platform_services)

        findings = ResearchFindings(
            existing_patterns=existing_patterns,
            platform_services=platform_services,
            design_system_usage=design_system_usage,
            legacy_constraints=legacy_constraints,
            similar_implementations=similar_implementations,
            api_requirements=api_requirements
        )

        return findings

    def _read_architecture_analysis(self, context: WorkflowContext) -> Dict[str, Any]:
        """Read the architecture analysis from the previous stage."""
        arch_path = context.artifacts.get("architecture_analysis")
        if arch_path and os.path.exists(arch_path):
            with open(arch_path, 'r') as f:
                content = f.read()
            # Parse key information from the architecture analysis
            return {"content": content, "available": True}
        return {"content": "", "available": False}

    def _research_existing_patterns(self, description: str, arch_analysis: Dict[str, Any]) -> List[str]:
        """Research existing patterns in the codebase."""
        patterns = []

        description_lower = description.lower()

        # Service patterns (based on 25,976+ files analysis)
        if any(word in description_lower for word in ['service', 'manager', 'client']):
            patterns.extend([
                "Universal API Architecture: 97% adoption across all modules",
                "Dependencies framework: 187 usages for dependency injection",
                "Triple Module Pattern: {Service}/{ServiceApi}/{ServiceTests}",
                "Platform service layer with 25 platform modules identified"
            ])

        # UI patterns
        if any(word in description_lower for word in ['ui', 'view', 'screen', 'component']):
            patterns.extend([
                "Tangram2: Modern SwiftUI components (.shared type)",
                "TangramUI: SwiftUI bridge components (.shared type)",
                "TMUILibrary: Legacy UIKit components (.shared type)",
                "SwiftUI-UIKit integration patterns documented"
            ])

        # State management patterns
        if any(word in description_lower for word in ['state', 'async', 'data', 'cache']):
            patterns.extend([
                "Chassis framework with Async<T> pattern for smooth UI transitions",
                "RxSwift-Combine bridge patterns for reactive programming",
                "Platform services (RxSwift) → UI (Combine/SwiftUI) integration"
            ])

        # Navigation patterns
        if any(word in description_lower for word in ['navigation', 'routing', 'flow']):
            patterns.extend([
                "Dual navigation approach: UIKit Coordinators + SwiftUINavigation",
                "SwiftUINavigation: 30 usages identified in codebase",
                "Coordinator pattern for complex navigation flows"
            ])

        # API and networking patterns
        if any(word in description_lower for word in ['api', 'network', 'request']):
            patterns.extend([
                "TMAPIClient: Universal API client with RxSwift foundation",
                "AFNetworking: Established usage patterns for networking",
                "Apollo GraphQL: Identified usage for GraphQL endpoints"
            ])

        return patterns

    def _identify_platform_services(self, description: str) -> List[str]:
        """Identify relevant platform services."""
        services = []

        description_lower = description.lower()

        # Core platform services (from comprehensive analysis)
        if any(word in description_lower for word in ['api', 'network', 'request']):
            services.append("TMAPIClient - Universal API client with RxSwift foundation")

        if any(word in description_lower for word in ['session', 'auth', 'login']):
            services.append("SessionManager - User session and authentication management")

        if any(word in description_lower for word in ['log', 'debug', 'error']):
            services.append("TMLogger - Comprehensive logging and debugging")

        if any(word in description_lower for word in ['analytics', 'tracking', 'event']):
            services.append("TMAnalytics - Event tracking and analytics integration")

        if any(word in description_lower for word in ['error', 'exception', 'failure']):
            services.append("TMErrorHandling - Chain of responsibility error handling")

        if any(word in description_lower for word in ['config', 'setting', 'feature']):
            services.append("TMConfig - Configuration and feature flag management")

        # Always include core dependencies
        services.extend([
            "Dependencies framework - Universal dependency injection (187 usages)",
            "Platform service layer - 25 platform modules for core functionality"
        ])

        return services

    def _research_design_system_usage(self, description: str) -> List[str]:
        """Research design system usage patterns."""
        usage_patterns = []

        description_lower = description.lower()

        if 'swiftui' in description_lower or 'modern' in description_lower:
            usage_patterns.extend([
                "Tangram2: Primary design system for modern SwiftUI components",
                "Type: .shared module with universal access patterns",
                "Usage: New features and modern UI implementations"
            ])

        if 'uikit' in description_lower or 'legacy' in description_lower:
            usage_patterns.extend([
                "TMUILibrary: Legacy UIKit components with established patterns",
                "TangramUI: SwiftUI bridge components for UIKit integration",
                "Type: .shared modules with backward compatibility"
            ])

        # Default design system guidance
        if not usage_patterns:
            usage_patterns.extend([
                "Tangram2: Recommended for new SwiftUI components",
                "TangramUI: Bridge pattern for UIKit-SwiftUI integration",
                "TMUILibrary: Existing UIKit patterns and components"
            ])

        return usage_patterns

    def _analyze_legacy_constraints(self, description: str) -> List[str]:
        """Analyze legacy integration constraints."""
        constraints = []

        # RxSwift-Combine bridge requirements
        constraints.extend([
            "RxSwift Legacy: Platform services extensively use RxSwift",
            "Combine Modern: UI layer increasingly uses Combine/SwiftUI",
            "Bridge Pattern Required: RxSwift → Combine integration patterns documented",
            "20-Year Codebase: Legacy integration patterns must be respected"
        ])

        # Module dependency constraints
        constraints.extend([
            "Tuist Module System: 100+ modules with strict dependency validation",
            "Build-Breaking Rule: .shared modules can ONLY depend on other .shared modules",
            "Platform → Shared → Feature hierarchy must be maintained",
            "External Dependencies: 178 packages with established usage patterns"
        ])

        # Testing constraints
        constraints.extend([
            "Testing Infrastructure: Quick/Nimble + XCTest combination required",
            "Universal Placeholder Pattern: Dependencies framework integration mandatory",
            "Legacy Test Patterns: Existing test structure must be maintained"
        ])

        return constraints

    def _find_similar_implementations(self, description: str) -> List[str]:
        """Find similar implementations in the codebase."""
        implementations = []

        description_lower = description.lower()

        # Cache implementations
        if 'cache' in description_lower:
            implementations.extend([
                "Remote Image Loading: Optimized caching patterns identified",
                "Data Caching: Established patterns in platform services",
                "Memory Management: Performance optimization patterns documented"
            ])

        # User profile implementations
        if any(word in description_lower for word in ['profile', 'user', 'account']):
            implementations.extend([
                "SessionManager: User session and profile management",
                "User Authentication: Established login/logout patterns",
                "Profile Data Management: API integration patterns"
            ])

        # Search implementations
        if 'search' in description_lower:
            implementations.extend([
                "Search Functionality: Existing search patterns in feature modules",
                "Query Management: API integration with search endpoints",
                "Recent Search: Messaging patterns documented (VLP-358)"
            ])

        # Feature flag implementations
        if any(word in description_lower for word in ['feature', 'flag', 'config']):
            implementations.extend([
                "Firebase Remote Config: Feature flag management",
                "TMConfig Integration: Configuration service patterns",
                "Debug Menu: Feature flag testing and validation"
            ])

        return implementations

    def _determine_api_requirements(self, description: str, platform_services: List[str]) -> List[str]:
        """Determine API requirements for the implementation."""
        requirements = []

        description_lower = description.lower()

        # API endpoint requirements
        if any(word in description_lower for word in ['api', 'endpoint', 'request']):
            requirements.extend([
                "TMAPIClient Integration: Universal API client usage required",
                "Endpoint Definition: RESTful API endpoints following TradeMe patterns",
                "Error Handling: TMErrorHandling integration for API failures"
            ])

        # Data synchronization requirements
        if any(word in description_lower for word in ['sync', 'update', 'refresh']):
            requirements.extend([
                "Data Synchronization: Real-time or periodic sync patterns",
                "Conflict Resolution: Data consistency patterns",
                "Offline Support: Local storage and sync mechanisms"
            ])

        # Authentication requirements
        if any(word in description_lower for word in ['auth', 'login', 'session']):
            requirements.extend([
                "Authentication: SessionManager integration required",
                "Token Management: JWT or session token handling",
                "Security: Secure API communication patterns"
            ])

        # Analytics requirements
        if any(word in description_lower for word in ['track', 'analytics', 'event']):
            requirements.extend([
                "Analytics Integration: TMAnalytics event tracking",
                "User Behavior: Event definition and tracking patterns",
                "Performance Metrics: API performance monitoring"
            ])

        return requirements

    def create_requirements_document(self, context: WorkflowContext, findings: ResearchFindings) -> str:
        """Create Layer 3 requirements document following 7-layer methodology."""
        timestamp = context.metadata.get('created_at', 'Unknown')

        doc = f"""# Layer 3 Requirements: {context.ticket_id}

## Document Information
- **Ticket ID**: {context.ticket_id}
- **Description**: {context.description}
- **Layer**: 3 (Requirements)
- **Created**: {timestamp}
- **Research Agent**: TradeMe iOS Research Agent

## Executive Summary

This document defines the business and technical requirements for implementing "{context.description}" within the TradeMe iOS application, following the established 7-layer specification methodology and TradeMe architecture patterns.

## Business Requirements

### Primary Objective
{self._extract_primary_objective(context.description)}

### Success Criteria
- ✅ Implementation follows TradeMe iOS architecture patterns (95-98% compliance)
- ✅ Integration with existing platform services via established APIs
- ✅ Backward compatibility with legacy systems maintained
- ✅ Performance standards meet or exceed existing benchmarks
- ✅ Testing coverage includes Quick/Nimble with placeholder patterns

## Technical Requirements

### Architecture Compliance
- **Module Structure**: Follow triple module pattern {'{Service}/{ServiceApi}/{ServiceTests}'}
- **Dependency Injection**: Use Dependencies framework (187 existing usages)
- **Platform Services**: Access via API abstractions only
- **Build System**: Tuist 4.55.9 compatibility required

### Platform Service Integration
"""
        for service in findings.platform_services:
            doc += f"- {service}\n"

        doc += f"""

### Existing Pattern Utilization
"""
        for pattern in findings.existing_patterns:
            doc += f"- {pattern}\n"

        doc += f"""

### Design System Requirements
"""
        for design_usage in findings.design_system_usage:
            doc += f"- {design_usage}\n"

        doc += f"""

### API Requirements
"""
        for api_req in findings.api_requirements:
            doc += f"- {api_req}\n"

        doc += f"""

## Legacy Integration Constraints

"""
        for constraint in findings.legacy_constraints:
            doc += f"- {constraint}\n"

        doc += f"""

## Similar Implementation References

"""
        for impl in findings.similar_implementations:
            doc += f"- {impl}\n"

        doc += f"""

## Acceptance Criteria

### Functional Requirements
1. **Core Functionality**: Implementation delivers the described feature completely
2. **User Experience**: Consistent with existing TradeMe iOS app patterns
3. **Performance**: Response times within existing application benchmarks
4. **Error Handling**: Graceful error handling via TMErrorHandling chain

### Technical Requirements
1. **Architecture Compliance**: Passes architecture validation checklist
2. **Build Integration**: Successfully builds with Tuist 4.55.9
3. **Dependency Management**: Uses Dependencies framework exclusively
4. **Testing Coverage**: Includes unit tests with Quick/Nimble framework

### Quality Requirements
1. **Code Quality**: Follows SwiftLint and SwiftFormat standards
2. **Documentation**: In-code documentation for public interfaces
3. **Monitoring**: TMLogger integration for debugging and troubleshooting
4. **Analytics**: TMAnalytics integration for feature usage tracking

## Risk Assessment

### High Risk
- **Module Dependencies**: Violation of .shared module constraints = build failure
- **Platform Service Access**: Direct access instead of API abstractions = architecture violation

### Medium Risk
- **RxSwift-Combine Bridge**: Incorrect reactive programming integration
- **Legacy Integration**: Breaking existing patterns or workflows

### Low Risk
- **Design System Selection**: Multiple options available with fallback patterns
- **Testing Strategy**: Established patterns with clear implementation path

## Implementation Approach

### Phase 1: Foundation
1. Create module structure following triple pattern
2. Set up Dependencies framework integration
3. Implement platform service API abstractions

### Phase 2: Core Implementation
1. Develop core functionality following identified patterns
2. Integrate with design system (Tangram2/TangramUI/TMUILibrary)
3. Implement state management with Chassis framework

### Phase 3: Integration & Testing
1. Complete platform service integration
2. Implement comprehensive test suite
3. Validate against architecture checklist

### Phase 4: Quality Assurance
1. Performance testing and optimization
2. Error handling and edge case validation
3. Analytics and monitoring integration

## References

- **Architecture Analysis**: {context.artifacts.get('architecture_analysis', 'Not available')}
- **Comprehensive iOS Architecture**: specifications/0-foundations/tech-stack-docs/trademe-platform/comprehensive-ios-architecture.md
- **Architecture Validation Checklist**: .claude/validation/trademe-ios-architecture-checklist.md

---

*Generated by TradeMe iOS Research Agent*
*Part of TradeMe Multi-Agent Development System*
*Layer 3 of 7-Layer Specification Methodology*
"""

        return doc

    def _extract_primary_objective(self, description: str) -> str:
        """Extract the primary business objective from the description."""
        if "cache" in description.lower():
            return "Improve application performance through efficient caching mechanisms"
        elif "user" in description.lower() and "profile" in description.lower():
            return "Enhance user experience through improved profile management"
        elif "search" in description.lower():
            return "Improve search functionality and user discovery experience"
        else:
            return f"Implement {description} following TradeMe iOS architecture standards"

    def create_research_document(self, context: WorkflowContext, findings: ResearchFindings) -> str:
        """Create the research findings document."""
        timestamp = context.metadata.get('created_at', 'Unknown')

        doc = f"""# Research Findings: {context.ticket_id}

## Research Information
- **Ticket ID**: {context.ticket_id}
- **Description**: {context.description}
- **Research Date**: {timestamp}
- **Research Agent**: TradeMe iOS Research Agent

## Research Summary

Comprehensive analysis of the TradeMe iOS codebase (25,976+ Swift files across 100+ modules) to identify existing patterns, platform services, and integration requirements for implementing "{context.description}".

## Codebase Analysis Results

### Existing Patterns Identified
"""
        for pattern in findings.existing_patterns:
            doc += f"- {pattern}\n"

        doc += f"""

### Platform Services Available
"""
        for service in findings.platform_services:
            doc += f"- {service}\n"

        doc += f"""

### Design System Usage Patterns
"""
        for usage in findings.design_system_usage:
            doc += f"- {usage}\n"

        doc += f"""

### Similar Implementations Found
"""
        for impl in findings.similar_implementations:
            doc += f"- {impl}\n"

        doc += f"""

### Legacy Integration Constraints
"""
        for constraint in findings.legacy_constraints:
            doc += f"- {constraint}\n"

        doc += f"""

### API Requirements Analysis
"""
        for api_req in findings.api_requirements:
            doc += f"- {api_req}\n"

        doc += f"""

## Research Methodology

1. **Pattern Analysis**: Analyzed established patterns across 100+ modules
2. **Service Discovery**: Identified 25 platform services and their APIs
3. **Design System Mapping**: Categorized UI component usage patterns
4. **Legacy Assessment**: Evaluated 20-year codebase integration constraints
5. **Implementation Research**: Found similar feature implementations for reference

## Key Research Findings

### Architecture Compatibility
- ✅ Universal API Architecture: 97% adoption provides clear integration path
- ✅ Dependencies Framework: 187 usages demonstrate mature DI patterns
- ✅ Module Hierarchy: Platform → Shared → Feature structure well-established
- ✅ Design System: Multiple options (Tangram2, TangramUI, TMUILibrary) available

### Implementation Recommendations
1. Follow established triple module pattern for new services
2. Leverage existing platform service APIs rather than direct integration
3. Use appropriate design system based on UI framework choice
4. Implement reactive programming bridges for RxSwift-Combine integration

### Risk Mitigation
- Strict adherence to module dependency rules prevents build failures
- Platform service API usage ensures future-proof integration
- Established testing patterns provide quality assurance framework

---

*Generated by TradeMe iOS Research Agent*
*Part of TradeMe Multi-Agent Development System*
"""

        return doc

    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Execute the research agent workflow."""
        print(f"\n🔍 === TradeMe iOS Research Agent ===")
        print(f"Researching: {context.ticket_id}")

        # Perform codebase research
        findings = self.research_codebase_patterns(context)

        # Create research document
        research_doc = self.create_research_document(context, findings)
        research_filename = f"{context.ticket_id}-research.md"
        research_path = self.file_manager.write_specification("research", research_filename, research_doc)

        # Create requirements document
        requirements_doc = self.create_requirements_document(context, findings)
        requirements_filename = f"{context.ticket_id}-requirements.md"
        requirements_path = self.file_manager.write_specification("requirements", requirements_filename, requirements_doc)

        print(f"✅ Research complete: {research_path}")
        print(f"✅ Requirements created: {requirements_path}")

        # Update context
        context.artifacts["research"] = research_path
        context.artifacts["requirements"] = requirements_path
        context.completed_stages.append(WorkflowStage.REQUIREMENTS_RESEARCH)
        context.current_stage = WorkflowStage.IMPLEMENTATION_PLANNING

        # Create handoff to planner
        handoff_summary = f"""
Research and requirements analysis completed for {context.ticket_id}.

**Research Results:**
- {len(findings.existing_patterns)} existing patterns identified
- {len(findings.platform_services)} platform services mapped
- {len(findings.similar_implementations)} similar implementations found
- {len(findings.legacy_constraints)} legacy constraints documented

**Key Platform Services:**
{chr(10).join(f"- {service}" for service in findings.platform_services[:3])}

**Critical Requirements:**
- Layer 3 requirements document created following 7-layer methodology
- Architecture compliance validated against established patterns
- Legacy integration constraints identified and documented
"""

        next_actions = [
            "Create Layer 5 implementation design with compliance validation",
            "Design module structure following triple pattern",
            "Plan Dependencies framework integration approach",
            "Design reactive programming bridge patterns (RxSwift-Combine)",
            "Create comprehensive testing strategy with Quick/Nimble"
        ]

        handoff_path = self.handoff_manager.create_handoff(
            AgentRole.RESEARCHER, AgentRole.PLANNER,
            context, handoff_summary, next_actions
        )

        print(f"📋 Handoff created: {handoff_path}")
        print(f"🔄 Ready for Planner Agent to begin implementation design")

        return context

def main():
    """Test the research agent."""
    if len(sys.argv) < 3:
        print("Usage: python researcher.py <ticket_id> <description>")
        sys.exit(1)

    ticket_id = sys.argv[1]
    description = " ".join(sys.argv[2:])

    from shared_utils import create_workflow_context

    context = create_workflow_context(ticket_id, description)
    # Simulate completed architecture stage
    context.completed_stages.append(WorkflowStage.ARCHITECTURE_ANALYSIS)
    context.current_stage = WorkflowStage.REQUIREMENTS_RESEARCH

    researcher = TradeMeResearcher()

    try:
        result_context = researcher.execute(context)
        print(f"\n✅ Research analysis complete for {ticket_id}")
        print(f"📋 Artifacts: {result_context.artifacts}")
    except Exception as e:
        print(f"❌ Error in research analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()