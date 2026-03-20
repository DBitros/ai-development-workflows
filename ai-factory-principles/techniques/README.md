# Software Factory Techniques

Practical patterns for applying factory principles, based on StrongDM's proven approaches.

---

## Overview

These techniques are **repeated patterns** discovered through building production Software Factories. Each technique solves a specific class of problems and can be combined with others.

---

## The Six Core Techniques

### 1. Digital Twin Universe (DTU)
**Problem**: Can't test against real third-party services at scale
**Solution**: Clone the externally observable behaviors of critical dependencies

[→ Full Documentation](./digital-twin-universe.md)

**Quick Example:**
```python
# Instead of:
okta_client.authenticate(username, password)  # Rate limited, costs money

# Use:
okta_twin.authenticate(username, password)  # Unlimited, free, deterministic
```

---

### 2. Gene Transfusion
**Problem**: Need to replicate patterns across codebases
**Solution**: Point agents at concrete exemplars to transfer working patterns

[→ Full Documentation](./gene-transfusion.md)

**Quick Example:**
```
Agent: "Implement authentication similar to how it's done in repo-a/auth.py"
→ Agent reads the pattern, adapts it to new context
```

---

### 3. The Filesystem (as Memory)
**Problem**: Agents need context management across sessions
**Solution**: Use directories, indexes, and on-disk state as memory substrate

[→ Full Documentation](./filesystem-memory.md)

**Quick Example:**
```
context/
  ├── current-task.md          # What agent is working on
  ├── completed-scenarios.json # Validation history
  ├── patterns/                # Discovered patterns
  └── decisions/               # Architecture decisions
```

---

### 4. Shift Work
**Problem**: Interactive vs autonomous work requires different approaches
**Solution**: Separate them - interactive for discovery, autonomous for execution

[→ Full Documentation](./shift-work.md)

**Quick Example:**
```
INTERACTIVE (with human):
- Clarify requirements
- Review architecture
- Approve approach

AUTONOMOUS (agent loop):
- Generate code
- Run tests
- Fix failures
- Iterate to green
```

---

### 5. Semport (Semantic Port)
**Problem**: Need to maintain code across languages/frameworks
**Solution**: Automated semantic-aware translation

[→ Full Documentation](./semport.md)

**Quick Example:**
```python
# Python implementation exists
def calculate_discount(price, tier):
    if tier == "gold": return price * 0.9
    if tier == "silver": return price * 0.95
    return price

# Agent creates TypeScript port
# → Preserves intent, adapts idioms
```

---

### 6. Pyramid Summaries
**Problem**: Need to compress context without losing detail
**Solution**: Reversible multi-level summarization

[→ Full Documentation](./pyramid-summaries.md)

**Quick Example:**
```
Level 1 (Detailed):  Full conversation history (100KB)
Level 2 (Summary):   Key points + decisions (10KB)
Level 3 (Abstract):  One-line summary (100 bytes)

Can expand back to any level as needed
```

---

## Technique Combinations

Techniques are most powerful when combined:

### Example: Feature Development

```
1. SHIFT WORK (Interactive)
   - Clarify requirements with stakeholder
   - Create scenarios

2. THE FILESYSTEM
   - Store scenarios in scenarios/
   - Track decisions in decisions/

3. GENE TRANSFUSION
   - Point agent at similar feature in codebase
   - "Build X similar to how Y is implemented"

4. AUTONOMOUS EXECUTION
   - Agent generates code
   - Runs scenarios
   - Iterates to green

5. SEMPORT (if multi-platform)
   - Port to other languages
   - Maintain semantic equivalence

6. PYRAMID SUMMARIES
   - Compress session history
   - Keep context manageable
```

---

## Technique Selection Guide

| If you need to... | Use this technique |
|-------------------|-------------------|
| Test against external APIs at scale | Digital Twin Universe |
| Replicate proven patterns | Gene Transfusion |
| Manage agent context across sessions | Filesystem Memory |
| Separate discovery from execution | Shift Work |
| Support multiple languages/frameworks | Semport |
| Keep context window manageable | Pyramid Summaries |

---

## Implementation Priority

Recommend building in this order:

### Phase 1: Foundation (Week 1)
1. **The Filesystem** - Context management
2. **Shift Work** - Interactive/autonomous separation

### Phase 2: Validation (Week 2)
3. **Digital Twin Universe** - Start with one service

### Phase 3: Scale (Week 3)
4. **Gene Transfusion** - Pattern replication
5. **Pyramid Summaries** - Context compression

### Phase 4: Multi-Platform (Week 4)
6. **Semport** - Cross-language support

---

## Detailed Docs

Each technique has comprehensive documentation:

- [Digital Twin Universe](./digital-twin-universe.md)
- [Gene Transfusion](./gene-transfusion.md)
- [Filesystem Memory](./filesystem-memory.md)
- [Shift Work](./shift-work.md)
- [Semport](./semport.md)
- [Pyramid Summaries](./pyramid-summaries.md)

---

## Contributing New Techniques

When you discover a new repeated pattern:

1. Document the **problem** it solves
2. Describe the **solution** pattern
3. Provide **concrete examples**
4. Show **combinations** with other techniques
5. Define **success metrics**

Add to this directory and update the README.

---

**Version**: 1.0
**Last Updated**: February 2026
