import os
from dotenv import load_dotenv

# Path to the .env file
ENV_PATH = ".env"

def load_keys():
    """Load env variables from .env if it exists"""
    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH, override=True)
    else:
        load_dotenv()

load_keys()

def get_env(key, fallback=None):
    """Safely get env variable, fallback if not found"""
    load_keys()
    value = os.getenv(key, fallback)
    return value

def has_api_keys():
    """Check if Groq API key is present"""
    return bool(get_env("GROQ_API_KEY"))

def save_env_keys(groq_key=None, hindsight_key=None, hindsight_pipeline=None, local_model_url=None, local_model_name=None):
    """Save API keys and local model config into .env file"""
    existing_keys = {}
    
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing_keys[k.strip()] = v.strip()

    if groq_key is not None and groq_key.strip() != "":
        existing_keys["GROQ_API_KEY"] = groq_key.strip()
    if hindsight_key is not None and hindsight_key.strip() != "":
        existing_keys["HINDSIGHT_API_KEY"] = hindsight_key.strip()
    if hindsight_pipeline is not None and hindsight_pipeline.strip() != "":
        existing_keys["HINDSIGHT_PIPELINE_ID"] = hindsight_pipeline.strip()
    if local_model_url is not None and local_model_url.strip() != "":
        existing_keys["LOCAL_MODEL_URL"] = local_model_url.strip()
    if local_model_name is not None and local_model_name.strip() != "":
        existing_keys["LOCAL_MODEL_NAME"] = local_model_name.strip()

    with open(ENV_PATH, "w") as f:
        for k, v in existing_keys.items():
            f.write(f"{k}={v}\n")
            
    # Reload environment
    load_keys()


def call_local_model(model_name: str, endpoint_url: str, system_prompt: str, user_prompt: str):
    """Call local OpenAI-compatible endpoint (Ollama/LM Studio/vLLM)"""
    import requests
    url = f"{endpoint_url.rstrip('/')}/chat/completions"
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 800
    }
    response = requests.post(url, json=payload, timeout=8)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    total_tokens = result.get("usage", {}).get("total_tokens", int(len(content.split()) * 1.3))
    return content, total_tokens



