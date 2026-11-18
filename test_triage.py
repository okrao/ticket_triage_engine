import pytest
from pydantic import ValidationError
from triage import TicketTriage, get_client

def test_valid_ticket_triage_json():
    """Verify valid LLM JSON parses cleanly into the TicketTriage schema."""
    sample_json = """
    {
        "category": "Account Access",
        "priority": "Critical",
        "sentiment": "Angry",
        "department_routing": "Retention",
        "summary": "Customer locked out after two password resets and threatening cancellation before auto-pay."
    }
    """
    result = TicketTriage.model_validate_json(sample_json)
    assert result.category == "Account Access"
    assert result.priority == "Critical"
    assert result.sentiment == "Angry"
    assert result.department_routing == "Retention"
    assert "password resets" in result.summary

def test_missing_required_field_raises_error():
    """Verify Pydantic catches incomplete LLM responses missing department_routing."""
    incomplete_json = """
    {
        "category": "Billing",
        "priority": "High",
        "sentiment": "Frustrated",
        "summary": "Duplicate charge reported."
    }
    """
    with pytest.raises(ValidationError):
        TicketTriage.model_validate_json(incomplete_json)

def test_malformed_json_raises_error():
    """Verify non-JSON conversational prose from an LLM triggers ValidationError."""
    bad_llm_output = "Sure! Here is the ticket triage: Billing, High priority."
    with pytest.raises(ValidationError):
        TicketTriage.model_validate_json(bad_llm_output)

def test_missing_api_keys_raises_value_error(monkeypatch):
    """Verify get_client() fails fast with a clear message when keys are unset."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="Set OPENAI_API_KEY or GROQ_API_KEY"):
        get_client()