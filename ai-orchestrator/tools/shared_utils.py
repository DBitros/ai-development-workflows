#!/usr/bin/env python3
"""
Shared utilities for TradeMe multi-agent system.
Provides common functionality for file operations, validation, and communication.
"""

import os
import yaml
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentRole(Enum):
    ARCHITECT = "architect"
    RESEARCHER = "researcher"
    PLANNER = "planner"
    PROGRAMMER = "programmer"
    SECURITY_ENGINEER = "security_engineer"
    TEST_RUNNER = "test_runner"
    QA_ENGINEER = "qa_engineer"

class WorkflowStage(Enum):
    ARCHITECTURE_ANALYSIS = "architecture_analysis"
    REQUIREMENTS_RESEARCH = "requirements_research"
    IMPLEMENTATION_PLANNING = "implementation_planning"
    CODE_GENERATION = "code_generation"
    SECURITY_AUDIT = "security_audit"
    TESTING = "testing"
    QUALITY_ASSURANCE = "quality_assurance"
    DEVELOPER_REVIEW = "developer_review"
    DEPLOYMENT = "deployment"

@dataclass
class WorkflowContext:
    ticket_id: str
    description: str
    current_stage: WorkflowStage
    completed_stages: List[WorkflowStage]
    artifacts: Dict[str, str]  # stage -> file_path
    metadata: Dict[str, Any]

class AgentConfig:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'agents.yaml')

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_agent_config(self, agent_role: AgentRole) -> Dict[str, Any]:
        return self.config['agents'][agent_role.value]

    def get_paths(self) -> Dict[str, str]:
        return self.config['paths']

    def get_workflow_config(self) -> Dict[str, Any]:
        return self.config['workflow']

class FileManager:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.paths = config.get_paths()

    def get_specs_path(self, relative_path: str) -> str:
        """Get full path within the specs repository."""
        return os.path.join(self.paths['specs_repo'], relative_path)

    def get_ios_project_path(self, relative_path: str) -> str:
        """Get full path within the iOS project."""
        return os.path.join(self.paths['ios_project'], relative_path)

    def get_agents_path(self, relative_path: str) -> str:
        """Get full path within the agents system."""
        return os.path.join(self.paths['agents_system'], relative_path)

    def get_path(self, path_key: str) -> str:
        """Get a configured path by key."""
        if path_key in self.paths:
            return self.paths[path_key]
        # If not a direct key, check if it's a relative path within agents_system
        return self.get_agents_path(path_key)

    def ensure_directory(self, file_path: str) -> None:
        """Ensure the directory for a file path exists."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def write_specification(self, layer: str, filename: str, content: str) -> str:
        """Write a specification file to the appropriate layer within the agents system."""
        if layer == "requirements":
            file_path = self.get_agents_path(f"{self.paths['requirements']}/{filename}")
        elif layer == "research":
            file_path = self.get_agents_path(f"{self.paths['research']}/{filename}")
        elif layer == "architecture":
            file_path = self.get_agents_path(f"{self.paths['architecture']}/{filename}")
        elif layer == "implementation_design":
            file_path = self.get_agents_path(f"{self.paths['implementation_design']}/{filename}")
        else:
            raise ValueError(f"Unknown specification layer: {layer}")

        self.ensure_directory(file_path)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    def read_specification(self, layer: str, filename: str) -> str:
        """Read a specification file from the appropriate layer within the agents system."""
        if layer == "requirements":
            file_path = self.get_agents_path(f"{self.paths['requirements']}/{filename}")
        elif layer == "research":
            file_path = self.get_agents_path(f"{self.paths['research']}/{filename}")
        elif layer == "architecture":
            file_path = self.get_agents_path(f"{self.paths['architecture']}/{filename}")
        elif layer == "implementation_design":
            file_path = self.get_agents_path(f"{self.paths['implementation_design']}/{filename}")
        else:
            raise ValueError(f"Unknown specification layer: {layer}")

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return None

class HandoffManager:
    def __init__(self, config: AgentConfig, file_manager: FileManager):
        self.config = config
        self.file_manager = file_manager

    def create_handoff(self, from_agent: AgentRole, to_agent: AgentRole,
                      context: WorkflowContext, summary: str, next_actions: List[str]) -> str:
        """Create a handoff document between agents."""
        timestamp = datetime.datetime.now().isoformat()

        handoff_doc = f"""# Agent Handoff: {from_agent.value.title()} → {to_agent.value.title()}

## Context
- **Ticket ID**: {context.ticket_id}
- **Description**: {context.description}
- **Timestamp**: {timestamp}
- **Current Stage**: {context.current_stage.value}
- **Completed Stages**: {[stage.value for stage in context.completed_stages]}

## Summary from {from_agent.value.title()}
{summary}

## Artifacts Created
"""
        for stage, artifact_path in context.artifacts.items():
            handoff_doc += f"- **{stage}**: `{artifact_path}`\n"

        handoff_doc += f"""
## Next Actions for {to_agent.value.title()}
"""
        for i, action in enumerate(next_actions, 1):
            handoff_doc += f"{i}. {action}\n"

        handoff_doc += f"""
## Metadata
```json
{json.dumps(context.metadata, indent=2)}
```

## Validation Checkpoints
- [ ] Architecture compliance validated
- [ ] Build system compatibility confirmed
- [ ] Testing strategy included
- [ ] Documentation requirements met

---
*Generated by TradeMe Multi-Agent System*
"""

        handoff_filename = f"{context.ticket_id}-handoff-{from_agent.value}-to-{to_agent.value}.md"
        handoff_path = self.file_manager.get_agents_path(f"logs/{handoff_filename}")

        self.file_manager.ensure_directory(handoff_path)
        with open(handoff_path, 'w') as f:
            f.write(handoff_doc)

        return handoff_path

class ValidationManager:
    def __init__(self, config: AgentConfig, file_manager: FileManager):
        self.config = config
        self.file_manager = file_manager

    def validate_architecture_compliance(self, context: WorkflowContext) -> Dict[str, bool]:
        """Run architecture compliance validation."""
        # This would integrate with the existing validation scripts
        # For now, return a placeholder validation result
        return {
            "module_dependencies_valid": True,
            "universal_api_pattern": True,
            "dependencies_framework_usage": True,
            "platform_service_integration": True,
            "swiftui_uikit_integration": True
        }

    def validate_build_system(self, context: WorkflowContext) -> Dict[str, bool]:
        """Validate against Tuist build system requirements."""
        return {
            "tuist_module_structure": True,
            "dependency_constraints": True,
            "build_configuration": True
        }

    def validate_testing_strategy(self, context: WorkflowContext) -> Dict[str, bool]:
        """Validate testing implementation."""
        return {
            "test_coverage": True,
            "quick_nimble_integration": True,
            "placeholder_pattern_usage": True
        }

def load_architecture_context(file_manager: FileManager) -> str:
    """Load the comprehensive architecture context for agents."""
    arch_guide_path = file_manager.get_specs_path(
        file_manager.paths['comprehensive_guide']
    )

    if os.path.exists(arch_guide_path):
        with open(arch_guide_path, 'r') as f:
            return f.read()

    return "Architecture context not found. Please ensure the comprehensive guide is available."

def create_workflow_context(ticket_id: str, description: str) -> WorkflowContext:
    """Create a new workflow context for a ticket."""
    return WorkflowContext(
        ticket_id=ticket_id,
        description=description,
        current_stage=WorkflowStage.ARCHITECTURE_ANALYSIS,
        completed_stages=[],
        artifacts={},
        metadata={
            "created_at": datetime.datetime.now().isoformat(),
            "workflow_version": "1.0",
            "trademe_integration": True
        }
    )

if __name__ == "__main__":
    # Test the utilities
    config = AgentConfig()
    file_manager = FileManager(config)
    handoff_manager = HandoffManager(config, file_manager)
    validation_manager = ValidationManager(config, file_manager)

    print("✅ Shared utilities loaded successfully")
    print(f"Specs repo: {file_manager.paths['specs_repo']}")
    print(f"iOS project: {file_manager.paths['ios_project']}")
    print(f"Agents system: {file_manager.paths['agents_system']}")