#!/usr/bin/env python3
"""
TradeMe Multi-Agent Development System Orchestrator

Coordinates the workflow between all agents:
1. Architect Agent - Analyzes requirements and validates architecture
2. Research Agent - Researches codebase patterns and creates requirements
3. Planner Agent - Creates implementation design with compliance validation
4. Programmer Agent - Generates Swift code following TradeMe patterns

Usage:
    python orchestrator.py "VLP-XXX: Add user profile caching to reduce API calls"
    python orchestrator.py --resume VLP-XXX  # Resume from previous session
    python orchestrator.py --validate VLP-XXX  # Validate completed work
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add tools and agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from shared_utils import (
    AgentConfig, FileManager, HandoffManager, ValidationManager,
    AgentRole, WorkflowStage, WorkflowContext, create_workflow_context
)

from architect import TradeMeArchitect
from researcher import TradeMeResearcher
from planner import TradeMePlanner
from programmer import TradeMeProgrammer
from security_agent import TradeMeSecurityAgent
from test_runner import TradeMeTestRunner
from qa_engineer import TradeMeQAEngineer
from crash_analyzer import TradeMeCrashAnalyzer

# Import workflow classification
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
from workflow_classifier import WorkflowClassifier, WorkflowType

class WorkflowOrchestrator:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)
        self.validation_manager = ValidationManager(self.config, self.file_manager)

        # Initialize agents
        self.architect = TradeMeArchitect()
        self.researcher = TradeMeResearcher()
        self.planner = TradeMePlanner()
        self.programmer = TradeMeProgrammer()
        self.security_agent = TradeMeSecurityAgent()
        self.test_runner = TradeMeTestRunner()
        self.qa_engineer = TradeMeQAEngineer()
        self.crash_analyzer = TradeMeCrashAnalyzer()

        # Initialize workflow classifier
        self.classifier = WorkflowClassifier()

        # Workflow configuration
        self.workflow_config = self.config.get_workflow_config()

    def execute_workflow(self, ticket_description: str, resume_ticket_id: str = None) -> WorkflowContext:
        """
        Execute the complete multi-agent workflow.
        """
        print("🤖 === TradeMe Multi-Agent Development System ===")
        print(f"🎯 Task: {ticket_description}")
        print("=" * 60)

        # Classify the workflow type
        classification = self.classifier.classify(ticket_description)
        print(f"🔍 Workflow Classification: {classification.workflow_type.value}")
        print(f"📊 Confidence: {classification.confidence:.2f}")
        if classification.reasoning:
            print(f"💭 Reasoning: {'; '.join(classification.reasoning)}")
        print("=" * 60)

        # Create or resume workflow context
        if resume_ticket_id:
            context = self._resume_workflow(resume_ticket_id)
            if context is None:
                print(f"❌ Could not resume workflow for {resume_ticket_id}")
                return None
        else:
            # Extract ticket ID from description or generate one
            ticket_id = self._extract_ticket_id(ticket_description)
            context = create_workflow_context(ticket_id, ticket_description)

            # Store classification in context
            context.metadata['workflow_classification'] = {
                'type': classification.workflow_type.value,
                'confidence': classification.confidence,
                'reasoning': classification.reasoning,
                'crash_indicators': classification.crash_indicators
            }

        # Save initial context
        self._save_workflow_context(context)

        try:
            # Execute appropriate workflow based on classification
            if classification.workflow_type == WorkflowType.CRASH_FIX:
                context = self._execute_crash_fix_workflow(context, classification)
            elif classification.workflow_type == WorkflowType.BUG_FIX:
                context = self._execute_bug_fix_workflow(context, classification)
            else:
                # Execute standard feature development workflow
                context = self._execute_workflow_stages(context)

            # Final validation
            if self._validate_workflow_completion(context):
                print("\n🎉 === Workflow Completed Successfully ===")
                self._print_workflow_summary(context)
            else:
                print("\n⚠️  === Workflow Completed with Issues ===")
                self._print_validation_issues(context)

            return context

        except Exception as e:
            print(f"\n❌ === Workflow Failed ===")
            print(f"Error: {e}")
            self._save_workflow_context(context)  # Save state for potential resume
            raise

    def _extract_ticket_id(self, description: str) -> str:
        """Extract ticket ID from description or generate one."""
        import re

        # Look for patterns like VLP-XXX, TICKET-123, etc.
        match = re.match(r'^([A-Z]+-\d+)', description)
        if match:
            return match.group(1)

        # Generate a ticket ID based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        return f"AUTO-{timestamp}"

    def _execute_workflow_stages(self, context: WorkflowContext) -> WorkflowContext:
        """Execute all workflow stages in sequence."""
        stages = [
            (WorkflowStage.ARCHITECTURE_ANALYSIS, self.architect, "🏛️  Architecture Analysis"),
            (WorkflowStage.REQUIREMENTS_RESEARCH, self.researcher, "🔍 Requirements Research"),
            (WorkflowStage.IMPLEMENTATION_PLANNING, self.planner, "📋 Implementation Planning"),
            (WorkflowStage.CODE_GENERATION, self.programmer, "💻 Code Generation"),
            (WorkflowStage.SECURITY_AUDIT, self.security_agent, "🔒 Security Audit"),
            (WorkflowStage.TESTING, self.test_runner, "🧪 Testing & Auto-Fix"),
            (WorkflowStage.QUALITY_ASSURANCE, self.qa_engineer, "✅ Quality Assurance"),
        ]

        for stage, agent, stage_name in stages:
            if stage in context.completed_stages:
                print(f"✅ {stage_name} (already completed)")
                continue

            print(f"\n🚀 Starting {stage_name}...")
            try:
                context = agent.execute(context)
                self._save_workflow_context(context)
                print(f"✅ {stage_name} completed successfully")

                # Validation checkpoint
                if self.workflow_config.get('validation_checkpoints'):
                    validation_result = self._run_validation_checkpoint(context, stage)
                    if not validation_result['passed']:
                        print(f"⚠️  Validation issues found after {stage_name}")
                        for issue in validation_result['issues']:
                            print(f"   - {issue}")

            except Exception as e:
                print(f"❌ {stage_name} failed: {e}")
                self._save_workflow_context(context)
                raise

        return context

    def _run_validation_checkpoint(self, context: WorkflowContext, stage: WorkflowStage) -> Dict[str, Any]:
        """Run validation at workflow checkpoints."""
        validation_result = {
            'passed': True,
            'issues': [],
            'stage': stage.value
        }

        try:
            if stage == WorkflowStage.ARCHITECTURE_ANALYSIS:
                arch_validation = self.validation_manager.validate_architecture_compliance(context)
                if not all(arch_validation.values()):
                    validation_result['passed'] = False
                    validation_result['issues'].extend([
                        f"Architecture compliance issue: {k}" for k, v in arch_validation.items() if not v
                    ])

            elif stage == WorkflowStage.IMPLEMENTATION_PLANNING:
                build_validation = self.validation_manager.validate_build_system(context)
                if not all(build_validation.values()):
                    validation_result['passed'] = False
                    validation_result['issues'].extend([
                        f"Build system issue: {k}" for k, v in build_validation.items() if not v
                    ])

            elif stage == WorkflowStage.CODE_GENERATION:
                test_validation = self.validation_manager.validate_testing_strategy(context)
                if not all(test_validation.values()):
                    validation_result['passed'] = False
                    validation_result['issues'].extend([
                        f"Testing strategy issue: {k}" for k, v in test_validation.items() if not v
                    ])

        except Exception as e:
            validation_result['passed'] = False
            validation_result['issues'].append(f"Validation error: {e}")

        return validation_result

    def _save_workflow_context(self, context: WorkflowContext) -> None:
        """Save workflow context for potential resume."""
        context_file = self.file_manager.get_agents_path(f"logs/{context.ticket_id}-context.json")
        self.file_manager.ensure_directory(context_file)

        # Convert context to JSON-serializable format
        context_dict = {
            'ticket_id': context.ticket_id,
            'description': context.description,
            'current_stage': context.current_stage.value,
            'completed_stages': [stage.value for stage in context.completed_stages],
            'artifacts': context.artifacts,
            'metadata': context.metadata
        }

        with open(context_file, 'w') as f:
            json.dump(context_dict, f, indent=2)

    def _resume_workflow(self, ticket_id: str) -> Optional[WorkflowContext]:
        """Resume workflow from saved context."""
        context_file = self.file_manager.get_agents_path(f"logs/{ticket_id}-context.json")

        if not os.path.exists(context_file):
            return None

        try:
            with open(context_file, 'r') as f:
                context_dict = json.load(f)

            # Reconstruct WorkflowContext
            context = WorkflowContext(
                ticket_id=context_dict['ticket_id'],
                description=context_dict['description'],
                current_stage=WorkflowStage(context_dict['current_stage']),
                completed_stages=[WorkflowStage(stage) for stage in context_dict['completed_stages']],
                artifacts=context_dict['artifacts'],
                metadata=context_dict['metadata']
            )

            print(f"📋 Resumed workflow for {ticket_id}")
            print(f"   Current stage: {context.current_stage.value}")
            print(f"   Completed stages: {len(context.completed_stages)}")

            return context

        except Exception as e:
            print(f"❌ Failed to resume workflow: {e}")
            return None

    def _execute_crash_fix_workflow(self, context: WorkflowContext, classification) -> WorkflowContext:
        """Execute crash fix specific workflow."""
        print("\n🚨 === Executing Crash Fix Workflow ===")

        stages = [
            ("crash_analysis", self.crash_analyzer, "🔍 Crash Analysis"),
            ("validation", self.qa_engineer, "🧪 Fix Validation")
        ]

        for stage_name, agent, stage_description in stages:
            print(f"\n{stage_description}")
            print("-" * 40)

            try:
                if stage_name == "crash_analysis":
                    # Generate crash analysis report
                    report_path = agent.generate_crash_fix_report(context)
                    context.artifacts[stage_name] = report_path
                    print(f"✅ {stage_description} completed")

                elif stage_name == "validation":
                    # Run QA validation on crash analysis
                    qa_result = agent.validate_crash_fix(context)
                    context.artifacts[stage_name] = qa_result
                    print(f"✅ {stage_description} completed")

            except Exception as e:
                print(f"❌ {stage_description} failed: {e}")
                raise

        print("\n🎉 === Crash Fix Workflow Completed ===")
        return context

    def _execute_bug_fix_workflow(self, context: WorkflowContext, classification) -> WorkflowContext:
        """Execute bug fix specific workflow."""
        print("\n🐛 === Executing Bug Fix Workflow ===")

        # For now, use the crash analyzer for general bug fixes too
        # In the future, we could add a separate bug analyzer
        stages = [
            ("bug_analysis", self.crash_analyzer, "🔍 Bug Analysis"),
            ("validation", self.qa_engineer, "🧪 Fix Validation")
        ]

        for stage_name, agent, stage_description in stages:
            print(f"\n{stage_description}")
            print("-" * 40)

            try:
                if stage_name == "bug_analysis":
                    report_path = agent.generate_crash_fix_report(context)
                    context.artifacts[stage_name] = report_path
                    print(f"✅ {stage_description} completed")

                elif stage_name == "validation":
                    qa_result = agent.validate_crash_fix(context)
                    context.artifacts[stage_name] = qa_result
                    print(f"✅ {stage_description} completed")

            except Exception as e:
                print(f"❌ {stage_description} failed: {e}")
                raise

        print("\n🎉 === Bug Fix Workflow Completed ===")
        return context

    def _validate_workflow_completion(self, context: WorkflowContext) -> bool:
        """Validate that the workflow completed successfully."""
        required_stages = [
            WorkflowStage.ARCHITECTURE_ANALYSIS,
            WorkflowStage.REQUIREMENTS_RESEARCH,
            WorkflowStage.IMPLEMENTATION_PLANNING,
            WorkflowStage.CODE_GENERATION,
            WorkflowStage.QUALITY_ASSURANCE
        ]

        # Check all required stages completed
        missing_stages = [stage for stage in required_stages if stage not in context.completed_stages]
        if missing_stages:
            print(f"❌ Missing stages: {[stage.value for stage in missing_stages]}")
            return False

        # Check all required artifacts exist
        required_artifacts = ['architecture_analysis', 'requirements', 'implementation_plan', 'code_generation', 'qa_report']
        missing_artifacts = [artifact for artifact in required_artifacts if artifact not in context.artifacts]
        if missing_artifacts:
            print(f"❌ Missing artifacts: {missing_artifacts}")
            return False

        # Validate artifact files exist
        for artifact_name, artifact_path in context.artifacts.items():
            if isinstance(artifact_path, str) and not os.path.exists(artifact_path):
                print(f"❌ Missing artifact file: {artifact_path}")
                return False

        return True

    def _print_workflow_summary(self, context: WorkflowContext) -> None:
        """Print a summary of the completed workflow."""
        print(f"""
📊 Workflow Summary for {context.ticket_id}
{'=' * 50}

📝 Description: {context.description}
⏰ Started: {context.metadata.get('created_at', 'Unknown')}
✅ Completed Stages: {len(context.completed_stages)}/5

📂 Generated Artifacts:
""")
        for artifact_name, artifact_path in context.artifacts.items():
            if isinstance(artifact_path, str):
                print(f"   - {artifact_name}: {os.path.basename(artifact_path)}")
            elif isinstance(artifact_path, list):
                print(f"   - {artifact_name}: {len(artifact_path)} files")

        print(f"""
🎯 Next Steps:
1. Review generated code in iOS project
2. Run build validation scripts
3. Execute test suite
4. Integrate with TradeMe iOS app
5. Performance validation and optimization

📁 Project Locations:
   - Specifications: {self.file_manager.paths['specs_repo']}
   - iOS Project: {self.file_manager.paths['ios_project']}
   - Agent Logs: {self.file_manager.paths['agents_system']}/logs/

🔗 Key Files:
   - Architecture Analysis: {os.path.basename(context.artifacts.get('architecture_analysis', ''))}
   - Requirements: {os.path.basename(context.artifacts.get('requirements', ''))}
   - Implementation Plan: {os.path.basename(context.artifacts.get('implementation_plan', ''))}
   - Code Summary: {os.path.basename(context.artifacts.get('code_generation', ''))}
""")

    def _print_validation_issues(self, context: WorkflowContext) -> None:
        """Print validation issues found during workflow."""
        print("⚠️  Validation Issues Found:")
        print("Please review and address these issues:")
        print("- Run architecture compliance validation")
        print("- Verify build system compatibility")
        print("- Validate testing strategy implementation")
        print("- Check generated code quality")

    def validate_completed_work(self, ticket_id: str) -> Dict[str, Any]:
        """Validate previously completed work."""
        print(f"🔍 Validating completed work for {ticket_id}...")

        # Load context
        context = self._resume_workflow(ticket_id)
        if not context:
            return {'success': False, 'error': f'No workflow found for {ticket_id}'}

        validation_results = {
            'success': True,
            'ticket_id': ticket_id,
            'architecture_compliance': {},
            'build_validation': {},
            'testing_validation': {},
            'file_integrity': {},
            'issues': []
        }

        try:
            # Architecture compliance
            validation_results['architecture_compliance'] = self.validation_manager.validate_architecture_compliance(context)

            # Build system validation
            validation_results['build_validation'] = self.validation_manager.validate_build_system(context)

            # Testing strategy validation
            validation_results['testing_validation'] = self.validation_manager.validate_testing_strategy(context)

            # File integrity check
            file_issues = []
            for artifact_name, artifact_path in context.artifacts.items():
                if isinstance(artifact_path, str) and not os.path.exists(artifact_path):
                    file_issues.append(f"Missing file: {artifact_path}")
                elif isinstance(artifact_path, list):
                    for file_path in artifact_path:
                        if not os.path.exists(file_path):
                            file_issues.append(f"Missing file: {file_path}")

            validation_results['file_integrity']['missing_files'] = file_issues
            validation_results['file_integrity']['passed'] = len(file_issues) == 0

            # Collect all issues
            all_validations = [
                validation_results['architecture_compliance'],
                validation_results['build_validation'],
                validation_results['testing_validation']
            ]

            for validation in all_validations:
                for key, passed in validation.items():
                    if not passed:
                        validation_results['issues'].append(f"Validation failed: {key}")

            validation_results['issues'].extend(file_issues)
            validation_results['success'] = len(validation_results['issues']) == 0

            # Print results
            if validation_results['success']:
                print("✅ All validations passed!")
            else:
                print("❌ Validation issues found:")
                for issue in validation_results['issues']:
                    print(f"   - {issue}")

        except Exception as e:
            validation_results['success'] = False
            validation_results['error'] = str(e)
            print(f"❌ Validation failed: {e}")

        return validation_results

def main():
    parser = argparse.ArgumentParser(
        description='TradeMe Multi-Agent Development System - AI-powered iOS development workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "VLP-123: Add user profile caching"           # Run complete workflow
  %(prog)s --resume VLP-123                              # Resume interrupted workflow
  %(prog)s --validate VLP-123                            # Validate completed work
  %(prog)s --list                                        # List all sessions
  %(prog)s --priority high "URGENT: Fix crash bug"      # High priority workflow
  %(prog)s --dry-run "TEST: Preview workflow"           # Preview without execution

Workflow Stages:
  1. 🏛️  Architecture Analysis   - Validate TradeMe iOS patterns
  2. 🔍 Requirements Research    - Create Layer 3 requirements + research
  3. 📋 Implementation Planning  - Design Layer 5 implementation
  4. 💻 Code Generation         - Generate production Swift code + tests
  5. 🧪 Quality Assurance      - Comprehensive testing and validation

Output Directories:
  generated-specs/              # Specification documents (Layer 3, 5)
  generated-code/               # Swift code with Tuist configuration
  quality-reports/              # QA testing reports and scores
  logs/                         # Workflow logs and agent handoffs
        ''')

    parser.add_argument('description', nargs='?',
                       help='Ticket description (e.g., "VLP-XXX: Add user caching")')
    parser.add_argument('--resume', metavar='TICKET_ID',
                       help='Resume workflow for specified ticket ID')
    parser.add_argument('--validate', metavar='TICKET_ID',
                       help='Validate completed work for specified ticket ID')
    parser.add_argument('--list', action='store_true',
                       help='List all workflow sessions')
    parser.add_argument('--priority', choices=['low', 'medium', 'high', 'urgent'],
                       default='medium', help='Set workflow priority (affects agent behavior)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview workflow steps without execution')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output with detailed agent logs')
    parser.add_argument('--output-dir', metavar='DIR',
                       help='Custom output directory (default: current directory)')
    parser.add_argument('--agents', nargs='+',
                       choices=['architect', 'researcher', 'planner', 'programmer', 'qa_engineer'],
                       help='Run only specific agents (for testing/debugging)')
    parser.add_argument('--skip-qa', action='store_true',
                       help='Skip quality assurance stage (faster but no validation)')
    parser.add_argument('--format', choices=['json', 'yaml', 'markdown'],
                       default='markdown', help='Output format for reports')
    parser.add_argument('--config', metavar='FILE',
                       help='Custom configuration file (default: config/agents.yaml)')
    parser.add_argument('--stats', action='store_true',
                       help='Show system statistics and performance metrics')

    args = parser.parse_args()

    orchestrator = WorkflowOrchestrator()

    try:
        # Show help and usage information
        if not any([args.description, args.resume, args.validate, args.list, args.stats]):
            print("🤖 TradeMe Multi-Agent Development System")
            print("=" * 50)
            print()
            print("📖 Usage Examples:")
            print('   ./orchestrator.py "VLP-123: Add user caching"')
            print('   ./orchestrator.py --priority high "URGENT: Fix crash"')
            print('   ./orchestrator.py --resume VLP-123')
            print('   ./orchestrator.py --validate VLP-123')
            print('   ./orchestrator.py --dry-run "Preview workflow"')
            print()
            print("🔧 Advanced Options:")
            print("   --verbose       Detailed output")
            print("   --skip-qa       Skip quality assurance")
            print("   --agents X Y    Run only specific agents")
            print("   --format json   Output format")
            print()
            print("📁 Output Directories:")
            print("   generated-specs/    Specification documents")
            print("   generated-code/     Swift code and Tuist projects")
            print("   quality-reports/    QA testing reports")
            print("   logs/               Workflow logs and handoffs")
            print()
            print("Type './orchestrator.py --help' for detailed options")
            return

        if args.stats:
            # Show system statistics
            print("📊 TradeMe Multi-Agent System Statistics")
            print("=" * 50)
            logs_dir = orchestrator.file_manager.get_agents_path("logs")
            if os.path.exists(logs_dir):
                context_files = [f for f in os.listdir(logs_dir) if f.endswith('-context.json')]
                print(f"🔄 Total workflows: {len(context_files)}")

                # Count by stage completion
                stage_stats = {stage.value: 0 for stage in WorkflowStage}
                for context_file in context_files:
                    try:
                        with open(os.path.join(logs_dir, context_file), 'r') as f:
                            context_data = json.load(f)
                            for stage in context_data.get('completed_stages', []):
                                if stage in stage_stats:
                                    stage_stats[stage] += 1
                    except:
                        continue

                print("📋 Stage Completion:")
                for stage, count in stage_stats.items():
                    print(f"   {stage}: {count}")
            else:
                print("📋 No workflow data found")

            return

        if args.list:
            # List all workflow sessions with details
            logs_dir = orchestrator.file_manager.get_agents_path("logs")
            if os.path.exists(logs_dir):
                context_files = [f for f in os.listdir(logs_dir) if f.endswith('-context.json')]
                if context_files:
                    print("📋 Available workflow sessions:")
                    print("=" * 60)
                    for context_file in sorted(context_files):
                        ticket_id = context_file.replace('-context.json', '')
                        context_path = os.path.join(logs_dir, context_file)
                        try:
                            with open(context_path, 'r') as f:
                                context_data = json.load(f)

                            description = context_data.get('description', 'No description')[:50]
                            completed = len(context_data.get('completed_stages', []))
                            current = context_data.get('current_stage', 'unknown')
                            created = context_data.get('metadata', {}).get('created_at', 'Unknown')[:19]

                            status = "✅ Complete" if completed == 5 else f"🔄 Stage {completed}/5"

                            print(f"🎫 {ticket_id}")
                            print(f"   📝 {description}...")
                            print(f"   📊 Status: {status} (Current: {current})")
                            print(f"   📅 Created: {created}")
                            print()
                        except:
                            print(f"⚠️  {ticket_id} (corrupted context)")
                else:
                    print("📋 No workflow sessions found")
                    print("💡 Run a workflow first: ./orchestrator.py \"TEST-001: Sample feature\"")
            else:
                print("📋 No workflow sessions directory found")
                print("💡 Run a workflow first: ./orchestrator.py \"TEST-001: Sample feature\"")

        elif args.validate:
            # Validate completed work
            result = orchestrator.validate_completed_work(args.validate)
            if result['success']:
                print("✅ Validation completed successfully")
                sys.exit(0)
            else:
                print("❌ Validation failed")
                sys.exit(1)

        elif args.resume:
            # Resume existing workflow
            context = orchestrator.execute_workflow("", args.resume)
            if context:
                sys.exit(0)
            else:
                print(f"❌ Failed to resume workflow for {args.resume}")
                sys.exit(1)

        elif args.description:
            # Handle dry-run preview
            if args.dry_run:
                ticket_id = orchestrator._extract_ticket_id(args.description)
                print(f"🔍 Dry Run Preview: {ticket_id}")
                print(f"📝 Description: {args.description}")
                print("=" * 60)
                print()
                print("🚀 Workflow Preview:")
                print("1. 🏛️  Architecture Analysis")
                print("   → Analyze requirements against TradeMe iOS patterns")
                print("   → Validate module dependencies and Universal API compliance")
                print("   → Generate architecture analysis document")
                print()
                print("2. 🔍 Requirements Research")
                print("   → Research existing patterns in 25,976+ Swift files")
                print("   → Create Layer 3 requirements document")
                print("   → Identify platform services and design system usage")
                print()
                print("3. 📋 Implementation Planning")
                print("   → Design Layer 5 implementation with compliance validation")
                print("   → Plan triple module structure and Dependencies integration")
                print("   → Create comprehensive testing strategy")
                print()
                print("4. 💻 Code Generation")
                print("   → Generate production Swift code following TradeMe patterns")
                print("   → Create Tuist configuration and build scripts")
                print("   → Generate comprehensive test suites with Quick/Nimble")
                print()
                print("5. 🧪 Quality Assurance")
                print("   → Validate build compilation and architecture compliance")
                print("   → Analyze code quality and performance")
                print("   → Generate quality report with 0-100 score")
                print()
                print("📁 Expected Output:")
                print(f"   generated-specs/{ticket_id}-*.md")
                print(f"   generated-code/Modules/{{ModuleName}}/")
                print(f"   quality-reports/{ticket_id}-qa-report.md")
                print(f"   logs/{ticket_id}-*.md")
                print()
                print("💡 To execute: Remove --dry-run flag")
                return

            # Start new workflow
            print(f"🚀 Starting workflow with priority: {args.priority}")
            if args.verbose:
                print("🔍 Verbose mode enabled")
            if args.skip_qa:
                print("⚠️  Quality assurance will be skipped")

            context = orchestrator.execute_workflow(args.description)
            if context:
                sys.exit(0)
            else:
                print("❌ Workflow failed")
                sys.exit(1)

        else:
            # Interactive mode
            print("🤖 TradeMe Multi-Agent Development System")
            print("Enter a ticket description or command:")
            print("Examples:")
            print("  VLP-XXX: Add user profile caching to reduce API calls")
            print("  --resume VLP-XXX")
            print("  --validate VLP-XXX")
            print("  --list")

            while True:
                try:
                    user_input = input("\n> ").strip()
                    if not user_input:
                        continue

                    if user_input.lower() in ['exit', 'quit', 'q']:
                        print("👋 Goodbye!")
                        break

                    if user_input.startswith('--'):
                        # Handle commands
                        parts = user_input.split()
                        if parts[0] == '--list':
                            args.list = True
                            main()
                        elif parts[0] == '--resume' and len(parts) > 1:
                            args.resume = parts[1]
                            main()
                        elif parts[0] == '--validate' and len(parts) > 1:
                            args.validate = parts[1]
                            main()
                        else:
                            print("❌ Invalid command")
                    else:
                        # Execute workflow
                        orchestrator.execute_workflow(user_input)

                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()