# Software Factory Decision Framework

**When to use the factory vs when to code manually**

---

## 🎯 Quick Decision Guide

```
┌─────────────────────────────────────────────────────────┐
│  Is the requirement clear and testable?                 │
│  ├─ YES → Use Software Factory ✅                       │
│  └─ NO → Manual approach or clarify first               │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ USE SOFTWARE FACTORY When:

### 1. **Well-Defined Features**

**Characteristics**:
- Clear requirements (you can explain it in 2-3 sentences)
- Specific outcomes (you know what "done" looks like)
- Concrete examples (you can give sample inputs/outputs)

**Examples**:
- ✅ "Optimize 3 dish images from 6-8MB to ~300KB using Next.js Image component"
- ✅ "Add Prisma migration files matching current schema"
- ✅ "Create loading spinner that shows during API calls"
- ✅ "Fix broken test mocks for Next.js 16 Promise compatibility"

**Why factory works**:
- Agent knows exactly what to build
- Success is unambiguous
- Scenarios can validate automatically

---

### 2. **Clear Success Criteria**

**Characteristics**:
- Measurable outcomes (numbers, states, behaviors)
- Binary pass/fail (not subjective)
- Automatable validation (can write a test)

**Examples**:
- ✅ "Image file size < 300KB" (measurable)
- ✅ "Button disabled when form invalid" (testable)
- ✅ "API returns 200 with user data" (specific)
- ✅ "All TypeScript errors resolved" (binary)

**Why factory works**:
- Scenarios define exactly what "success" means
- Agent iterates until scenarios pass
- No ambiguity about when to stop

---

### 3. **Existing Patterns to Follow**

**Characteristics**:
- Similar code exists in codebase
- Documented patterns in knowledge base
- Framework best practices available
- Reference implementations accessible

**Examples**:
- ✅ "Add authentication like how it's done in auth.py"
- ✅ "Create component following our glassmorphic design pattern"
- ✅ "Implement API route matching our wrapper pattern"
- ✅ "Add tests following vitest setup in test-utils.ts"

**Why factory works**:
- Agents excel at pattern recognition
- Can read and adapt existing code
- Maintains consistency automatically

---

### 4. **Testable Behavior**

**Characteristics**:
- Functionality can be validated programmatically
- Edge cases can be enumerated
- Expected behavior is deterministic

**Examples**:
- ✅ "CSV parser handles empty files correctly"
- ✅ "Checkout flow sends meal choice to Stripe metadata"
- ✅ "Webhook populates database with order data"
- ✅ "Form validation rejects invalid postcodes"

**Why factory works**:
- Scenarios catch regressions
- Agent can verify its own work
- Quality is enforced, not hoped for

---

### 5. **Refactoring with Preserved Behavior**

**Characteristics**:
- External behavior stays the same
- Internal structure improves
- Tests define the contract

**Examples**:
- ✅ "Refactor pricing.tsx to use composition pattern (tests must still pass)"
- ✅ "Extract duplicated code into shared utils (functionality unchanged)"
- ✅ "Migrate from CSS modules to Tailwind (visual output identical)"

**Why factory works**:
- Tests lock in behavior
- Agent can't accidentally change functionality
- Refactoring is mechanical, not creative

---

### 6. **Bug Fixes with Reproduction Steps**

**Characteristics**:
- Bug is reproducible
- Expected behavior is known
- Can write failing test demonstrating bug

**Examples**:
- ✅ "Button stays disabled after form submission (should re-enable)"
- ✅ "Image optimization breaks on JPEG files (works on PNG)"
- ✅ "Webhook fails when meal_choice is null (should handle gracefully)"

**Why factory works**:
- Failing test = clear target
- Agent fixes until test passes
- Regression prevented

---

## ❌ DON'T USE SOFTWARE FACTORY When:

### 1. **Vague "Make It Better" Requests**

**Characteristics**:
- No specific target state
- Success is subjective
- "Better" is undefined

**Examples**:
- ❌ "Make the homepage look more modern"
- ❌ "Improve the user experience"
- ❌ "Make it faster" (without defining what or how much)
- ❌ "Fix the design"

**Why factory fails**:
- Agent doesn't know when to stop
- No clear validation criteria
- Endless iteration without convergence

**Instead**:
1. Define specific improvements
2. Set measurable targets
3. THEN use factory

**Better requests**:
- ✅ "Update homepage to use Plus Jakarta Sans font and glassmorphic cards"
- ✅ "Reduce page load time to < 2 seconds on 3G"
- ✅ "Optimize images to < 300KB each"

---

### 2. **Design/UX Decisions Needing Human Judgment**

**Characteristics**:
- Requires aesthetic judgment
- Involves user empathy
- Multiple valid solutions
- Creative exploration needed

**Examples**:
- ❌ "Design the checkout flow"
- ❌ "Choose color scheme for the app"
- ❌ "Decide navigation structure"
- ❌ "Create brand identity"

**Why factory fails**:
- Design is creative, not mechanical
- Requires taste and judgment
- Agents don't have aesthetic sense
- Multiple iterations won't improve quality

**Instead**:
1. Make design decisions yourself (or with designer)
2. Document the design
3. THEN use factory to implement

**After decisions**:
- ✅ "Implement checkout flow per design in checkout-flow.png"
- ✅ "Apply color scheme: primary=#FF6B35, secondary=#004E89"
- ✅ "Build navigation matching sitemap.md"

---

### 3. **Customer Discovery Requiring Empathy**

**Characteristics**:
- Understanding user needs
- Identifying pain points
- Emotional intelligence required
- Open-ended exploration

**Examples**:
- ❌ "Talk to customers about what features they want"
- ❌ "Understand why users are churning"
- ❌ "Research competitor UX to find opportunities"
- ❌ "Validate product-market fit"

**Why factory fails**:
- Requires human empathy
- Needs to read between the lines
- Context and nuance matter
- Building rapport is human skill

**Instead**:
1. Do customer research yourself
2. Document findings
3. THEN use factory to build solutions

**After discovery**:
- ✅ "Customers want X feature - build it per requirements.md"
- ✅ "Churn analysis shows Y issue - fix per spec.md"
- ✅ "Competitors have Z pattern - implement similar flow"

---

### 4. **Strategic Planning Needing Business Context**

**Characteristics**:
- Requires business judgment
- Involves trade-offs
- Needs market understanding
- Long-term implications

**Examples**:
- ❌ "Should we build feature X or Y first?"
- ❌ "What pricing model should we use?"
- ❌ "Which market segment to target?"
- ❌ "Make vs buy decision for service Z"

**Why factory fails**:
- Requires business context agents don't have
- Trade-offs need human judgment
- Strategy is about "why", factory is about "how"

**Instead**:
1. Make strategic decisions
2. Document the strategy
3. THEN use factory to execute

**After decisions**:
- ✅ "Build feature X per strategy-doc.md (we decided X before Y)"
- ✅ "Implement tiered pricing: $10/$20/$30 per plans.md"
- ✅ "Build SW20 targeting per market-analysis.md"

---

### 5. **Exploratory Prototyping**

**Characteristics**:
- Testing hypotheses
- Learning what's possible
- Discovering constraints
- Finding the right approach

**Examples**:
- ❌ "Experiment with different animation styles"
- ❌ "Try various data structures to see which performs best"
- ❌ "Prototype 3 different UX flows"
- ❌ "Spike: Can we integrate with API X?"

**Why factory fails**:
- Exploration is non-linear
- Success criteria change during process
- Multiple valid outcomes
- Learning IS the goal

**Instead**:
1. Do exploration manually or with agent assistance
2. Document what you learned
3. THEN use factory to build the chosen solution

**After exploration**:
- ✅ "Build animation using framer-motion per prototype-3.mp4"
- ✅ "Implement hash map approach (benchmarked best)"
- ✅ "Build UX flow #2 per user-testing-results.md"

---

### 6. **One-Liner Changes**

**Characteristics**:
- Trivial changes
- Takes 30 seconds to do manually
- More time to specify than to implement

**Examples**:
- ❌ "Change button text from 'Submit' to 'Send'"
- ❌ "Update copyright year to 2026"
- ❌ "Fix typo: 'recieve' → 'receive'"
- ❌ "Add console.log for debugging"

**Why factory fails**:
- Setup overhead > implementation time
- Overkill for trivial tasks
- Just do it manually in 10 seconds

**Rule of thumb**: If you can do it in < 2 minutes, don't use factory

---

## 🎯 Decision Matrix

| Factor | Use Factory | Don't Use Factory |
|--------|-------------|-------------------|
| **Clarity** | Requirements clear | Requirements vague |
| **Validation** | Can write tests | Success is subjective |
| **Patterns** | Existing examples | Greenfield/novel |
| **Complexity** | 10+ min to implement | < 2 min to implement |
| **Type** | Implementation | Design/strategy |
| **Knowledge** | Technical execution | Human judgment |

---

## 🔍 Real Examples from PlannedEats

### ✅ GOOD Factory Uses (From Our Session)

**Issue #10: Image Optimization**
- ✅ Clear: "Optimize 3 images to ~300KB each"
- ✅ Testable: File size checks, Next.js Image component validation
- ✅ Pattern exists: Next.js Image documentation
- ✅ Time: 10+ min manually
- **Result**: 10.5x speedup, 100% first-try success

**Test Suite Fix**:
- ✅ Clear: "Fix failing tests to make CI green"
- ✅ Testable: Test suite passes
- ✅ Pattern exists: Test fixing is mechanical
- ✅ Time: 4 hours manually
- **Result**: 24x speedup, 38 tests fixed systematically

---

### ❌ BAD Factory Uses (Hypothetical)

**"Make PlannedEats more appealing"**
- ❌ Vague: What does "appealing" mean?
- ❌ Subjective: Can't write automated tests
- ❌ No clear target state
- **Instead**: Define specific visual improvements, THEN use factory

**"Should we add weekly or monthly subscriptions?"**
- ❌ Strategic decision requiring business context
- ❌ Needs customer research, competitor analysis
- ❌ Trade-offs require human judgment
- **Instead**: Research options, decide, THEN use factory to implement

**"Fix the WhatsApp button" (when it's a 1-line CSS change)**
- ❌ Trivial: Takes 10 seconds manually
- ❌ Setup overhead > implementation
- **Instead**: Just change it manually

---

## 🎓 How to Convert "Bad" Requests to "Good" Ones

### Template:

**Vague request** → **Specific requirement** → **Factory-ready**

**Example 1**:
```
❌ "Make the site faster"
   ↓
⚠️  "Optimize images and reduce page load time"
   ↓
✅ "Optimize 3 dish images to <300KB, reduce total load to <2s on 3G"
   → Factory can build this!
```

**Example 2**:
```
❌ "Improve error handling"
   ↓
⚠️  "Add better error messages"
   ↓
✅ "Show user-friendly toast notifications on API errors with retry button"
   → Factory can build this!
```

**Example 3**:
```
❌ "Fix the design"
   ↓
⚠️  "Make it look more modern"
   ↓
✅ "Apply glassmorphic design: white/10 backdrop-blur cards, orange accents"
   → Factory can build this!
```

---

## 📊 ROI by Request Type

| Request Type | Factory Speedup | Why |
|--------------|-----------------|-----|
| **Well-defined feature** | 10-20x | Clear target, automatable |
| **Bug fix (reproducible)** | 15-25x | Test-driven, mechanical |
| **Refactoring** | 8-15x | Behavior preserved by tests |
| **Vague improvement** | 2-5x | Needs clarification first |
| **Design decision** | N/A | Human judgment required |
| **One-liner change** | 0.5x | Slower than manual! |

---

## 🎬 Practical Workflow

### Step 1: Evaluate the Request

Ask yourself:
1. Can I write 3-5 scenarios that define success? **YES/NO**
2. Would someone else understand what "done" means? **YES/NO**
3. Does similar code/pattern exist? **YES/NO**
4. Will this take 10+ minutes to implement? **YES/NO**

**If 3+ YES** → Use factory ✅
**If 2 or fewer YES** → Manual or clarify first

---

### Step 2: If Unclear, Clarify First

**Use agent for clarification**:
```
"I want to improve the homepage"
  ↓
Ask agent: "What specific improvements would make the homepage better?
           Analyze current homepage and suggest measurable changes."
  ↓
Agent suggests: "Reduce load time, improve mobile layout, add social proof"
  ↓
Pick one: "Reduce load time to <2s by optimizing images"
  ↓
NOW use factory with clear spec!
```

---

### Step 3: Use the Right Tool

| Situation | Tool | Why |
|-----------|------|-----|
| **Clear feature** | Factory | 10x faster |
| **Need design** | Manual + Designer | Human creativity |
| **Need strategy** | Research + Discussion | Business judgment |
| **Quick fix** | Manual | Faster than setup |
| **Exploration** | Manual + Agent chat | Learning mode |
| **Implementation** | Factory | Execution mode |

---

## 💡 Examples from Real Work

### PlannedEats Factory Runs (Proven)

| Issue | Type | Factory? | Result |
|-------|------|----------|--------|
| **#10: Image Optimization** | Well-defined | ✅ YES | 10.5x speedup |
| **Test Suite Fix** | Clear criteria | ✅ YES | 24x speedup |
| **#27: Prisma Migrations** | Specific task | ✅ YES | Use factory |
| **#17: Loading States** | Clear patterns | ✅ YES | Use factory |
| **Design homepage** | Creative | ❌ NO | Need human |
| **Fix typo** | Trivial | ❌ NO | Just do it |

---

### ai-tools Potential Uses

| Task | Factory? | Why |
|------|----------|-----|
| **Add retry logic to orchestrator** | ✅ YES | Clear behavior, testable |
| **Create new CLI command** | ✅ YES | Follow existing pattern |
| **Fix failing tests** | ✅ YES | Clear target (green CI) |
| **Decide architecture** | ❌ NO | Strategic decision |
| **Explore new framework** | ❌ NO | Learning/discovery |
| **Update version number** | ❌ NO | Trivial (10 seconds) |

---

## 🎯 Decision Tree

```
Start
  │
  ├─ Can you write automated test? ──NO──→ Manual or clarify
  │                                  YES
  │                                   │
  ├─ Will it take 10+ minutes? ──────NO──→ Just do it manually
  │                                  YES
  │                                   │
  ├─ Is success measurable? ─────────NO──→ Define criteria first
  │                                  YES
  │                                   │
  ├─ Similar code exists? ───────────NO──→ Can still use factory
  │                                  YES      (but slower)
  │                                   │
  └─────────────────────────────────────→ ✅ USE SOFTWARE FACTORY
```

---

## 📝 Pre-Flight Checklist

**Before starting a factory run**, verify:

- [ ] I can describe the requirement in 2-3 clear sentences
- [ ] I can write at least 3 scenarios that define success
- [ ] I know what "done" looks like (specific, measurable)
- [ ] The work will take 10+ minutes to implement manually
- [ ] Success can be validated programmatically (not just "looks good")
- [ ] I have time to set up scenarios (5-10 min investment)

**If all checked** → Proceed with factory! 🏭

**If 2+ unchecked** → Clarify or manual approach

---

## 🚀 The Sweet Spot

**Factory is MOST valuable for**:

1. **Medium complexity features** (30 min - 4 hours manual work)
   - Not too trivial (setup overhead)
   - Not too vague (needs clarity)
   - Sweet spot: 10-20x speedup

2. **Systematic work** (bugs, refactoring, test fixes)
   - Clear mechanical process
   - Agent excels at systematic tasks
   - Sweet spot: 15-25x speedup

3. **Pattern replication** (applying existing patterns)
   - Agent reads pattern
   - Adapts to new context
   - Maintains consistency
   - Sweet spot: 8-15x speedup

---

## 💎 Golden Rule

> **"If you can't write a test that proves it works, don't use the factory."**

**Corollary**: If you CAN write the test, the factory will probably beat manual development by 10x+.

---

## 📚 See Also

- **Success stories**: `factory-run/issue-10/` (image optimization)
- **Methodology**: `MANIFESTO.md` (core principles)
- **Templates**: `templates/` (ready to use)
- **Examples**: `examples/digital-twin-stripe.py`

---

**Version**: 1.0
**Last Updated**: March 2026
**Based on**: 2 production factory runs (PlannedEats)
