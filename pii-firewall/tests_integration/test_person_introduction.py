"""
Regression: names introduced by a copular/auxiliary verb must be detected.

The linguistic filter exists to drop NER false positives in command phrases
("Compare Ana Garcia with the baseline"). It used to reject any PERSON entity
preceded by a VERB *or AUX*, which silently discarded the single most common
way a person states their name — "My name is John Doe", "I am Sarah Connor",
"The patient is Maria Lopez". Those names then reached the LLM provider in
clear text with no error and no warning.

Only a sentence-initial imperative may disqualify an entity now.
"""
import pytest

from privacy_firewall import create_firewall


def _ctx(thread: str) -> dict:
    return {
        "tenant_id": "test",
        "case_id": "regression",
        "thread_id": thread,
        "actor_id": "pytest",
    }


@pytest.fixture(scope="module")
def firewall():
    return create_firewall("generic", detector_backend="presidio")


@pytest.mark.parametrize(
    "text, name",
    [
        ("My name is John Doe", "John Doe"),
        ("I am Sarah Connor", "Sarah Connor"),
        ("The patient is Maria Lopez", "Maria Lopez"),
        ("The account holder was Robert Fisher", "Robert Fisher"),
        ("John Doe called me yesterday", "John Doe"),
        ("I met Alice Watson at the clinic", "Alice Watson"),
    ],
)
def test_person_is_anonymized(firewall, text, name):
    result = firewall.anonymize(text=text, context=_ctx(f"intro-{name}"))
    assert name not in result.sanitized_text, (
        f"PERSON leaked in clear text: {result.sanitized_text!r}"
    )
    assert "[PERSON_" in result.sanitized_text


def test_command_phrase_is_still_filtered(firewall):
    """The false-positive filter must keep working for its intended case."""
    text = "Compare Ana Garcia with the baseline"
    result = firewall.anonymize(text=text, context=_ctx("command"))
    assert result.sanitized_text == text


def test_rehydrate_restores_introduced_name(firewall):
    ctx = _ctx("roundtrip")
    anonymized = firewall.anonymize(text="My name is John Doe", context=ctx)
    assert "John Doe" not in anonymized.sanitized_text
    restored = firewall.rehydrate(text=anonymized.sanitized_text, context=ctx)
    assert restored == "My name is John Doe"
