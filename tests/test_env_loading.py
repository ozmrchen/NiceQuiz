import os
import pytest
from dotenv import load_dotenv, find_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Automatically load environment variables for all tests.
    """
    dotenv_path = find_dotenv()
    if not dotenv_path:
        pytest.fail("Could not find .env file")
    load_dotenv(dotenv_path)

def test_openai_api_key_loaded():
    """
    Test that the OPENAI_API_KEY environment variable is loaded correctly.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY is not set in the environment."
    assert api_key.startswith("sk-"), "OPENAI_API_KEY does not appear to be valid."