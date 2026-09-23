import base64
import json
import logging
from pathlib import Path

import requests

from app.config.settings import OLLAMA_CONFIG


logger = logging.getLogger(__name__)


class OllamaServiceError(Exception):
    """Raised when local Ollama cannot return a valid vision result."""


ANALYSIS_PROMPT = """
Analyze this image using only visible evidence. Do not invent information, guess
names or identities, or guess unreadable text. Return only valid JSON with this
exact shape:
{
  "description": "short factual description",
  "visible_text": "readable text, or empty string",
  "objects": ["confidently identified visible objects"],
  "scene": "factual scene description, or empty string",
  "tags": ["confident descriptive tags"]
}
Use an empty string when text or scene cannot be identified. Use an empty array
when no objects or tags can be confidently identified. Do not include markdown.
""".strip()


def _validate_result(result):
    if not isinstance(result, dict):
        raise OllamaServiceError("Ollama returned a non-object response")
    text_fields = ("description", "visible_text", "scene")
    if any(not isinstance(result.get(field, ""), str) for field in text_fields):
        raise OllamaServiceError("Ollama returned invalid text fields")
    for field in ("objects", "tags"):
        values = result.get(field, [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise OllamaServiceError(f"Ollama returned invalid {field}")
    return {
        "description": result.get("description", "").strip(),
        "visible_text": result.get("visible_text", "").strip(),
        "objects": [item.strip() for item in result.get("objects", []) if item.strip()],
        "scene": result.get("scene", "").strip(),
        "tags": [item.strip() for item in result.get("tags", []) if item.strip()],
    }


def analyze_image(image_path):
    """Analyze a validated image with the configured local Ollama vision model."""
    path = Path(image_path)
    if not path.is_file():
        raise OllamaServiceError("Image file not found")
    base_url = OLLAMA_CONFIG.get("base_url", "http://localhost:11434").rstrip("/")
    model = OLLAMA_CONFIG.get("model")
    if not model:
        raise OllamaServiceError("OLLAMA_MODEL is not configured")
    try:
        encoded_image = base64.b64encode(path.read_bytes()).decode("ascii")
        response = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": ANALYSIS_PROMPT, "images": [encoded_image], "format": "json", "stream": False},
            timeout=120,
        )
        if response.status_code == 404:
            raise OllamaServiceError(f"Ollama model not found: {model}")
        response.raise_for_status()
        raw_result = response.json().get("response", "")
        if not raw_result:
            raise OllamaServiceError("Ollama returned an empty response")
        return _validate_result(json.loads(raw_result))
    except OllamaServiceError:
        raise
    except requests.Timeout as error:
        raise OllamaServiceError("Ollama request timed out") from error
    except requests.RequestException as error:
        logger.exception("Ollama API request failed")
        raise OllamaServiceError("Ollama is unavailable") from error
    except (OSError, json.JSONDecodeError, ValueError) as error:
        logger.exception("Ollama response could not be parsed")
        raise OllamaServiceError("Ollama returned invalid analysis") from error


def generate_image_metadata(image_bytes):
    """
    Use Ollama (LLaVA model) to analyze an image.
    Returns a dict with 'ai_description' and 'detected_text'.
    """
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".img") as image_file:
        image_file.write(image_bytes)
        image_file.flush()
        result = analyze_image(image_file.name)
    return {
        "ai_description": result["description"],
        "detected_text": result["visible_text"] or None,
        "objects": result["objects"],
        "scene": result["scene"],
        "tags": result["tags"],
    }
