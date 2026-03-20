# The Software Factory Manifesto

> **"Why am I doing this? (implied: the model should be doing this instead)"**

Inspired by StrongDM AI's Software Factory, this manifesto establishes the principles for building software where AI agents autonomously write, test, and converge code without human review.

## The Core Laws

### Law 1: Code Must NOT Be Written By Humans
If you're writing code, you're doing it wrong. Your job is to specify intent, create validation harnesses, and let agents converge to working solutions.

### Law 2: Code Must NOT Be Reviewed By Humans
Humans cannot review at the scale and speed required. Code is validated through scenarios, not inspection. If it passes end-to-end validation, it ships.

### Law 3: Spend Tokens Like Fuel
If you haven't spent **$1,000 on tokens per day per engineer**, your factory has room for improvement. Tokens are cheaper than developer time. Use them liberally.

---

## The Factory Formula

```
Seed → Validation Harness → Feedback Loop = Working Software
```

### 1. **Seed** (Entry Point)
Every piece of software needs an initial seed:
- A few sentences describing intent
- A screenshot of desired output
- An existing codebase to evolve
- A PRD or spec document

The seed doesn't need to be perfect. It needs to be **enough for an agent to start**.

### 2. **Validation Harness** (The Loop - Part 1)
Your validation must be:
- **End-to-end**: As close to real environment as possible
- **Automated**: No human verification required
- **Customer-facing**: Tests what customers actually experience
- **Economics-aware**: Validates business logic, not just technical correctness

#### Validation Techniques:
- Scenario-based testing (not just unit tests)
- Digital Twin Universe (behavioral clones of dependencies)
- Agentic simulation (AI acting as users)
- Just-in-time surveys
- Customer interviews converted to test scenarios
- Price elasticity testing

### 3. **Feedback** (The Loop - Part 2)
A sample of the output, fed back into the inputs. This closed loop allows your system to:
- Self-correct errors
- Compound correctness (not error)
- Converge toward working solutions
- Learn from failures

**The loop runs until holdout scenarios pass (and stay passing).**

---

## Apply More Tokens

> "For every obstacle, ask: how can we convert this problem into a representation the model can understand?"

Convert EVERYTHING into LLM-consumable format:

| Signal Type | How to Capture |
|-------------|----------------|
| **Use traces** | Screen recordings, click paths, user sessions |
| **Screen capture** | Screenshots of bugs, desired UIs, examples |
| **Conversation transcripts** | Customer support logs, sales calls |
| **Incident replays** | Production errors, stack traces, logs |
| **Adversarial use** | Security testing, edge case exploration |
| **Agentic simulation** | AI acting as users, stress testing |
| **Just-in-time surveys** | Contextual user feedback |
| **Customer interviews** | Direct user input converted to scenarios |
| **Price elasticity** | Business metrics, conversion data |

---

## The Validation Constraint

> "Given zero hand-written code and zero traditional review, we required a system that could grow from cascades of natural-language specifications and be validated automatically without semantic inspection of source."

**Code is treated like ML model weights:**
- Opaque internal structure
- Correctness inferred ONLY from externally observable behavior
- No manual code inspection
- Black-box validation

---

## Economics of The Agentic Moment

### What Was Impossible, Now Routine

The economics have fundamentally changed. Things that were "economically unfeasible" 6 months ago are now standard practice:

- **Digital Twin Universe**: Building high-fidelity clones of entire SaaS apps (Okta, Jira, Slack) was always possible but never worth the cost. Now it's a weekend project.

- **Comprehensive Test Coverage**: Writing thousands of end-to-end scenarios was too expensive. Now agents generate and maintain them.

- **Multi-language Ports**: Maintaining parallel implementations in different languages was unsustainable. Now semantic ports happen automatically.

### Deliberate Naivete

> "Remove the habits, conventions, and constraints of Software 1.0"

When you think "that would be too expensive" or "that would take too long," **question that assumption**. The old rules don't apply.

---

## Startup Application

At a startup, the Software Factory principles are:

### Speed + Quality Are Not Mutually Exclusive
- **MVP today beats perfect next quarter** - ship fast
- **But quality is non-negotiable** - validate thoroughly
- **Let agents handle the grunt work** - you focus on intent and validation

### Own Every Change
- When you (or your agent) touch code, you own it
- Breaks you introduce, you fix
- Quality is YOUR responsibility, not the agent's

### Rally The Team (of Agents)
- Launch specialists in parallel
- Each agent has clear FOCUS boundaries
- Celebrate wins, own failures fast
- Maintain momentum above all

---

## Success Metrics

### Primary Metrics:
1. **Token Spend**: Are you spending enough on agents vs human time?
2. **Scenario Pass Rate**: What % of holdout scenarios pass?
3. **Time to Convergence**: How fast do agents reach working solutions?
4. **Iteration Velocity**: How many attempts until success?

### Secondary Metrics:
5. **Human Review Time**: Should be approaching zero
6. **Manual Code Writing**: Should be approaching zero
7. **Production Incident Rate**: Should be decreasing (better validation)
8. **Feature Delivery Speed**: Should be accelerating

---

## The Software Factory Stack

### Foundation Layer (Must Have):
- **Unified LLM Client**: Single interface across providers (OpenAI, Anthropic, Gemini)
- **Coding Agent Loop**: Autonomous agent that can read, write, execute, iterate
- **Execution Environment**: Where agents run (local, Docker, K8s)

### Orchestration Layer (High Value):
- **Attractor**: DOT-based pipeline for multi-stage workflows
- **Scenario Engine**: Manages test scenarios and validation
- **Feedback Loop**: Captures results and feeds back to agents

### Advanced Layer (Force Multipliers):
- **Digital Twin Universe**: Clones of critical dependencies
- **CXDB**: Context store for agent memory/history
- **Gene Transfusion**: Pattern transfer between codebases
- **Semport**: Semantic auto-translation between languages

---

## Anti-Patterns (Never Do This)

❌ **Writing code by hand** when an agent could generate it
❌ **Manual code review** instead of scenario validation
❌ **Skipping validation** because "it looks right"
❌ **Treating agents like junior developers** (they're not - they're tireless execution engines)
❌ **Under-investing in tokens** (false economy)
❌ **Accepting vague specs** (garbage in, garbage out)
❌ **Blocking on human approval** (defeats the purpose)

---

## Getting Started

### Week 1: Foundation
1. Implement Unified LLM Client (or use existing)
2. Set up basic agent loop with file operations
3. Create your first automated scenario

### Week 2: Validation
1. Build scenario harness
2. Define success criteria for one feature
3. Run agent through full loop: seed → validate → feedback

### Week 3: Scale
1. Add parallel agent execution
2. Create Digital Twins for your critical dependencies
3. Measure token spend and iteration speed

### Week 4: Production
1. Ship your first factory-built feature
2. Monitor scenario pass rates
3. Iterate based on metrics

---

## The Promise

When fully operational, your Software Factory will:

✅ Ship features **10x faster** than manual development
✅ Maintain **higher quality** through comprehensive validation
✅ Scale engineering output **without scaling headcount**
✅ Free humans to focus on **strategy and validation**, not implementation
✅ Compound correctness with every iteration

---

## References

- **StrongDM Software Factory**: https://factory.strongdm.ai
- **Attractor (Open Source)**: https://github.com/strongdm/attractor
- **StrongDM Story**: https://factory.strongdm.ai/
- **Principles**: https://factory.strongdm.ai/principles
- **Techniques**: https://factory.strongdm.ai/techniques

---

**Version**: 1.0
**Date**: February 2026
**Status**: Living Document

---

> "We're not just working, we're building the future."
> — The Startup Way
