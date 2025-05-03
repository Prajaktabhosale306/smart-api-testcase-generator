import json
import requests
from typing import Any, Dict, Union
from app.utils import resolve_ref

try:
    import yaml  # For YAML support
except ImportError:
    yaml = None


class SwaggerLoader:
    def __init__(self, source: Union[str, Dict[str, Any]]):
        self.spec = self.load_spec(source)
        self.spec = self.resolve_all_refs_in_spec()  # Optionally expand $ref

    def load_spec(self, source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Loads OpenAPI/Swagger spec from a URL, file path, or raw dict.
        """
        if isinstance(source, dict):
            return source

        elif isinstance(source, str):
            if source.startswith("http://") or source.startswith("https://"):
                response = requests.get(source)
                response.raise_for_status()
                return response.json()
            else:
                with open(source, "r", encoding="utf-8") as f:
                    if source.endswith((".yaml", ".yml")) and yaml:
                        return yaml.safe_load(f)
                    else:
                        return json.load(f)
        else:
            raise TypeError(f"Unsupported spec input type: {type(source)}")

    def get_paths(self) -> Dict[str, Any]:
        """
        Returns the 'paths' section of the OpenAPI spec (with resolved $refs).
        """
        return self.spec.get("paths", {})

    def get_components(self) -> Dict[str, Any]:
        """
        Returns the 'components' section of the OpenAPI spec (with resolved $refs).
        """
        return self.spec.get("components", {})

    def resolve_all_refs_in_spec(self) -> Dict[str, Any]:
        """
        Recursively resolves all $ref references in the OpenAPI spec.
        """
        def _resolve(obj: Any) -> Any:
            if isinstance(obj, dict):
                if "$ref" in obj:
                    return resolve_ref(obj["$ref"], self.spec)
                return {k: _resolve(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_resolve(i) for i in obj]
            else:
                return obj

        return _resolve(self.spec)
