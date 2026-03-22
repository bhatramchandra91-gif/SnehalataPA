"""
core/claude_client.py
Shared Claude API client. Works both locally (.env) and on Streamlit Cloud (st.secrets).
"""
import os
import json
import anthropic
import streamlit as st


def get_client() -> anthropic.Anthropic:
    """Get Anthropic client - works locally and on Streamlit Cloud."""
    # Try Streamlit secrets first (cloud deployment)
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        # Fall back to .env for local development
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found.\n"
            "Local: Create a .env file with ANTHROPIC_API_KEY=sk-ant-...\n"
            "Cloud: Add it in Streamlit Cloud → Settings → Secrets"
        )
    return anthropic.Anthropic(api_key=api_key)


def call_claude(prompt: str, max_tokens: int = 2000, system: str = "") -> str:
    """Make a Claude API call and return raw text response."""
    client = get_client()
    kwargs = dict(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text.strip()


def call_claude_json(prompt: str, max_tokens: int = 2000, system: str = "") -> dict:
    """Call Claude and parse JSON response. Strips markdown fences."""
    raw = call_claude(prompt, max_tokens, system)
    # Strip markdown code fences
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            try:
                return json.loads(part)
            except Exception:
                continue
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON.\nRaw (first 400 chars):\n{raw[:400]}\n\nError: {e}")
