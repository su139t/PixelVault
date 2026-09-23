import json
import sys

from app.services.ollama_service import OllamaServiceError, analyze_image


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python test_ollama.py /path/to/image")
    try:
        result = analyze_image(sys.argv[1])
    except OllamaServiceError as error:
        raise SystemExit(f"Ollama test failed: {error}") from error

    print("========= OLLAMA RESULT =========")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()