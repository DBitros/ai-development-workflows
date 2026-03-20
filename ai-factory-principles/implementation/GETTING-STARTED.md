# Getting Started: Your First Software Factory

A practical guide to building your first Software Factory in 2 weeks.

---

## Before You Start

### Prerequisites

✅ **Access to LLM APIs** (OpenAI, Anthropic, or Gemini)
✅ **API budget** (~$100-500 for initial exploration)
✅ **Coding agent** (Claude Code, Cursor, or similar)
✅ **Existing codebase** (or willingness to start fresh)

### Mindset Shift

The hardest part isn't technical - it's mental:

❌ **Old mindset**: "I need to write this code carefully"
✅ **New mindset**: "I need to specify this intent clearly"

❌ **Old mindset**: "Let me review this code line by line"
✅ **New mindset**: "Let me write scenarios that validate behavior"

❌ **Old mindset**: "Minimize API calls to save money"
✅ **New mindset**: "Maximize API calls to save time"

---

## Week 1: Foundation

### Day 1-2: Unified LLM Client

**Goal**: Single interface across multiple LLM providers

**Option A: Use StrongDM's Spec**
```bash
# Clone their spec
git clone https://github.com/strongdm/attractor

# Feed to your coding agent
codeagent> Implement the Unified LLM Client from
           /tmp/attractor/unified-llm-spec.md
```

**Option B: Use Existing Library**
```python
# Use Vercel AI SDK, LiteLLM, or similar
pip install litellm

# Test multi-provider
from litellm import completion

# Claude
response = completion(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Hello"}]
)

# GPT
response = completion(
    model="gpt-5.2",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Success Criteria:**
- [ ] Can call 3+ providers through single interface
- [ ] Handles streaming responses
- [ ] Tracks token usage
- [ ] Costs < $10 to verify

---

### Day 3-4: Basic Agent Loop

**Goal**: Agent that can read, write, execute, iterate

**Minimal Agent:**
```python
class BasicAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.tools = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_command": self.run_command
        }

    def execute_task(self, task_description):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_description}
        ]

        while True:
            # Get LLM response
            response = self.llm.complete(
                messages=messages,
                tools=self.tools
            )

            # If no tool calls, agent is done
            if not response.tool_calls:
                return response.text

            # Execute tool calls
            for tool_call in response.tool_calls:
                result = self.execute_tool(tool_call)
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool_call.id
                })
```

**Success Criteria:**
- [ ] Agent can read files
- [ ] Agent can write files
- [ ] Agent can execute commands
- [ ] Agent iterates until task complete
- [ ] Costs < $20 for testing

---

### Day 5-7: First Automated Scenario

**Goal**: One feature validated end-to-end by agents

**Choose a Simple Feature:**
- CSV to JSON converter
- REST API endpoint (GET/POST)
- CLI tool with argument parsing
- Simple data transformation

**Example: CSV to JSON Converter**

**1. Write the Spec (Seed):**
```markdown
# CSV to JSON Converter

Build a Python CLI that converts CSV files to JSON.

## Requirements
- Accept CSV file path as argument
- Parse CSV with headers
- Output formatted JSON to stdout
- Handle edge cases (empty file, missing values)

## Success Scenarios
1. Basic: cities.csv (3 cols, 10 rows) → valid JSON
2. Large: transactions.csv (20 cols, 100k rows) in < 2 sec
3. Edge: empty.csv → empty array []
4. Edge: malformed.csv → exit code 1 with error
```

**2. Create Test Scenarios:**
```python
# scenarios/test_csv_converter.py

def test_basic_conversion():
    """Scenario: Convert simple CSV to JSON"""
    # Given: A CSV file exists
    create_file("cities.csv", """
city,population,country
Tokyo,37400068,Japan
Delhi,28514000,India
Shanghai,25582000,China
""")

    # When: User runs converter
    result = subprocess.run(
        ["python", "csv2json.py", "cities.csv"],
        capture_output=True,
        text=True
    )

    # Then: Output is valid JSON with correct data
    output = json.loads(result.stdout)
    assert len(output) == 3
    assert output[0]["city"] == "Tokyo"
    assert output[0]["population"] == "37400068"
    assert result.returncode == 0


def test_large_file_performance():
    """Scenario: Handle large files efficiently"""
    # Given: A large CSV file (100k rows)
    create_large_csv("transactions.csv", rows=100000)

    # When: User runs converter
    start = time.time()
    result = subprocess.run(
        ["python", "csv2json.py", "transactions.csv"],
        capture_output=True
    )
    duration = time.time() - start

    # Then: Completes in < 2 seconds
    assert result.returncode == 0
    assert duration < 2.0
    assert len(json.loads(result.stdout)) == 100000


def test_empty_file():
    """Scenario: Handle empty CSV gracefully"""
    create_file("empty.csv", "")

    result = subprocess.run(
        ["python", "csv2json.py", "empty.csv"],
        capture_output=True,
        text=True
    )

    output = json.loads(result.stdout)
    assert output == []
    assert result.returncode == 0
```

**3. Run Agent Through Loop:**
```bash
# First iteration
agent> Build a CSV to JSON converter according to spec.md

# Run scenarios
pytest scenarios/test_csv_converter.py
# Result: 1 passed, 2 failed

# Feed back to agent
agent> 2 scenarios failed:
       - test_large_file_performance: took 4.2 seconds (expected < 2)
       - test_empty_file: returned null instead of []

# Agent iterates
agent> [reads code, identifies issues, makes improvements]

# Run scenarios again
pytest scenarios/test_csv_converter.py
# Result: 3 passed, 0 failed

# DONE!
```

**Success Criteria:**
- [ ] All scenarios pass
- [ ] Agent required < 5 iterations
- [ ] Total token cost < $50
- [ ] You didn't write any code manually

---

## Week 2: Validation at Scale

### Day 8-9: Scenario Harness

**Goal**: Infrastructure for managing hundreds of scenarios

**Create Scenario Framework:**
```python
# scenarios/framework.py

class ScenarioRunner:
    def __init__(self):
        self.scenarios = []
        self.results = []

    def add_scenario(self, name, func):
        """Register a scenario"""
        self.scenarios.append({"name": name, "func": func})

    def run_all(self):
        """Execute all scenarios and collect results"""
        for scenario in self.scenarios:
            try:
                scenario["func"]()
                self.results.append({
                    "name": scenario["name"],
                    "status": "PASS"
                })
            except AssertionError as e:
                self.results.append({
                    "name": scenario["name"],
                    "status": "FAIL",
                    "error": str(e)
                })
            except Exception as e:
                self.results.append({
                    "name": scenario["name"],
                    "status": "ERROR",
                    "error": str(e)
                })

    def report(self):
        """Generate detailed report"""
        passed = [r for r in self.results if r["status"] == "PASS"]
        failed = [r for r in self.results if r["status"] == "FAIL"]
        errors = [r for r in self.results if r["status"] == "ERROR"]

        return {
            "total": len(self.results),
            "passed": len(passed),
            "failed": len(failed),
            "errors": len(errors),
            "pass_rate": len(passed) / len(self.results) * 100,
            "details": self.results
        }
```

**Usage:**
```python
runner = ScenarioRunner()

runner.add_scenario("Basic conversion", test_basic_conversion)
runner.add_scenario("Large file", test_large_file_performance)
runner.add_scenario("Empty file", test_empty_file)

runner.run_all()
report = runner.report()

print(f"Pass Rate: {report['pass_rate']:.1f}%")
print(f"Passed: {report['passed']}/{report['total']}")

# Feed to agent if failures
if report['failed'] > 0:
    agent.provide_feedback(report['details'])
```

**Success Criteria:**
- [ ] Can run 10+ scenarios
- [ ] Results captured automatically
- [ ] Failures reported with details
- [ ] Takes < 30 seconds to run all

---

### Day 10-11: Digital Twin (Start Simple)

**Goal**: Clone ONE external dependency you test frequently

**Choose Your First Twin:**

**Easy Starter: Email Service**
```python
class EmailTwin:
    """Mimics SendGrid/Mailgun"""
    def __init__(self):
        self.sent_emails = []

    def send(self, to, subject, body):
        """Simulates sending email"""
        email = {
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": datetime.now(),
            "status": "delivered"
        }
        self.sent_emails.append(email)
        return {"id": f"msg_{len(self.sent_emails)}", "status": "accepted"}

    def get_sent_count(self):
        return len(self.sent_emails)

    def verify_email_sent(self, to, subject_contains):
        """Test helper"""
        for email in self.sent_emails:
            if email["to"] == to and subject_contains in email["subject"]:
                return True
        return False
```

**Usage in Tests:**
```python
def test_user_signup_sends_welcome_email():
    email_twin = EmailTwin()

    # Signup new user (app uses email_twin instead of real service)
    user = signup_user("alice@example.com", email_service=email_twin)

    # Verify welcome email sent
    assert email_twin.verify_email_sent(
        to="alice@example.com",
        subject_contains="Welcome"
    )
```

**Medium Challenge: Payment Service**
```python
class StripeTwin:
    """Mimics Stripe payments"""
    def create_customer(self, email):
        # State machine (see digital-twin-universe.md)
        ...

    def create_payment_intent(self, amount, currency, customer):
        ...

    def confirm_payment(self, intent_id):
        ...
```

**Advanced: Full API Service (Okta, Jira, etc.)**
See [Digital Twin Universe guide](../techniques/digital-twin-universe.md)

**Success Criteria:**
- [ ] Twin replaces real service in tests
- [ ] Tests run 10x+ faster
- [ ] Can simulate failure modes
- [ ] Zero external API calls

---

### Day 12-14: Feedback Loop Optimization

**Goal**: Maximize agent learning from failures

**Create Structured Feedback:**
```python
def generate_feedback(scenario_results):
    """Convert test results to agent-actionable feedback"""
    feedback = []

    for result in scenario_results:
        if result["status"] == "FAIL":
            feedback.append({
                "scenario": result["name"],
                "status": "FAILED",
                "expected": extract_expected(result),
                "actual": extract_actual(result),
                "location": identify_failure_location(result),
                "suggestion": suggest_fix(result)
            })

    return format_for_agent(feedback)
```

**Example Feedback Format:**
```markdown
## Scenario Results: 3 PASSED, 2 FAILED

### ✅ PASSED
- Basic conversion
- Large file performance
- Empty file handling

### ❌ FAILED

#### Scenario: "Handle Unicode characters"
**Expected**: Characters like 北京 preserved in JSON
**Actual**: UnicodeDecodeError on line 23

**Analysis**:
- File opened without encoding specification
- Need to specify encoding='utf-8'
- Located in csv2json.py:23

**Suggested Fix**:
```python
# Change this:
with open(filepath) as f:

# To this:
with open(filepath, encoding='utf-8') as f:
```

#### Scenario: "Return exit code 1 on error"
**Expected**: Exit code 1 when CSV is malformed
**Actual**: Uncaught exception, exit code 255

**Analysis**:
- No exception handling for parse errors
- Need try/except around CSV parsing
- Located in csv2json.py:parse_csv()

**Suggested Fix**:
```python
try:
    reader = csv.DictReader(f)
    return list(reader)
except csv.Error as e:
    print(f"Error parsing CSV: {e}", file=sys.stderr)
    sys.exit(1)
```
```

**Success Criteria:**
- [ ] Failures include expected vs actual
- [ ] Failures point to specific code location
- [ ] Failures suggest fixes
- [ ] Agent fixes issues on first try (80%+ success rate)

---

## Week 3: Scale & Parallelization

### Day 15-16: Parallel Agent Execution

**Goal**: Multiple agents working simultaneously

**Pattern: Task Decomposition**
```python
# Main agent decomposes work
agent> Build user management API with authentication

# Spawns sub-agents in parallel
subagent_1> Build /register endpoint
subagent_2> Build /login endpoint
subagent_3> Build JWT token handling
subagent_4> Build password hashing

# Wait for all to complete
# Integrate results
# Run integration scenarios
```

**Success Criteria:**
- [ ] Can spawn 3+ agents in parallel
- [ ] Work is properly scoped (no conflicts)
- [ ] Integration scenarios pass
- [ ] 2-3x faster than sequential

---

### Day 17-18: Token Spend Optimization

**Goal**: Spend efficiently, not cheaply

**Measure Everything:**
```python
class TokenTracker:
    def __init__(self):
        self.calls = []

    def track(self, provider, model, tokens_in, tokens_out, cost):
        self.calls.append({
            "timestamp": datetime.now(),
            "provider": provider,
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost": cost
        })

    def daily_report(self):
        today = [c for c in self.calls if c["timestamp"].date() == date.today()]
        return {
            "total_cost": sum(c["cost"] for c in today),
            "total_calls": len(today),
            "total_tokens": sum(c["tokens_in"] + c["tokens_out"] for c in today)
        }
```

**Optimization Strategies:**

1. **Use cheaper models for simple tasks**
   ```python
   # Expensive for simple task
   response = llm.complete(model="claude-opus-4-6", prompt="Extract email")

   # Better
   response = llm.complete(model="claude-haiku-4-5", prompt="Extract email")
   ```

2. **Use expensive models for complex reasoning**
   ```python
   # Too cheap for complex task
   response = llm.complete(model="gpt-5.2-mini", prompt="Design system architecture")

   # Better
   response = llm.complete(model="gpt-5.2", prompt="Design system architecture")
   ```

3. **Implement prompt caching**
   ```python
   # Cache system prompts
   # Anthropic: Use cache_control
   # OpenAI: Automatic via Responses API
   ```

**Success Criteria:**
- [ ] Daily spend tracked
- [ ] Model selection matches task complexity
- [ ] Caching reduces costs by 50%+
- [ ] Cost per feature < traditional dev

---

### Day 19-21: Metrics & Monitoring

**Goal**: Know if your factory is working

**Key Metrics Dashboard:**
```python
class FactoryMetrics:
    def __init__(self):
        self.metrics = {
            "token_spend": 0,
            "scenarios_run": 0,
            "scenarios_passed": 0,
            "iterations_to_success": [],
            "time_to_convergence": [],
            "features_shipped": 0
        }

    def log_scenario_run(self, passed, iterations, time_seconds):
        self.metrics["scenarios_run"] += 1
        if passed:
            self.metrics["scenarios_passed"] += 1
            self.metrics["iterations_to_success"].append(iterations)
            self.metrics["time_to_convergence"].append(time_seconds)

    def report(self):
        return {
            "pass_rate": self.metrics["scenarios_passed"] / self.metrics["scenarios_run"] * 100,
            "avg_iterations": statistics.mean(self.metrics["iterations_to_success"]),
            "avg_time_to_convergence": statistics.mean(self.metrics["time_to_convergence"]),
            "token_spend_per_feature": self.metrics["token_spend"] / max(1, self.metrics["features_shipped"])
        }
```

**Success Criteria:**
- [ ] Scenario pass rate: 90%+ first try
- [ ] Avg iterations to success: < 3
- [ ] Avg time to convergence: < 1 hour
- [ ] Token spend tracked daily

---

## Week 4: Production

### Day 22-23: Ship First Feature

**Goal**: Factory-built feature in production

**Process:**
1. Write spec (seed)
2. Agent builds implementation
3. Scenarios validate behavior
4. Agent iterates to green
5. Deploy (if all scenarios pass)

**No Manual Code Review Required**

**Success Criteria:**
- [ ] Feature deployed
- [ ] All scenarios pass
- [ ] Zero production incidents in first 7 days
- [ ] Built 5-10x faster than manual

---

### Day 24-25: Monitoring & Iteration

**Goal**: Learn from production, improve factory

**What to Track:**
- Scenario pass rates over time
- Token spend trends
- Time to convergence trends
- Production incidents (should decrease)
- Developer satisfaction

**Iterate:**
- Add scenarios for any production issues
- Improve Digital Twins based on failures
- Tune agent prompts for better first-try success
- Add new techniques as needed

---

### Day 26-28: Scale Up

**Goal**: Apply factory to more features

**Expand Gradually:**
- Week 5: 2-3 features
- Week 6: 5-7 features
- Week 7: 10+ features

**Success Pattern:**
```
As factory matures:
- First-try pass rate increases (70% → 90% → 95%)
- Iterations decrease (5 → 3 → 2)
- Time to convergence decreases (hours → minutes)
- Cost per feature decreases (cheaper models work)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Insufficient Scenarios
**Symptom**: Agents pass tests but break in production
**Solution**: Write more scenarios, especially edge cases

### ❌ Pitfall 2: Vague Specs
**Symptom**: Agents iterate 10+ times without convergence
**Solution**: Be more specific about intent and success criteria

### ❌ Pitfall 3: Manual Code Writing
**Symptom**: You keep "fixing one small thing" manually
**Solution**: Feed failures back to agent, let it learn

### ❌ Pitfall 4: Premature Optimization
**Symptom**: Worrying about token costs before validating speed
**Solution**: Optimize for speed first, cost second

### ❌ Pitfall 5: Skipping Digital Twins
**Symptom**: Tests are slow, flaky, or hit rate limits
**Solution**: Build twins for frequently-tested dependencies

---

## Success Indicators

### Week 1
- ✅ Multi-provider LLM client working
- ✅ Basic agent can read/write/execute
- ✅ First feature built and validated

### Week 2
- ✅ Scenario harness managing 10+ tests
- ✅ First Digital Twin operational
- ✅ Feedback loop optimized

### Week 3
- ✅ Parallel execution working
- ✅ Token spend tracked and optimized
- ✅ Metrics dashboard live

### Week 4
- ✅ First production feature shipped
- ✅ Factory processes documented
- ✅ Ready to scale

---

## Next Steps

After your first 2 weeks:

1. **Read Advanced Techniques**
   - [Gene Transfusion](../techniques/gene-transfusion.md)
   - [Semport](../techniques/semport.md)
   - [Pyramid Summaries](../techniques/pyramid-summaries.md)

2. **Implement Full Stack**
   - [Unified LLM Client Spec](./unified-llm-client.md)
   - [Coding Agent Loop Spec](./coding-agent-loop.md)
   - [Attractor Spec](./attractor.md)

3. **Build DTU**
   - Clone your top 3 dependencies
   - Run 1000+ scenarios per hour
   - Test failure modes safely

4. **Scale Factory**
   - More features per week
   - Higher pass rates
   - Lower costs
   - Faster convergence

---

## Resources

- [StrongDM Software Factory](https://factory.strongdm.ai/)
- [Attractor GitHub](https://github.com/strongdm/attractor)
- [Digital Twin Universe Guide](../techniques/digital-twin-universe.md)

---

**Good luck building your Software Factory!** 🚀

Remember: "Why am I doing this? (implied: the model should be doing this instead)"

---

**Version**: 1.0
**Last Updated**: February 2026
