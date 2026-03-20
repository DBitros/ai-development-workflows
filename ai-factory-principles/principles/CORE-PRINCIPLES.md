# Core Principles of the Software Factory

> **Seed → Validation Harness → Feedback Loop. Tokens are the fuel.**

This document details the fundamental principles that make the Software Factory work.

---

## Principle 1: The Entry Point (Seed)

Every piece of software needs an initial seed. Historically called a PRD or spec. Today, this could be:

- **A few sentences** - "Build a REST API for user management with CRUD operations"
- **A screenshot** - Image of desired UI or behavior
- **An existing codebase** - Start from what works, evolve it
- **A conversation** - User describing what they need

### What Makes a Good Seed?

✅ **Clear intent** - What problem are we solving?
✅ **Observable outcomes** - How will we know it works?
✅ **Enough context** - Agent can make informed decisions
✅ **Not necessarily complete** - Agents fill gaps through iteration

❌ **Perfectly detailed specs** - Not required, often wasted effort
❌ **Implementation details** - Let agents decide HOW
❌ **Complete requirements** - Discovery happens in the loop

### Seed Examples:

**Minimal Seed:**
```
Build a Python CLI tool that converts CSV to JSON.
Accept file path as argument, output formatted JSON to stdout.
```

**Better Seed:**
```
Build a Python CLI tool that converts CSV to JSON.

Requirements:
- Accept CSV file path as command-line argument
- Parse CSV with headers
- Output formatted JSON to stdout
- Handle missing values (convert to null)
- Return exit code 1 on errors

Success Criteria:
- Can convert sample.csv with 1000 rows in < 1 second
- Handles edge cases: empty file, missing headers, special chars
```

**Optimal Seed:**
```
Build a Python CLI tool that converts CSV to JSON.

[Include requirements as above PLUS:]

Reference Implementation:
- Use pandas.read_csv() for parsing
- Use json.dumps() with indent=2 for output
- See existing-tool.py for CLI pattern

Test Scenarios:
1. Basic case: cities.csv (3 columns, 10 rows) → cities.json
2. Large file: transactions.csv (20 columns, 100k rows)
3. Edge cases: empty.csv, malformed.csv, unicode.csv
```

---

## Principle 2: Validation Harness (The Loop - Part 1)

Your validation harness must be:

### End-to-End
Test the system as users experience it, not as developers see it.

**Example - BAD (Unit Test):**
```python
def test_parse_csv():
    assert parse_csv("a,b\n1,2") == [{"a": "1", "b": "2"}]
```

**Example - GOOD (End-to-End Scenario):**
```python
def test_csv_conversion_scenario():
    # Given: A real CSV file exists
    create_file("input.csv", "name,age\nAlice,30\nBob,25")

    # When: User runs the CLI tool
    result = subprocess.run(["python", "csv2json.py", "input.csv"],
                           capture_output=True)

    # Then: Output is valid JSON with correct data
    output = json.loads(result.stdout)
    assert len(output) == 2
    assert output[0]["name"] == "Alice"
    assert output[0]["age"] == "30"
    assert result.returncode == 0
```

### As Close to Real Environment as Possible

Test against actual dependencies, or perfect clones.

#### Real Dependency:
```python
# Test against actual Stripe API (test mode)
stripe.api_key = "sk_test_..."
charge = stripe.Charge.create(amount=1000, currency="usd", ...)
assert charge.status == "succeeded"
```

#### Digital Twin:
```python
# Test against behavioral clone of Stripe
twin_stripe = DigitalTwinStripe()
charge = twin_stripe.create_charge(amount=1000, currency="usd", ...)
assert charge.status == "succeeded"
assert twin_stripe.webhooks_sent == ["charge.succeeded"]
```

### Customer-Facing Validation

Validate what customers experience, not implementation details.

**Example - Customer-Facing Scenario:**
```gherkin
Scenario: User purchases premium subscription

Given: User is logged in with free account
When: User clicks "Upgrade to Premium" button
And: Enters credit card details
And: Confirms purchase
Then: User sees "Success! Welcome to Premium" message
And: User's account shows "Premium" badge
And: User can access premium features
And: User receives confirmation email within 2 minutes
```

### Economics-Aware Validation

Test business logic, not just technical correctness.

**Example - Economics Validation:**
```python
def test_pricing_discount_applies_correctly():
    # Create customer with 10% loyalty discount
    customer = create_customer(loyalty_tier="gold")

    # Purchase $100 item
    order = create_order(customer, items=[{"sku": "WIDGET", "price": 100}])

    # Verify discount applied
    assert order.subtotal == 100
    assert order.discount == 10
    assert order.total == 90

    # Verify revenue accounting
    assert order.recorded_revenue == 90
    assert order.discount_reason == "LOYALTY_GOLD_10PCT"
```

---

## Principle 3: Feedback (The Loop - Part 2)

> "A sample of the output, fed back into the inputs. This closed loop allows your system to self-correct and compound correctness."

### How Feedback Works

```
┌─────────────────────────────────────────────────┐
│  Agent generates code                            │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  Run validation scenarios                        │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  Capture results (pass/fail + details)           │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  Feed results back to agent                      │
│  "3 scenarios passed, 2 failed. Details:..."     │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│  Agent analyzes failures and adjusts             │
└─────────────┬───────────────────────────────────┘
              │
              ▼
              │
       Loop continues until
      all scenarios pass
```

### Feedback Quality Matters

**Poor Feedback:**
```
❌ "Tests failed"
❌ "Something is wrong with the API"
❌ "3 scenarios failed"
```

**Good Feedback:**
```
✅ Scenario: "User login with valid credentials" - FAILED
   Expected: HTTP 200, JWT token in response
   Actual: HTTP 401, {"error": "Invalid password"}

   Failure Analysis:
   - Password comparison is case-sensitive, should be case-insensitive
   - Located in auth.py:45

✅ Scenario: "User login with invalid credentials" - PASSED

✅ Scenario: "User login rate limiting" - FAILED
   Expected: HTTP 429 after 5 attempts
   Actual: No rate limiting enforced

   Failure Analysis:
   - Rate limiter not configured
   - Need to add @rate_limit(5, per_minute) decorator
```

### Compounding Correctness vs Compounding Error

Before the "agentic moment" (pre-Oct 2024):
```
Iteration 1: 70% correct
Iteration 2: 65% correct (model introduces new bugs)
Iteration 3: 55% correct (accumulating errors)
Iteration N: Collapse (death by a thousand cuts)
```

After (with proper validation loop):
```
Iteration 1: 70% correct (3 scenarios pass, 2 fail)
Iteration 2: 85% correct (4 scenarios pass, 1 fail)
Iteration 3: 95% correct (all scenarios pass, edge case fails)
Iteration N: 100% correct (all scenarios pass consistently)
```

**The key difference:** Quality feedback that guides improvement.

---

## Principle 4: Apply More Tokens

> "For every obstacle, ask: how can we convert this problem into a representation the model can understand?"

### The Token Investment Mindset

Old mindset: "Minimize LLM calls to save money"
New mindset: "Maximize LLM calls to save TIME"

**Economics:**
- Developer time: $100-300/hour
- Claude Opus tokens: ~$15-60/million tokens
- GPT-5.2 tokens: ~$10-50/million tokens

A $1000 token spend = 3-10 hours of developer time saved.

### What to Convert to Tokens

| Problem | Convert to... | How Agents Use It |
|---------|--------------|-------------------|
| **User reported bug** | Screenshot + steps to reproduce | Generate test case, identify root cause |
| **Feature request** | User interview transcript | Extract requirements, generate spec |
| **Performance issue** | Profiler traces + metrics | Identify bottleneck, suggest optimization |
| **Security concern** | Vulnerability scan results | Generate fix, add validation |
| **UI improvement** | Before/after screenshots | Generate CSS/components |
| **Integration** | API docs + example requests | Generate client code + tests |
| **Customer churn** | Support ticket history | Identify pain points, prioritize fixes |
| **Pricing question** | Competitor analysis + usage data | Model pricing scenarios |

### Technique: Use Traces

Capture everything users do:
- Click paths through UI
- API request/response logs
- Database query patterns
- Error stacktraces
- Session recordings

Feed to agents: "Here are 100 user sessions. Identify common patterns and friction points."

### Technique: Screen Capture

Screenshots are high-bandwidth input:
- Bug reports with visuals
- Desired UI examples
- Competitor feature comparison
- Design mockups

Agents can: Read text from images, understand layouts, generate matching code.

### Technique: Conversation Transcripts

Every customer interaction is data:
- Support tickets
- Sales calls
- User interviews
- Feature requests
- Bug reports

Feed to agents: "Here are 50 support tickets about login issues. Generate comprehensive test scenarios."

### Technique: Incident Replays

Production errors are goldmines:
- Sentry/Datadog traces
- Log aggregations
- Stack traces
- User sessions leading to errors

Feed to agents: "This error happened 30 times yesterday. Fix the root cause and add validation."

### Technique: Adversarial Use

Let agents break things:
- Security fuzzing
- Edge case generation
- Load testing
- Chaos engineering

Feed results back: "Here are 10 ways the system failed under stress. Fix them."

### Technique: Agentic Simulation

AI acting as users:
- Explore the product
- Try to complete tasks
- Identify UX problems
- Generate realistic test data

Feed results: "Agent explored the checkout flow. Found 3 blocking issues."

### Technique: Just-in-Time Surveys

Contextual user feedback:
- In-app NPS prompts
- Feature satisfaction ratings
- A/B test results

Feed to agents: "87% of users struggle with feature X. Simplify the UX."

### Technique: Customer Interviews

Convert conversations to scenarios:
- Record user interviews
- Transcribe and summarize
- Extract requirements
- Generate test scenarios

Feed to agents: "Here's what 10 enterprise customers need. Build it."

### Technique: Price Elasticity Testing

Business metrics inform technical decisions:
- Conversion rates by pricing tier
- Feature adoption by segment
- Churn analysis

Feed to agents: "Premium features have 12% conversion. Make them more compelling."

---

## Principle 5: The Validation Constraint

> "Code was treated analogously to an ML model snapshot: opaque weights whose correctness is inferred exclusively from externally observable behavior."

### Why This Matters

Traditional code review asks:
- "Is this code clean?"
- "Are there edge cases?"
- "Is it maintainable?"

Factory validation asks:
- "Does it pass all scenarios?"
- "Does it meet SLAs?"
- "Do customers get value?"

**Internal structure is opaque. Only external behavior matters.**

### Validation Levels

#### Level 1: Functional Correctness
Does it do what it's supposed to do?
```python
Scenario: API returns user data
Given: User ID 123 exists
When: GET /api/users/123
Then: Response is 200 with user data
```

#### Level 2: Performance
Does it do it fast enough?
```python
Scenario: API response time < 100ms
Given: Database has 1M users
When: GET /api/users/123
Then: Response time < 100ms (p95)
```

#### Level 3: Reliability
Does it work under load?
```python
Scenario: API handles 1000 req/sec
Given: Load test with 1000 concurrent users
When: Each user makes 10 requests
Then: Error rate < 0.1%
```

#### Level 4: Security
Is it safe?
```python
Scenario: API rejects unauthorized access
Given: No auth token provided
When: GET /api/users/123
Then: Response is 401 Unauthorized
```

#### Level 5: Business Logic
Does it make business sense?
```python
Scenario: Premium features require subscription
Given: Free tier user
When: Attempts to access premium feature
Then: Response is 403 with upgrade prompt
```

---

## Principle 6: Economics of the Agentic Moment

### What Changed

**Before (Software 1.0):**
- Writing code: Expensive (developer time)
- Code review: Expensive (senior dev time)
- Testing: Expensive (QA team)
- Maintenance: Very expensive (ongoing dev time)

**After (Software Factory):**
- Writing code: Cheap (agent tokens)
- Code review: Not needed (scenario validation)
- Testing: Cheap (agents generate + run tests)
- Maintenance: Cheap (agents fix issues)

### The New Economics

| Activity | Old Cost | New Cost | Savings |
|----------|----------|----------|---------|
| Write feature | 40 hours @ $150 = $6,000 | $100 tokens + 2 hours spec = $400 | 93% |
| Code review | 8 hours @ $200 = $1,600 | $0 (scenario validation) | 100% |
| Write tests | 16 hours @ $150 = $2,400 | $50 tokens | 98% |
| Fix bugs | 8 hours @ $150 = $1,200 | $30 tokens | 98% |
| **Total** | **$11,200** | **$580** | **95%** |

### Deliberate Naivete

When building a Software Factory, practice "deliberate naivete":

**Question everything that was "too expensive":**
- ❓ "Building a replica of our production environment for testing"
- ❓ "Comprehensive end-to-end test coverage"
- ❓ "Maintaining multiple language implementations"
- ❓ "Real-time migration of legacy code"
- ❓ "Perfect documentation for every API"

**The answer is now:** Just do it. The economics have changed.

---

## Putting It All Together

### The Factory Workflow

```
1. SEED
   ↓
   Developer writes: "Build OAuth2 login flow with Google"

2. AGENT GENERATES CODE
   ↓
   Agent creates: auth routes, Google OAuth client, token handling

3. VALIDATION HARNESS RUNS
   ↓
   Scenarios execute:
   - ✅ User can login with Google
   - ❌ User sees error with invalid state parameter
   - ✅ Tokens are stored securely
   - ❌ Token refresh fails after 24 hours

4. FEEDBACK TO AGENT
   ↓
   "2 scenarios failed. Details:
    - Invalid state parameter returns 500, should return 400
    - Token refresh not implemented"

5. AGENT ADJUSTS
   ↓
   Agent fixes validation and adds token refresh

6. LOOP CONTINUES
   ↓
   All scenarios pass → SHIP IT
```

### Success Looks Like

- **Scenario pass rate**: 95%+ on first try, 100% after 2-3 iterations
- **Human involvement**: Spec writing + validation design only
- **Time to ship**: Hours, not days/weeks
- **Quality**: Higher (comprehensive scenarios vs manual testing)
- **Cost**: Lower (tokens vs developer time)

---

## Next: Techniques

See [Techniques Documentation](../techniques/README.md) for specific patterns like:
- Digital Twin Universe
- Gene Transfusion
- Shift Work
- Semport
- Pyramid Summaries

---

**Version**: 1.0
**Last Updated**: February 2026
