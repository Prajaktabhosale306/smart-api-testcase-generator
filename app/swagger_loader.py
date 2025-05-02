# app/swagger_loader.py

import json
import requests
from typing import Any, Dict, Union
from app.utils import resolve_ref

class SwaggerLoader:
    def __init__(self, source: Union[str, Dict[str, Any]]):
        self.spec = self.load_spec(source)
    
    def load_spec(self, source: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Loads OpenAPI/Swagger spec from a URL, file path, or raw dict.
        """
        if isinstance(source, dict):
            return source
        elif source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source)
            response.raise_for_status()
            return response.json()
        else:
            with open(source, "r", encoding="utf-8") as f:
                return json.load(f)

    def get_paths(self) -> Dict[str, Any]:
        """
        Returns the 'paths' section of the OpenAPI spec.
        """
        return self.spec.get("paths", {})

    def get_components(self) -> Dict[str, Any]:
        """
        Returns the 'components' section of the OpenAPI spec.
        """
        return self.spec.get("components", {})

    def resolve_all_refs_in_spec(self) -> Dict[str, Any]:
        """
        Optional: You can expand and resolve all $ref objects in the spec recursively.
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
