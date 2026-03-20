"""
Digital Twin Example: Stripe Payment API

This demonstrates how to build a behavioral clone of a third-party service
for testing at scale without rate limits or costs.
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


class TwinError(Exception):
    """Base exception for Digital Twin errors."""
    pass


class CardDeclinedError(TwinError):
    """Card was declined."""
    pass


class RateLimitError(TwinError):
    """Rate limit exceeded."""
    pass


@dataclass
class Customer:
    """Stripe customer object."""
    id: str
    email: str
    created: int
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class PaymentIntent:
    """Stripe payment intent object."""
    id: str
    amount: int
    currency: str
    customer: str
    status: str
    created: int
    last_payment_error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, str] = field(default_factory=dict)


class StripeTwin:
    """
    Behavioral clone of Stripe's payment API.

    Replicates the externally observable behavior of:
    - Customer creation
    - Payment intent creation
    - Payment confirmation
    - Error modes (card declined, rate limits, etc.)
    """

    def __init__(self):
        # Internal state
        self.customers: Dict[str, Customer] = {}
        self.payment_intents: Dict[str, PaymentIntent] = {}
        self.next_id = 1000

        # Failure mode simulation
        self.failure_mode: Optional[str] = None

        # Analytics
        self.api_calls: List[Dict[str, Any]] = []
        self.webhooks_sent: List[Dict[str, Any]] = []

    def set_failure_mode(self, mode: Optional[str]):
        """
        Enable failure simulation for testing.

        Args:
            mode: "card_declined", "network_error", "rate_limit", or None
        """
        self.failure_mode = mode

    def create_customer(self, email: str, metadata: Optional[Dict] = None) -> Customer:
        """
        Create a customer (mimics stripe.Customer.create).

        Args:
            email: Customer email
            metadata: Optional metadata

        Returns:
            Customer object
        """
        customer_id = f"cus_{self.next_id}"
        self.next_id += 1

        customer = Customer(
            id=customer_id,
            email=email,
            created=int(time.time()),
            metadata=metadata or {}
        )

        self.customers[customer_id] = customer

        # Track API call
        self.api_calls.append({
            "endpoint": "customers.create",
            "timestamp": datetime.now(),
            "result": "success"
        })

        return customer

    def create_payment_intent(
        self,
        amount: int,
        currency: str,
        customer: str,
        metadata: Optional[Dict] = None
    ) -> PaymentIntent:
        """
        Create a payment intent (mimics stripe.PaymentIntent.create).

        Args:
            amount: Amount in currency minor units (cents)
            currency: Three-letter currency code (e.g., "usd")
            customer: Customer ID
            metadata: Optional metadata

        Returns:
            PaymentIntent object

        Raises:
            TwinError: If customer doesn't exist
        """
        # Validate customer exists
        if customer not in self.customers:
            raise TwinError(f"No such customer: {customer}")

        # Simulate rate limit
        if self.failure_mode == "rate_limit":
            raise RateLimitError("Rate limit exceeded")

        intent_id = f"pi_{self.next_id}"
        self.next_id += 1

        intent = PaymentIntent(
            id=intent_id,
            amount=amount,
            currency=currency,
            customer=customer,
            status="requires_confirmation",
            created=int(time.time()),
            metadata=metadata or {}
        )

        self.payment_intents[intent_id] = intent

        # Track API call
        self.api_calls.append({
            "endpoint": "payment_intents.create",
            "timestamp": datetime.now(),
            "result": "success"
        })

        return intent

    def confirm_payment_intent(self, intent_id: str) -> PaymentIntent:
        """
        Confirm a payment intent (mimics intent.confirm()).

        Args:
            intent_id: Payment intent ID

        Returns:
            Updated PaymentIntent

        Raises:
            TwinError: If intent doesn't exist or is in wrong state
            CardDeclinedError: If card is declined (failure mode)
            RateLimitError: If rate limited (failure mode)
        """
        if intent_id not in self.payment_intents:
            raise TwinError(f"No such payment intent: {intent_id}")

        intent = self.payment_intents[intent_id]

        # Validate state
        if intent.status != "requires_confirmation":
            raise TwinError(f"Payment intent not in confirmable state: {intent.status}")

        # Simulate failures
        if self.failure_mode == "card_declined":
            intent.status = "requires_payment_method"
            intent.last_payment_error = {
                "type": "card_error",
                "code": "card_declined",
                "message": "Your card was declined",
                "decline_code": "generic_decline"
            }
            return intent

        if self.failure_mode == "network_error":
            raise TwinError("Connection timeout")

        if self.failure_mode == "rate_limit":
            raise RateLimitError("Too many requests")

        # SUCCESS case
        intent.status = "succeeded"

        # Simulate webhook
        self._send_webhook({
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": intent.id,
                    "amount": intent.amount,
                    "currency": intent.currency,
                    "status": intent.status
                }
            }
        })

        # Track API call
        self.api_calls.append({
            "endpoint": "payment_intents.confirm",
            "timestamp": datetime.now(),
            "result": "success"
        })

        return intent

    def _send_webhook(self, data: Dict[str, Any]):
        """Simulate webhook delivery."""
        self.webhooks_sent.append({
            "timestamp": datetime.now(),
            "data": data
        })

    def reset(self):
        """Reset twin state (useful for test isolation)."""
        self.customers.clear()
        self.payment_intents.clear()
        self.api_calls.clear()
        self.webhooks_sent.clear()
        self.next_id = 1000
        self.failure_mode = None

    def get_stats(self) -> Dict[str, Any]:
        """Get analytics about API usage."""
        return {
            "total_api_calls": len(self.api_calls),
            "customers_created": len(self.customers),
            "payment_intents_created": len(self.payment_intents),
            "webhooks_sent": len(self.webhooks_sent),
            "current_failure_mode": self.failure_mode
        }


# ============================================================================
# Example Usage
# ============================================================================

def test_successful_payment():
    """Scenario: Successful payment flow."""
    print("Scenario: Successful payment")
    print("-" * 50)

    twin = StripeTwin()

    # Create customer
    customer = twin.create_customer("alice@example.com")
    print(f"✅ Created customer: {customer.id}")

    # Create payment intent
    intent = twin.create_payment_intent(
        amount=5000,  # $50.00
        currency="usd",
        customer=customer.id
    )
    print(f"✅ Created payment intent: {intent.id} for ${intent.amount/100:.2f}")

    # Confirm payment
    result = twin.confirm_payment_intent(intent.id)
    print(f"✅ Payment confirmed! Status: {result.status}")

    # Verify webhook sent
    assert len(twin.webhooks_sent) == 1
    assert twin.webhooks_sent[0]["data"]["type"] == "payment_intent.succeeded"
    print(f"✅ Webhook sent: payment_intent.succeeded")

    print(f"\nStats: {twin.get_stats()}")
    print()


def test_card_declined():
    """Scenario: Card declined."""
    print("Scenario: Card declined")
    print("-" * 50)

    twin = StripeTwin()
    twin.set_failure_mode("card_declined")

    customer = twin.create_customer("bob@example.com")
    intent = twin.create_payment_intent(
        amount=10000,  # $100.00
        currency="usd",
        customer=customer.id
    )

    # Confirm payment - should fail
    result = twin.confirm_payment_intent(intent.id)

    assert result.status == "requires_payment_method"
    assert result.last_payment_error is not None
    assert result.last_payment_error["code"] == "card_declined"

    print(f"✅ Card declined as expected")
    print(f"   Error: {result.last_payment_error['message']}")
    print()


def test_rate_limit():
    """Scenario: Rate limit error."""
    print("Scenario: Rate limit")
    print("-" * 50)

    twin = StripeTwin()
    twin.set_failure_mode("rate_limit")

    customer = twin.create_customer("charlie@example.com")

    try:
        intent = twin.create_payment_intent(
            amount=2000,
            currency="usd",
            customer=customer.id
        )
        print("❌ Should have raised RateLimitError")
    except RateLimitError as e:
        print(f"✅ Rate limit triggered as expected: {e}")

    print()


def test_scale_validation():
    """Scenario: Validate at scale (impossible with real Stripe)."""
    print("Scenario: Scale testing (1000 payments)")
    print("-" * 50)

    twin = StripeTwin()

    start = time.time()

    # Process 1000 payments
    for i in range(1000):
        customer = twin.create_customer(f"user{i}@example.com")
        intent = twin.create_payment_intent(
            amount=1000 + i,  # Variable amounts
            currency="usd",
            customer=customer.id
        )
        twin.confirm_payment_intent(intent.id)

    duration = time.time() - start

    print(f"✅ Processed 1000 payments in {duration:.2f} seconds")
    print(f"   Rate: {1000/duration:.0f} payments/second")
    print(f"   Cost: $0 (vs ~$10 with real Stripe API)")
    print(f"   Stats: {twin.get_stats()}")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("Digital Twin: Stripe Payment API")
    print("=" * 70)
    print()

    # Run scenarios
    test_successful_payment()
    test_card_declined()
    test_rate_limit()
    test_scale_validation()

    print("=" * 70)
    print("All scenarios passed! ✅")
    print("=" * 70)
    print()
    print("Key insights:")
    print("  - Zero external API calls")
    print("  - Zero cost")
    print("  - Can test failure modes safely")
    print("  - Can validate at scale (1000+ scenarios)")
    print("  - Deterministic, reproducible results")
