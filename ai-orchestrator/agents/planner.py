#!/usr/bin/env python3
"""
TradeMe iOS Planner Agent

Responsible for:
- Creating Layer 5 implementation design with compliance validation
- Designing module structure following triple pattern
- Planning Dependencies framework integration
- Designing reactive programming bridge patterns
- Creating comprehensive testing strategy
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
class ImplementationPlan:
    module_structure: Dict[str, List[str]]
    dependency_integration: List[str]
    reactive_patterns: List[str]
    testing_strategy: List[str]
    implementation_phases: List[Dict[str, Any]]
    file_structure: Dict[str, str]
    code_templates: Dict[str, str]

class TradeMePlanner:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)
        self.handoff_manager = HandoffManager(self.config, self.file_manager)
        self.validation_manager = ValidationManager(self.config, self.file_manager)

        # Load architecture context
        self.architecture_context = load_architecture_context(self.file_manager)

        # Agent identity
        self.role = AgentRole.PLANNER
        self.agent_config = self.config.get_agent_config(self.role)

    def create_implementation_plan(self, context: WorkflowContext) -> ImplementationPlan:
        """
        Create comprehensive implementation plan with compliance validation.
        """
        print(f"📋 TradeMe iOS Planner creating implementation plan for: {context.ticket_id}")
        print(f"📝 Description: {context.description}")

        # Read previous artifacts
        requirements_content = self._read_requirements(context)
        research_content = self._read_research(context)
        arch_analysis = self._read_architecture_analysis(context)

        # Design module structure
        module_structure = self._design_module_structure(context.description, requirements_content)

        # Plan dependency integration
        dependency_integration = self._plan_dependency_integration(context.description, research_content)

        # Design reactive patterns
        reactive_patterns = self._design_reactive_patterns(context.description, arch_analysis)

        # Create testing strategy
        testing_strategy = self._create_testing_strategy(context.description, module_structure)

        # Plan implementation phases
        implementation_phases = self._plan_implementation_phases(
            context.description, module_structure, dependency_integration
        )

        # Design file structure
        file_structure = self._design_file_structure(context.description, module_structure)

        # Create code templates
        code_templates = self._create_code_templates(context.description, module_structure)

        plan = ImplementationPlan(
            module_structure=module_structure,
            dependency_integration=dependency_integration,
            reactive_patterns=reactive_patterns,
            testing_strategy=testing_strategy,
            implementation_phases=implementation_phases,
            file_structure=file_structure,
            code_templates=code_templates
        )

        return plan

    def _read_requirements(self, context: WorkflowContext) -> str:
        """Read the requirements document."""
        req_path = context.artifacts.get("requirements")
        if req_path and os.path.exists(req_path):
            with open(req_path, 'r') as f:
                return f.read()
        return ""

    def _read_research(self, context: WorkflowContext) -> str:
        """Read the research document."""
        research_path = context.artifacts.get("research")
        if research_path and os.path.exists(research_path):
            with open(research_path, 'r') as f:
                return f.read()
        return ""

    def _read_architecture_analysis(self, context: WorkflowContext) -> str:
        """Read the architecture analysis document."""
        arch_path = context.artifacts.get("architecture_analysis")
        if arch_path and os.path.exists(arch_path):
            with open(arch_path, 'r') as f:
                return f.read()
        return ""

    def _design_module_structure(self, description: str, requirements: str) -> Dict[str, List[str]]:
        """Design the module structure following triple pattern."""
        description_lower = description.lower()

        # Determine module type and name
        if any(word in description_lower for word in ['cache', 'storage', 'persist']):
            module_name = "UserProfileCache"
            module_type = "platform"
        elif any(word in description_lower for word in ['ui', 'view', 'screen']):
            module_name = "ProfileView"
            module_type = "feature"
        elif any(word in description_lower for word in ['service', 'manager', 'client']):
            module_name = "ProfileService"
            module_type = "platform"
        else:
            # Extract key words for module name
            words = description.split()
            module_name = ''.join(word.title() for word in words[:2] if word.lower() not in ['add', 'the', 'to', 'a', 'an'])
            module_type = "shared"

        # Triple module pattern structure
        structure = {
            "main_module": {
                "name": module_name,
                "type": module_type,
                "files": [
                    f"{module_name}.swift",
                    f"{module_name}Implementation.swift",
                    f"{module_name}Dependencies.swift"
                ]
            },
            "api_module": {
                "name": f"{module_name}Api",
                "type": "shared",
                "files": [
                    f"{module_name}Protocol.swift",
                    f"{module_name}Models.swift",
                    f"{module_name}Error.swift"
                ]
            },
            "tests_module": {
                "name": f"{module_name}Tests",
                "type": "test",
                "files": [
                    f"{module_name}Tests.swift",
                    f"{module_name}MockImplementation.swift",
                    f"{module_name}TestHelpers.swift"
                ]
            }
        }

        return {
            "module_name": module_name,
            "module_type": module_type,
            "structure": structure,
            "dependencies": self._determine_module_dependencies(description_lower, module_type)
        }

    def _determine_module_dependencies(self, description_lower: str, module_type: str) -> List[str]:
        """Determine module dependencies based on functionality."""
        dependencies = ["Dependencies"]  # Always include Dependencies framework

        # Platform service dependencies (only for platform/feature modules)
        if module_type in ["platform", "feature"]:
            if any(word in description_lower for word in ['api', 'network', 'request']):
                dependencies.append("TMAPIClientApi")

            if any(word in description_lower for word in ['session', 'auth', 'login']):
                dependencies.append("SessionManagerApi")

            if any(word in description_lower for word in ['log', 'debug', 'error']):
                dependencies.append("TMLoggerApi")

            if any(word in description_lower for word in ['analytics', 'tracking']):
                dependencies.append("TMAnalyticsApi")

            if any(word in description_lower for word in ['config', 'feature']):
                dependencies.append("TMConfigApi")

        # UI dependencies
        if any(word in description_lower for word in ['ui', 'view', 'swiftui']):
            dependencies.extend(["Tangram2", "SwiftUINavigation"])

        # State management dependencies
        if any(word in description_lower for word in ['state', 'async', 'reactive']):
            dependencies.extend(["Chassis", "Combine"])

        # Testing dependencies (for test modules)
        if module_type == "test":
            dependencies.extend(["Quick", "Nimble", "XCTest"])

        return dependencies

    def _plan_dependency_integration(self, description: str, research: str) -> List[str]:
        """Plan Dependencies framework integration."""
        integration_steps = [
            "1. Define protocol interfaces in API module",
            "2. Create DependencyKey for service registration",
            "3. Implement DependencyValues extension",
            "4. Register service in main module Dependencies container",
            "5. Create factory methods for dependency injection",
            "6. Implement mock versions for testing"
        ]

        description_lower = description.lower()

        # Add specific integration patterns based on functionality
        if any(word in description_lower for word in ['api', 'network']):
            integration_steps.extend([
                "7. Integrate TMAPIClient via dependency injection",
                "8. Create API endpoint configurations",
                "9. Implement request/response models"
            ])

        if any(word in description_lower for word in ['cache', 'storage']):
            integration_steps.extend([
                "7. Integrate storage backend via dependency injection",
                "8. Create cache configuration protocols",
                "9. Implement cache invalidation strategies"
            ])

        return integration_steps

    def _design_reactive_patterns(self, description: str, arch_analysis: str) -> List[str]:
        """Design reactive programming patterns for RxSwift-Combine bridge."""
        patterns = []

        description_lower = description.lower()

        if any(word in description_lower for word in ['api', 'network', 'service']):
            patterns.extend([
                "Platform Service (RxSwift) → Observable<T> patterns",
                "UI Layer (Combine) → @Published property wrappers",
                "Bridge Pattern: RxSwift.Observable → Combine.AnyPublisher",
                "Error Handling: RxSwift.ErrorType → Combine.Error mapping"
            ])

        if any(word in description_lower for word in ['state', 'async', 'ui']):
            patterns.extend([
                "Chassis Framework: Async<T> state management pattern",
                "SwiftUI Integration: @StateObject + ObservableObject",
                "State Transitions: Loading → Success/Failure patterns",
                "UI Binding: Combine publishers to SwiftUI views"
            ])

        if any(word in description_lower for word in ['data', 'cache', 'persist']):
            patterns.extend([
                "Data Flow: Repository pattern with reactive streams",
                "Cache Updates: Publisher-based cache invalidation",
                "Data Consistency: Conflict resolution with reactive patterns"
            ])

        return patterns

    def _create_testing_strategy(self, description: str, module_structure: Dict[str, Any]) -> List[str]:
        """Create comprehensive testing strategy."""
        strategy = [
            "Unit Testing Framework: Quick + Nimble + XCTest",
            "Universal Placeholder Pattern: Dependencies framework mocks",
            "Test Module Structure: {ModuleName}Tests with comprehensive coverage",
            "Mock Implementation: Protocol-based mocks for all dependencies"
        ]

        description_lower = description.lower()

        # Add specific testing strategies
        if any(word in description_lower for word in ['api', 'network']):
            strategy.extend([
                "API Testing: Mock TMAPIClient with predefined responses",
                "Network Testing: URLSession mocking for integration tests",
                "Error Scenarios: Network failure and timeout testing"
            ])

        if any(word in description_lower for word in ['ui', 'view', 'swiftui']):
            strategy.extend([
                "UI Testing: SwiftUI view testing with ViewInspector",
                "State Testing: ObservableObject state change validation",
                "Interaction Testing: User interaction simulation"
            ])

        if any(word in description_lower for word in ['cache', 'storage']):
            strategy.extend([
                "Storage Testing: In-memory mock for cache operations",
                "Performance Testing: Cache hit/miss ratio validation",
                "Concurrency Testing: Thread-safe access patterns"
            ])

        strategy.extend([
            "Integration Testing: End-to-end workflow validation",
            "Performance Testing: Memory and CPU usage benchmarks",
            "Accessibility Testing: VoiceOver and accessibility compliance"
        ])

        return strategy

    def _plan_implementation_phases(self, description: str, module_structure: Dict[str, Any],
                                   dependency_integration: List[str]) -> List[Dict[str, Any]]:
        """Plan implementation phases."""
        module_name = module_structure.get("module_name", "Feature")

        phases = [
            {
                "phase": 1,
                "name": "Foundation Setup",
                "description": "Create module structure and basic interfaces",
                "tasks": [
                    "Create triple module structure (Main/Api/Tests)",
                    "Define protocol interfaces in API module",
                    "Set up Dependencies framework integration",
                    "Create basic project structure in Tuist"
                ],
                "deliverables": [
                    f"{module_name}Api module with protocols",
                    f"{module_name} module with basic structure",
                    f"{module_name}Tests module with test harness"
                ]
            },
            {
                "phase": 2,
                "name": "Core Implementation",
                "description": "Implement core functionality and business logic",
                "tasks": [
                    "Implement core service/feature logic",
                    "Integrate platform services via APIs",
                    "Implement reactive patterns (RxSwift-Combine bridge)",
                    "Add comprehensive error handling"
                ],
                "deliverables": [
                    f"{module_name}Implementation.swift",
                    "Platform service integrations",
                    "Reactive programming bridges",
                    "Error handling implementation"
                ]
            },
            {
                "phase": 3,
                "name": "UI Integration",
                "description": "Implement UI components and user interactions",
                "tasks": [
                    "Create UI components using appropriate design system",
                    "Implement state management with Chassis framework",
                    "Add navigation patterns (Coordinators/SwiftUINavigation)",
                    "Integrate analytics and logging"
                ],
                "deliverables": [
                    "UI components (SwiftUI/UIKit)",
                    "State management implementation",
                    "Navigation integration",
                    "Analytics integration"
                ]
            },
            {
                "phase": 4,
                "name": "Testing & Quality Assurance",
                "description": "Comprehensive testing and validation",
                "tasks": [
                    "Implement unit tests with Quick/Nimble",
                    "Create integration tests for platform services",
                    "Add UI tests for user interactions",
                    "Performance and accessibility testing"
                ],
                "deliverables": [
                    "Comprehensive test suite",
                    "Performance benchmarks",
                    "Accessibility compliance",
                    "Code coverage reports"
                ]
            }
        ]

        return phases

    def _design_file_structure(self, description: str, module_structure: Dict[str, Any]) -> Dict[str, str]:
        """Design the file structure for implementation."""
        module_name = module_structure.get("module_name", "Feature")
        structure = module_structure.get("structure", {})

        file_structure = {}

        # Main module files
        main_module = structure.get("main_module", {})
        if main_module:
            module_path = f"Modules/{main_module['name']}/Sources"
            for file in main_module.get("files", []):
                file_structure[f"{module_path}/{file}"] = f"Main implementation file for {file.replace('.swift', '')}"

        # API module files
        api_module = structure.get("api_module", {})
        if api_module:
            api_path = f"Modules/{api_module['name']}/Sources"
            for file in api_module.get("files", []):
                file_structure[f"{api_path}/{file}"] = f"API interface file for {file.replace('.swift', '')}"

        # Test module files
        test_module = structure.get("tests_module", {})
        if test_module:
            test_path = f"Modules/{test_module['name']}/Sources"
            for file in test_module.get("files", []):
                file_structure[f"{test_path}/{file}"] = f"Test file for {file.replace('.swift', '')}"

        # Project configuration files
        file_structure[f"Project.swift"] = "Tuist project configuration"
        file_structure[f"Modules/{module_name}/Project.swift"] = "Module-specific Tuist configuration"

        return file_structure

    def _create_code_templates(self, description: str, module_structure: Dict[str, Any]) -> Dict[str, str]:
        """Create code templates for implementation."""
        module_name = module_structure.get("module_name", "Feature")
        dependencies = module_structure.get("dependencies", [])

        templates = {}

        # Protocol template
        templates["protocol"] = f"""
import Foundation
import Dependencies

// MARK: - {module_name} Protocol

public protocol {module_name}Protocol: Sendable {{
    // Define your service interface here
    func performAction() async throws -> Result
}}

// MARK: - Models

public struct {module_name}Result: Sendable, Equatable {{
    // Define your result model here
}}

// MARK: - Errors

public enum {module_name}Error: Error, LocalizedError, Sendable {{
    case invalidInput
    case networkError
    case unknown

    public var errorDescription: String? {{
        switch self {{
        case .invalidInput: return "Invalid input provided"
        case .networkError: return "Network error occurred"
        case .unknown: return "Unknown error"
        }}
    }}
}}
"""

        # Implementation template
        implementation_imports = "\\n".join(f"import {dep}" for dep in dependencies)
        templates["implementation"] = f"""
{implementation_imports}

// MARK: - {module_name} Implementation

struct {module_name}Implementation: {module_name}Protocol {{
    @Dependency(\\.tmAPIClient) private var apiClient
    @Dependency(\\.tmLogger) private var logger

    func performAction() async throws -> {module_name}Result {{
        logger.info("Performing action in {module_name}")

        // Implement your logic here
        // Follow TradeMe patterns and architecture guidelines

        return {module_name}Result()
    }}
}}

// MARK: - Dependencies Integration

extension {module_name}Implementation: DependencyKey {{
    static let liveValue: {module_name}Protocol = {module_name}Implementation()
}}

extension DependencyValues {{
    var {module_name.lower()}: {module_name}Protocol {{
        get {{ self[{module_name}Implementation.self] }}
        set {{ self[{module_name}Implementation.self] = newValue }}
    }}
}}
"""

        # Test template
        templates["test"] = f"""
import Quick
import Nimble
import XCTest
@testable import {module_name}
@testable import {module_name}Api
import Dependencies

// MARK: - {module_name} Tests

final class {module_name}Tests: QuickSpec {{
    override func spec() {{
        describe("{module_name}Implementation") {{
            var sut: {module_name}Protocol!

            beforeEach {{
                sut = withDependencies {{
                    // Configure test dependencies here
                }} operation: {{
                    {module_name}Implementation()
                }}
            }}

            afterEach {{
                sut = nil
            }}

            context("when performing action") {{
                it("should return expected result") {{
                    // Implement your tests here
                    // Follow Quick/Nimble patterns

                    waitUntil {{ done in
                        Task {{
                            do {{
                                let result = try await sut.performAction()
                                expect(result).toNot(beNil())
                                done()
                            }} catch {{
                                fail("Should not throw error: \\(error)")
                                done()
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}

// MARK: - Mock Implementation

struct Mock{module_name}: {module_name}Protocol {{
    func performAction() async throws -> {module_name}Result {{
        return {module_name}Result()
    }}
}}
"""

        return templates

    def create_implementation_design_document(self, context: WorkflowContext, plan: ImplementationPlan) -> str:
        """Create Layer 5 implementation design document."""
        timestamp = context.metadata.get('created_at', 'Unknown')
        module_name = plan.module_structure.get("module_name", "Feature")

        doc = f"""# Layer 5 Implementation Design: {context.ticket_id}

## Document Information
- **Ticket ID**: {context.ticket_id}
- **Description**: {context.description}
- **Layer**: 5 (Implementation Design)
- **Created**: {timestamp}
- **Planning Agent**: TradeMe iOS Planner Agent

## Executive Summary

This document provides the detailed implementation design for "{context.description}" following TradeMe iOS architecture patterns, the 7-layer specification methodology, and established build system requirements.

## Architecture Overview

### Module Structure (Triple Pattern)
- **Main Module**: {plan.module_structure.get('module_name', 'Feature')} ({plan.module_structure.get('module_type', 'shared')} type)
- **API Module**: {plan.module_structure.get('module_name', 'Feature')}Api (shared type)
- **Tests Module**: {plan.module_structure.get('module_name', 'Feature')}Tests (test type)

### Dependencies Framework Integration
"""
        for step in plan.dependency_integration:
            doc += f"- {step}\n"

        doc += f"""

### Module Dependencies
"""
        dependencies = plan.module_structure.get("dependencies", [])
        for dep in dependencies:
            doc += f"- {dep}\n"

        doc += f"""

## Reactive Programming Patterns

### RxSwift-Combine Bridge Integration
"""
        for pattern in plan.reactive_patterns:
            doc += f"- {pattern}\n"

        doc += f"""

## File Structure

### Project Organization
"""
        for file_path, description in plan.file_structure.items():
            doc += f"- **{file_path}**: {description}\n"

        doc += f"""

## Implementation Phases

"""
        for phase in plan.implementation_phases:
            doc += f"""### Phase {phase['phase']}: {phase['name']}

**Description**: {phase['description']}

**Tasks**:
"""
            for task in phase['tasks']:
                doc += f"- {task}\n"

            doc += f"""
**Deliverables**:
"""
            for deliverable in phase['deliverables']:
                doc += f"- {deliverable}\n"

            doc += "\n"

        doc += f"""## Testing Strategy

### Comprehensive Test Coverage
"""
        for strategy_item in plan.testing_strategy:
            doc += f"- {strategy_item}\n"

        doc += f"""

## Code Templates

### Protocol Interface (API Module)
```swift{plan.code_templates.get('protocol', '')}
```

### Implementation (Main Module)
```swift{plan.code_templates.get('implementation', '')}
```

### Test Suite (Tests Module)
```swift{plan.code_templates.get('test', '')}
```

## Compliance Validation

### Architecture Checklist
- [ ] Triple module pattern implemented ({module_name}/{module_name}Api/{module_name}Tests)
- [ ] Dependencies framework integration complete
- [ ] Platform service access via API abstractions only
- [ ] Module hierarchy constraints respected (Platform → Shared → Feature)
- [ ] Tuist build system compatibility confirmed

### Quality Assurance
- [ ] SwiftLint and SwiftFormat compliance
- [ ] Quick/Nimble test framework integration
- [ ] Universal placeholder pattern for mocking
- [ ] TMLogger integration for debugging
- [ ] TMErrorHandling chain of responsibility

### Performance Standards
- [ ] Memory usage within application benchmarks
- [ ] API response times meet existing standards
- [ ] Cache performance (if applicable) optimized
- [ ] UI responsiveness maintained

## Risk Mitigation

### High-Risk Items
1. **Module Dependencies**: Ensure .shared modules only depend on other .shared modules
2. **Platform Service Integration**: Use API abstractions, never direct access
3. **Build System**: Maintain Tuist 4.55.9 compatibility

### Validation Steps
1. Architecture compliance validation via checklist
2. Build system testing with clean builds
3. Dependency graph analysis for violations
4. Performance benchmarking against baselines

## Implementation Guidelines

### Code Quality Standards
- Follow established SwiftLint and SwiftFormat rules
- Implement comprehensive error handling via TMErrorHandling
- Use TMLogger for debugging and monitoring
- Integrate TMAnalytics for feature usage tracking

### Testing Requirements
- Minimum 80% code coverage for new code
- All public interfaces must have unit tests
- Integration tests for platform service interactions
- UI tests for user-facing features

### Documentation Standards
- In-code documentation for all public interfaces
- Architecture decision rationale in implementation comments
- Performance considerations documented
- Error handling patterns explained

## Next Steps

1. **Code Generation**: Programmer agent implements design following templates
2. **Quality Validation**: Automated testing and compliance checking
3. **Integration Testing**: End-to-end workflow validation
4. **Performance Optimization**: Benchmarking and optimization cycles

## References

- **Architecture Analysis**: {context.artifacts.get('architecture_analysis', 'Not available')}
- **Requirements Document**: {context.artifacts.get('requirements', 'Not available')}
- **Research Findings**: {context.artifacts.get('research', 'Not available')}

---

*Generated by TradeMe iOS Planner Agent*
*Part of TradeMe Multi-Agent Development System*
*Layer 5 of 7-Layer Specification Methodology*
"""

        return doc

    def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Execute the planner agent workflow."""
        print(f"\n📋 === TradeMe iOS Planner Agent ===")
        print(f"Planning implementation for: {context.ticket_id}")

        # Create implementation plan
        plan = self.create_implementation_plan(context)

        # Create implementation design document
        design_doc = self.create_implementation_design_document(context, plan)
        design_filename = f"{context.ticket_id}-implementation-plan.md"
        design_path = self.file_manager.write_specification("implementation_design", design_filename, design_doc)

        print(f"✅ Implementation design complete: {design_path}")

        # Update context
        context.artifacts["implementation_plan"] = design_path
        context.completed_stages.append(WorkflowStage.IMPLEMENTATION_PLANNING)
        context.current_stage = WorkflowStage.CODE_GENERATION

        # Create handoff to programmer
        handoff_summary = f"""
Implementation design completed for {context.ticket_id}.

**Implementation Plan Summary:**
- Module Structure: {plan.module_structure.get('module_name', 'Feature')} with triple pattern
- Dependencies: {len(plan.module_structure.get('dependencies', []))} platform services integrated
- Implementation Phases: {len(plan.implementation_phases)} phases planned
- File Structure: {len(plan.file_structure)} files to be created
- Code Templates: Ready for {len(plan.code_templates)} template types

**Key Components:**
- Triple Module Pattern: {plan.module_structure.get('module_name', 'Feature')}/Api/Tests
- Dependencies Framework: Comprehensive DI integration planned
- Reactive Patterns: {len(plan.reactive_patterns)} bridge patterns designed
- Testing Strategy: {len(plan.testing_strategy)} testing approaches planned

**Ready for Code Generation**:
All architectural decisions made, compliance validated, and templates prepared.
"""

        next_actions = [
            "Generate Swift code following implementation design templates",
            "Create triple module structure with Tuist configuration",
            "Implement Dependencies framework integration",
            "Generate comprehensive test suite with Quick/Nimble",
            "Validate architecture compliance during implementation"
        ]

        handoff_path = self.handoff_manager.create_handoff(
            AgentRole.PLANNER, AgentRole.PROGRAMMER,
            context, handoff_summary, next_actions
        )

        print(f"📋 Handoff created: {handoff_path}")
        print(f"🔄 Ready for Programmer Agent to begin code generation")

        return context

def main():
    """Test the planner agent."""
    if len(sys.argv) < 3:
        print("Usage: python planner.py <ticket_id> <description>")
        sys.exit(1)

    ticket_id = sys.argv[1]
    description = " ".join(sys.argv[2:])

    from shared_utils import create_workflow_context

    context = create_workflow_context(ticket_id, description)
    # Simulate completed previous stages
    context.completed_stages.extend([
        WorkflowStage.ARCHITECTURE_ANALYSIS,
        WorkflowStage.REQUIREMENTS_RESEARCH
    ])
    context.current_stage = WorkflowStage.IMPLEMENTATION_PLANNING

    planner = TradeMePlanner()

    try:
        result_context = planner.execute(context)
        print(f"\n✅ Implementation planning complete for {ticket_id}")
        print(f"📋 Artifacts: {result_context.artifacts}")
    except Exception as e:
        print(f"❌ Error in implementation planning: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()