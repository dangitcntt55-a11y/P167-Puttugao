"""Test schema check tool."""
import pytest
from agent.diagnosis.tools.schema_check import schema_check


@pytest.mark.asyncio
async def test_schema_check_returns_dict():
    result = await schema_check("https://example.com")
    assert isinstance(result, dict)
    assert "has_product_schema" in result or "error" in result
