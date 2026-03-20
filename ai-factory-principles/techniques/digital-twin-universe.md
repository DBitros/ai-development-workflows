# Digital Twin Universe (DTU)

> **Clone the externally observable behaviors of critical third-party dependencies. Validate at volumes and rates far exceeding production limits, with deterministic, replayable test conditions.**

---

## The Problem

### Testing Against Real Services is Broken

When you test against real third-party APIs:

❌ **Rate limited** - Can't run thousands of tests per hour
❌ **Costs money** - Every API call = $$
❌ **Non-deterministic** - Flaky tests, timing issues
❌ **Can't test failures** - Can't simulate outages, edge cases
❌ **Slow** - Network latency kills test speed
❌ **Shared state** - Tests interfere with each other
❌ **Production risk** - Accidentally hit prod, trigger abuse detection

### Mocking is Also Broken

When you use traditional mocks:

❌ **Drift from reality** - Mocks diverge from actual API behavior
❌ **Edge cases missed** - Don't know what you don't mock
❌ **False confidence** - Tests pass but prod fails
❌ **Maintenance burden** - Update mocks when API changes

---

## The Solution: Digital Twins

A **Digital Twin** is a behavioral clone of a third-party service that:

✅ Replicates observable API behavior
✅ Includes edge cases and error modes
✅ Runs locally with zero latency
✅ Has no rate limits or costs
✅ Provides deterministic, reproducible responses
✅ Allows dangerous failure testing
✅ Tracks call patterns for analysis

### What a Twin IS:
- A behavioral clone of API responses
- An in-memory state machine matching the real service
- A test harness that mimics production edge cases

### What a Twin IS NOT:
- A complete reimplementation (only externally observable behavior)
- A production replacement (testing only)
- A security risk (no real credentials, no real side effects)

---

## StrongDM's Digital Twin Universe

They built twins for:

1. **Okta** - Identity provider (SSO, SAML, user provisioning)
2. **Jira** - Project management (issues, workflows, webhooks)
3. **Slack** - Team communication (channels, messages, bots)
4. **Google Docs** - Document collaboration (create, edit, share)
5. **Google Drive** - File storage (upload, download, permissions)
6. **Google Sheets** - Spreadsheets (cells, formulas, sharing)

### Why These Services?

- **Critical dependencies** - App breaks if they fail
- **Complex behavior** - Many edge cases and states
- **Expensive to test** - Rate limits and API costs
- **Hard to simulate failures** - Can't make real Okta "go down"

### Impact

- **Validate at scale**: Thousands of scenarios per hour
- **Test failure modes**: Simulate outages, slow responses, corrupted data
- **Zero cost**: No API charges
- **Zero risk**: Can't accidentally affect production

---

## Building Your First Digital Twin

### Step 1: Choose a Service

**Good candidates:**
- Payment processors (Stripe, PayPal)
- Auth providers (Auth0, Okta, Firebase Auth)
- Email services (SendGrid, Mailgun)
- SMS services (Twilio)
- Cloud storage (S3, Google Cloud Storage)

**Start small:**
Pick ONE service that:
- You test frequently
- Has rate limits or costs
- Has complex behavior to simulate

### Step 2: Map External Behavior

Don't reimplement the entire service. Map what YOUR app observes.

**Example: Stripe Payment Twin**

Your app uses these Stripe APIs:
```python
# 1. Create customer
customer = stripe.Customer.create(email="user@example.com")

# 2. Create payment intent
intent = stripe.PaymentIntent.create(
    amount=1000,
    currency="usd",
    customer=customer.id
)

# 3. Confirm payment
intent.confirm()

# 4. Check status
intent.retrieve()
```

Your twin needs to support ONLY these operations, not all of Stripe.

### Step 3: Implement State Machine

```python
class StripeTwin:
    def __init__(self):
        self.customers = {}
        self.payment_intents = {}
        self.next_id = 1000

    def create_customer(self, email):
        """Mimics stripe.Customer.create()"""
        customer_id = f"cus_{self.next_id}"
        self.next_id += 1

        self.customers[customer_id] = {
            "id": customer_id,
            "email": email,
            "created": int(time.time())
        }

        return self.customers[customer_id]

    def create_payment_intent(self, amount, currency, customer):
        """Mimics stripe.PaymentIntent.create()"""
        intent_id = f"pi_{self.next_id}"
        self.next_id += 1

        # Validate customer exists
        if customer not in self.customers:
            raise TwinError("No such customer")

        self.payment_intents[intent_id] = {
            "id": intent_id,
            "amount": amount,
            "currency": currency,
            "customer": customer,
            "status": "requires_confirmation",
            "created": int(time.time())
        }

        return self.payment_intents[intent_id]

    def confirm_payment_intent(self, intent_id):
        """Mimics intent.confirm()"""
        if intent_id not in self.payment_intents:
            raise TwinError("No such payment intent")

        intent = self.payment_intents[intent_id]

        # Simulate payment processing
        if intent["status"] != "requires_confirmation":
            raise TwinError("Payment intent not in confirmable state")

        # SUCCESS case (most common)
        intent["status"] = "succeeded"

        # Could also simulate failures:
        # - intent["status"] = "requires_payment_method" (card declined)
        # - intent["status"] = "processing" (pending)

        return intent
```

### Step 4: Add Edge Cases

Real services have complex behaviors. Your twin should too.

```python
class StripeTwinAdvanced(StripeTwin):
    def __init__(self):
        super().__init__()
        self.failure_mode = None  # For testing failures

    def set_failure_mode(self, mode):
        """Enable failure simulation for testing"""
        self.failure_mode = mode

    def confirm_payment_intent(self, intent_id):
        # Simulate network error
        if self.failure_mode == "network_error":
            raise NetworkError("Connection timeout")

        # Simulate card declined
        if self.failure_mode == "card_declined":
            intent = self.payment_intents[intent_id]
            intent["status"] = "requires_payment_method"
            intent["last_payment_error"] = {
                "type": "card_error",
                "code": "card_declined",
                "message": "Your card was declined"
            }
            return intent

        # Simulate rate limit
        if self.failure_mode == "rate_limit":
            raise RateLimitError("Too many requests")

        # Normal case
        return super().confirm_payment_intent(intent_id)
```

### Step 5: Use in Tests

```python
def test_successful_payment():
    # Use twin instead of real Stripe
    stripe_twin = StripeTwinAdvanced()

    # Create customer
    customer = stripe_twin.create_customer("test@example.com")

    # Create payment intent
    intent = stripe_twin.create_payment_intent(
        amount=1000,
        currency="usd",
        customer=customer["id"]
    )

    # Confirm payment
    result = stripe_twin.confirm_payment_intent(intent["id"])

    # Assertions
    assert result["status"] == "succeeded"
    assert result["amount"] == 1000


def test_payment_failure_card_declined():
    stripe_twin = StripeTwinAdvanced()
    stripe_twin.set_failure_mode("card_declined")

    customer = stripe_twin.create_customer("test@example.com")
    intent = stripe_twin.create_payment_intent(1000, "usd", customer["id"])

    # This should fail
    result = stripe_twin.confirm_payment_intent(intent["id"])

    assert result["status"] == "requires_payment_method"
    assert "card_declined" in result["last_payment_error"]["code"]


def test_payment_failure_network_error():
    stripe_twin = StripeTwinAdvanced()
    stripe_twin.set_failure_mode("network_error")

    customer = stripe_twin.create_customer("test@example.com")
    intent = stripe_twin.create_payment_intent(1000, "usd", customer["id"])

    # This should raise exception
    with pytest.raises(NetworkError):
        stripe_twin.confirm_payment_intent(intent["id"])
```

---

## Advanced Patterns

### Pattern 1: Webhook Simulation

Real services send webhooks. Your twin should too.

```python
class StripeTwinWithWebhooks(StripeTwinAdvanced):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url
        self.webhooks_sent = []

    def confirm_payment_intent(self, intent_id):
        result = super().confirm_payment_intent(intent_id)

        # Send webhook (like real Stripe does)
        webhook_data = {
            "type": "payment_intent.succeeded",
            "data": {"object": result}
        }

        # Simulate webhook delivery
        self._send_webhook(webhook_data)

        return result

    def _send_webhook(self, data):
        # Could actually POST to webhook_url
        # Or just record for verification
        self.webhooks_sent.append(data)
```

### Pattern 2: Time-Based Behavior

Some services have time-dependent behavior.

```python
class StripeTwinWithTime(StripeTwin):
    def __init__(self):
        super().__init__()
        self.current_time = time.time()

    def advance_time(self, seconds):
        """For testing time-based behavior"""
        self.current_time += seconds

    def create_subscription(self, customer, price, trial_days=0):
        sub_id = f"sub_{self.next_id}"
        self.next_id += 1

        trial_end = self.current_time + (trial_days * 86400)

        self.subscriptions[sub_id] = {
            "id": sub_id,
            "customer": customer,
            "status": "trialing" if trial_days > 0 else "active",
            "trial_end": trial_end if trial_days > 0 else None
        }

        return self.subscriptions[sub_id]

    def check_subscription_status(self, sub_id):
        sub = self.subscriptions[sub_id]

        # If trial ended, transition to active
        if sub["status"] == "trialing" and self.current_time > sub["trial_end"]:
            sub["status"] = "active"

        return sub
```

### Pattern 3: Multi-Tenant Isolation

For testing multi-tenant scenarios.

```python
class StripeTwinMultiTenant:
    def __init__(self):
        self.tenants = {}  # tenant_id -> StripeTwin

    def get_tenant(self, tenant_id):
        if tenant_id not in self.tenants:
            self.tenants[tenant_id] = StripeTwin()
        return self.tenants[tenant_id]

    def create_customer(self, tenant_id, email):
        twin = self.get_tenant(tenant_id)
        return twin.create_customer(email)

# Usage:
twin = StripeTwinMultiTenant()

# Tenant A
customer_a = twin.create_customer("tenant_a", "user@a.com")

# Tenant B (completely isolated)
customer_b = twin.create_customer("tenant_b", "user@b.com")
```

---

## Twin Quality Checklist

### Level 1: Basic Twin
- [ ] Replicates happy path API responses
- [ ] Maintains internal state
- [ ] Returns data in correct format

### Level 2: Production-Ready Twin
- [ ] Handles error cases (4xx, 5xx)
- [ ] Validates inputs (required fields, types)
- [ ] Matches real API error messages
- [ ] Simulates rate limiting

### Level 3: Advanced Twin
- [ ] Time-based behavior
- [ ] Webhook simulation
- [ ] Failure mode injection
- [ ] State persistence (optional)
- [ ] Performance characteristics (delays)

### Level 4: Digital Twin Universe
- [ ] Multiple services interconnected
- [ ] Cross-service scenarios
- [ ] Realistic data generation
- [ ] Analytics and observability

---

## Common Pitfalls

### ❌ Don't: Reimplement Everything

```python
# BAD: Trying to implement all of Stripe
class StripeTwin:
    def create_customer(self): ...
    def update_customer(self): ...
    def delete_customer(self): ...
    def list_customers(self): ...
    def create_charge(self): ...
    def create_refund(self): ...
    # ... 100 more methods ...
```

**Why it's bad:** You'll never finish, and you'll diverge from reality.

### ✅ Do: Implement What You Use

```python
# GOOD: Only what your app needs
class StripeTwin:
    def create_customer(self, email): ...
    def create_payment_intent(self, amount, currency, customer): ...
    def confirm_payment_intent(self, intent_id): ...
    # That's it! Just what we use.
```

### ❌ Don't: Mock Response Strings

```python
# BAD: Hardcoded responses
def create_customer(self, email):
    return '{"id": "cus_123", "email": "test@example.com"}'
```

**Why it's bad:** Not stateful, not realistic, not useful.

### ✅ Do: Maintain State

```python
# GOOD: Real state machine
def create_customer(self, email):
    customer_id = f"cus_{self.next_id}"
    self.customers[customer_id] = {"id": customer_id, "email": email}
    return self.customers[customer_id]
```

---

## ROI Analysis

### Cost Comparison

**Testing with Real Stripe API:**
```
1000 test runs/day × 365 days = 365,000 API calls
At $0.01/call (conservative) = $3,650/year
Plus: Rate limit delays, flaky tests, prod risk
```

**Testing with Stripe Twin:**
```
Initial build: 8 hours @ $150/hr = $1,200
Maintenance: 2 hours/month @ $150/hr = $3,600/year
Cost: $4,800 total

Savings: $3,650 - $0 = $3,650/year in API costs
Plus: Faster tests, zero rate limits, zero prod risk
```

**Break-even:** ~4 months

### Time Savings

**With Real API:**
- Network latency: 200ms per call
- Rate limit delays: 10% of tests wait
- Total test time: 6 minutes

**With Twin:**
- In-memory: 1ms per call
- No rate limits
- Total test time: 18 seconds

**Improvement:** 20x faster test suite

---

## Examples from StrongDM

### Okta Twin

They built a behavioral clone that:
- Handles SAML auth flows
- Manages user provisioning
- Simulates SSO redirects
- Validates tokens

**Impact:** Can test thousands of auth scenarios per hour without hitting Okta's rate limits.

### Jira Twin

Replicates:
- Issue creation/updates
- Workflow transitions
- Webhook delivery
- Query API

**Impact:** Test complex issue workflows without polluting real Jira instance.

### Google Docs Twin

Simulates:
- Document CRUD operations
- Sharing/permissions
- Collaborative editing
- Version history

**Impact:** Test document integration without Google API quotas.

---

## Next Steps

1. **Identify your most-tested external dependency**
2. **Map the API surface your app uses** (5-10 methods max)
3. **Build a basic twin** (state machine, happy path)
4. **Add error cases** (failures your app must handle)
5. **Replace real API in tests** (measure speed improvement)
6. **Iterate** (add edge cases as needed)

---

## Resources

- [StrongDM DTU Showcase](https://factory.strongdm.ai/techniques/dtu)
- [Pattern: Test Double](https://martinfowler.com/bliki/TestDouble.html)
- [Building Simulation Services](https://www.hillelwayne.com/post/simulate-dependencies/)

---

**Version**: 1.0
**Last Updated**: February 2026
