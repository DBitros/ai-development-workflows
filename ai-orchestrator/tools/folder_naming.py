"""
Auto-folder naming utilities for the multi-agent orchestrator.

Generates descriptive folder names from ticket inputs.
Example: "TICKET-123: Add caching layer" → "TICKET-123-add-caching-layer"
"""

import re
from typing import Tuple, Optional


def parse_ticket_input(ticket_input: str) -> Tuple[str, str]:
    """
    Parse ticket input to extract ticket ID and title.

    Args:
        ticket_input: Ticket string like "TICKET-123: Add caching layer" or "TICKET-123"

    Returns:
        Tuple of (ticket_id, title)

    Examples:
        >>> parse_ticket_input("TICKET-123: Add caching layer")
        ('TICKET-123', 'Add caching layer')

        >>> parse_ticket_input("TICKET-123")
        ('TICKET-123', '')

        >>> parse_ticket_input("BUG-456: Fix crash on login")
        ('BUG-456', 'Fix crash on login')
    """
    # Pattern: TICKET-123: Title or just TICKET-123
    match = re.match(r'^([A-Z]+-\d+)(?::\s*(.+))?$', ticket_input.strip(), re.IGNORECASE)

    if match:
        ticket_id = match.group(1).upper()
        title = match.group(2) or ""
        return ticket_id, title.strip()

    # If no match, assume the whole thing is ticket ID
    return ticket_input.strip(), ""


def to_kebab_case(text: str,
                   max_length: int = 50,
                   remove_words: Optional[list] = None) -> str:
    """
    Convert text to kebab-case format.

    Args:
        text: Text to convert
        max_length: Maximum length of output (default: 50)
        remove_words: List of words to remove (default: ["the", "a", "an"])

    Returns:
        Kebab-case string

    Examples:
        >>> to_kebab_case("Add caching layer")
        'add-caching-layer'

        >>> to_kebab_case("Fix the crash on login")
        'fix-crash-on-login'

        >>> to_kebab_case("This is a very long title that exceeds the maximum length", max_length=20)
        'this-is-very-long'
    """
    if remove_words is None:
        remove_words = ["the", "a", "an"]

    # Convert to lowercase
    text = text.lower()

    # Remove common noise words
    words = text.split()
    filtered_words = [w for w in words if w not in remove_words]
    text = " ".join(filtered_words) if filtered_words else text

    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Truncate to max length at word boundary
    if len(text) > max_length:
        text = text[:max_length]
        # Cut at last hyphen to avoid partial words
        if '-' in text:
            text = text.rsplit('-', 1)[0]

    return text


def generate_folder_name(ticket_input: str,
                         max_description_length: int = 50,
                         remove_words: Optional[list] = None) -> str:
    """
    Generate a descriptive folder name from ticket input.

    Args:
        ticket_input: Ticket string like "TICKET-123: Add caching layer"
        max_description_length: Maximum length for description part (default: 50)
        remove_words: List of words to remove from description (default: ["the", "a", "an"])

    Returns:
        Folder name in format: {TICKET-ID}-{description-slug} or just {TICKET-ID}

    Examples:
        >>> generate_folder_name("TICKET-123: Add caching layer")
        'TICKET-123-add-caching-layer'

        >>> generate_folder_name("BUG-456: Fix crash on login")
        'BUG-456-fix-crash-on-login'

        >>> generate_folder_name("TICKET-789")
        'TICKET-789'

        >>> generate_folder_name("FEAT-101: Implement the new user authentication system")
        'FEAT-101-implement-new-user-authentication'
    """
    ticket_id, title = parse_ticket_input(ticket_input)

    if not title:
        # No title provided, just use ticket ID
        return ticket_id

    # Convert title to kebab-case
    description_slug = to_kebab_case(
        title,
        max_length=max_description_length,
        remove_words=remove_words
    )

    # Combine ticket ID and description
    return f"{ticket_id}-{description_slug}"


def validate_folder_name(folder_name: str) -> bool:
    """
    Validate that a folder name follows the expected format.

    Args:
        folder_name: Folder name to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_folder_name("TICKET-123-add-caching")
        True

        >>> validate_folder_name("TICKET-123")
        True

        >>> validate_folder_name("invalid folder name")
        False
    """
    # Pattern: TICKET-123 or TICKET-123-description-slug
    pattern = r'^[A-Z]+-\d+(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?$'
    return bool(re.match(pattern, folder_name, re.IGNORECASE))


# Configuration defaults (can be overridden by config file)
DEFAULT_CONFIG = {
    "auto_generate": True,
    "format": "{ticket_id}-{description_slug}",
    "description_slug": {
        "lowercase": True,
        "separator": "-",
        "max_length": 50,
        "remove_words": ["the", "a", "an"]
    }
}


if __name__ == "__main__":
    # Test examples
    test_inputs = [
        "TICKET-123: Add caching layer",
        "BUG-456: Fix crash on login",
        "FEAT-789: Implement the new user authentication system",
        "TICKET-101",
        "STORY-202: Update the UI to match the new design system",
    ]

    print("Auto-Folder Naming Examples:")
    print("=" * 80)
    for ticket_input in test_inputs:
        folder_name = generate_folder_name(ticket_input)
        is_valid = validate_folder_name(folder_name)
        print(f"Input:  {ticket_input}")
        print(f"Output: {folder_name}")
        print(f"Valid:  {is_valid}")
        print("-" * 80)
