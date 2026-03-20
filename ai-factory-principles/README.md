# AI Software Factory Principles

> **Building software where AI agents autonomously write, test, and converge code without human review.**

Inspired by [StrongDM's Software Factory](https://factory.strongdm.ai/), this directory contains principles, techniques, and implementation guides for building your own Software Factory.

---

## What is a Software Factory?

A **Software Factory** is a system where:

✅ AI agents write code (humans write specs)
✅ Code is validated through scenarios (not manual review)
✅ Agents iterate until all tests pass (self-correction)
✅ Quality compounds with each iteration (not degrades)
✅ Everything ships faster and cheaper

### The Core Laws

1. **Code must NOT be written by humans**
2. **Code must NOT be reviewed by humans**
3. **Spend tokens like fuel** - $1,000/day per engineer minimum

---

## Quick Start

### 5-Minute Understanding

Read in this order:
1. [MANIFESTO.md](./MANIFESTO.md) - Core philosophy and laws
2. [Getting Started Guide](./implementation/GETTING-STARTED.md) - Your first factory

### 1-Hour Deep Dive

3. [Core Principles](./principles/CORE-PRINCIPLES.md) - Detailed methodology
4. [Techniques Overview](./techniques/README.md) - Practical patterns
5. [Digital Twin Universe](./techniques/digital-twin-universe.md) - Most powerful technique

---

## Directory Structure

```
ai-factory-principles/
├── MANIFESTO.md                    # Core philosophy and laws
├── README.md                       # This file
│
├── principles/                     # Core methodology
│   └── CORE-PRINCIPLES.md         # Seed → Validation → Feedback
│
├── techniques/                     # Practical patterns
│   ├── README.md                  # Techniques overview
│   ├── digital-twin-universe.md   # Clone external dependencies
│   ├── gene-transfusion.md        # Transfer patterns between codebases
│   ├── filesystem-memory.md       # Use filesystem as agent memory
│   ├── shift-work.md              # Interactive vs autonomous work
│   ├── semport.md                 # Semantic translation between languages
│   └── pyramid-summaries.md       # Multi-level context compression
│
├── implementation/                 # How to build it
│   ├── GETTING-STARTED.md         # Your first 2 weeks
│   ├── unified-llm-client.md      # Multi-provider SDK spec
│   ├── coding-agent-loop.md       # Autonomous coding agent spec
│   └── attractor.md               # Pipeline orchestration spec
│
└── specs/                          # StrongDM's open-source specs
    ├── attractor-spec.md          # DOT-based workflow orchestration
    ├── coding-agent-loop-spec.md  # Agent implementation
    └── unified-llm-spec.md        # Multi-provider client
```

---

## The Factory Formula

```
┌─────────────────────────────────────────────────┐
│  1. SEED (Entry Point)                           │
│     - Spec, screenshot, or existing codebase     │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  2. VALIDATION HARNESS (The Loop - Part 1)       │
│     - End-to-end scenarios                       │
│     - Digital Twin Universe                      │
│     - Automated, customer-facing validation      │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  3. FEEDBACK (The Loop - Part 2)                 │
│     - Pass/fail results + details                │
│     - Fed back to agent                          │
│     - Iterate until all scenarios pass           │
└─────────────┬───────────────────────────────────┘
              │
              ▼
         ┌────┴────┐
         │ SUCCESS │
         └─────────┘
```

---

## Key Principles Summary

### Principle 1: Seed (Entry Point)
Every project starts with:
- A few sentences (not a complete spec)
- A screenshot (visual intent)
- An existing codebase (evolve it)
- A conversation (describe the need)

### Principle 2: Validation Harness
Test end-to-end, as close to real environment as possible:
- Scenario-based (not just unit tests)
- Customer-facing (validate UX, not internals)
- Economics-aware (business logic matters)
- Automated (no human verification)

### Principle 3: Feedback Loop
Capture results and feed back to agent:
- Pass/fail with detailed context
- Agent analyzes failures and adjusts
- Loop continues until scenarios pass
- **Compounding correctness** (not error)

### Principle 4: Apply More Tokens
Convert everything to LLM-consumable format:
- User traces, screenshots, conversations
- Incident replays, error logs
- Customer interviews, support tickets
- Competitive analysis, pricing data

### Principle 5: Validation Constraint
Code is opaque (like ML model weights):
- No manual inspection
- Only external behavior matters
- Black-box validation

### Principle 6: New Economics
What was "too expensive" is now routine:
- Digital Twin Universe (clone entire services)
- Comprehensive test coverage (thousands of scenarios)
- Multi-language ports (maintain parallel implementations)
- Real-time refactoring (agents fix technical debt)

---

## The Six Core Techniques

| Technique | Problem | Solution |
|-----------|---------|----------|
| **Digital Twin Universe** | Can't test against real APIs at scale | Clone behavioral dependencies |
| **Gene Transfusion** | Need to replicate patterns | Point agents at exemplars |
| **Filesystem Memory** | Agents need persistent context | Use directories as memory |
| **Shift Work** | Interactive vs autonomous conflict | Separate discovery from execution |
| **Semport** | Multi-language maintenance | Semantic auto-translation |
| **Pyramid Summaries** | Context window limits | Reversible multi-level compression |

[→ Full Techniques Documentation](./techniques/README.md)

---

## Implementation Roadmap

### Week 1: Foundation
- [ ] Set up unified LLM client (multi-provider)
- [ ] Build basic agent loop (read, write, execute)
- [ ] Create first automated scenario

### Week 2: Validation
- [ ] Design scenario harness
- [ ] Define success criteria
- [ ] Run agent through full loop (seed → validate → feedback)

### Week 3: Scale
- [ ] Add parallel agent execution
- [ ] Build first Digital Twin
- [ ] Measure token spend and velocity

### Week 4: Production
- [ ] Ship first factory-built feature
- [ ] Monitor scenario pass rates
- [ ] Iterate based on metrics

[→ Detailed Getting Started Guide](./implementation/GETTING-STARTED.md)

---

## Success Metrics

### Primary Metrics:
- **Token Spend**: $1,000+/day per engineer
- **Scenario Pass Rate**: 95%+ first try, 100% after 2-3 iterations
- **Time to Convergence**: Hours, not days/weeks

### Secondary Metrics:
- **Human Review Time**: Approaching zero
- **Manual Code Writing**: Approaching zero
- **Production Incidents**: Decreasing (better validation)
- **Feature Delivery Speed**: Accelerating

---

## The Promise

When fully operational, your Software Factory will:

✅ Ship features **10x faster** than manual development
✅ Maintain **higher quality** through comprehensive validation
✅ Scale engineering output **without scaling headcount**
✅ Free humans to focus on **strategy and validation**, not implementation
✅ Compound correctness with every iteration

---

## Related Resources

### StrongDM Resources
- [Software Factory Site](https://factory.strongdm.ai/)
- [Attractor (Open Source)](https://github.com/strongdm/attractor)
- [Principles](https://factory.strongdm.ai/principles)
- [Techniques](https://factory.strongdm.ai/techniques)
- [Products](https://factory.strongdm.ai/products)

### Community Analysis
- [Simon Willison's Analysis](https://simonwillison.net/2026/Feb/7/software-factory/)
- [StrongDM Blog](https://www.strongdm.com/blog/the-strongdm-software-factory-building-software-with-ai)

### Reference Projects
- [Vercel AI SDK](https://github.com/vercel/ai) - Multi-provider pattern
- [LiteLLM](https://github.com/BerriAI/litellm) - 100+ provider support
- [codex-rs](https://github.com/openai/codex/tree/main/codex-rs) - OpenAI agent
- [gemini-cli](https://github.com/google-gemini/gemini-cli) - Google agent

---

## Contributing

This is a living document. As we implement and learn:

1. Document new techniques discovered
2. Update success metrics
3. Share implementation learnings
4. Contribute to open source specs

---

## License

Following StrongDM's approach - these principles are freely shareable.
Implementation specs from StrongDM are Apache 2.0.

---

**Version**: 1.0
**Last Updated**: February 2026
**Status**: Active Development

---

> "Why am I doing this? (implied: the model should be doing this instead)"
