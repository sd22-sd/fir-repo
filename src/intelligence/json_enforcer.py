# src/intelligence/json_enforcer.py

import json
import re
from copy import deepcopy
from .schema import FIR_SCHEMA


def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return None
        return None


def enforce_schema(data):
    """
    Ensure all keys exist according to FIR_SCHEMA.
    """

    def recursive_fill(schema, obj):
        result = deepcopy(schema)

        for key in schema:
            if key in obj:
                if isinstance(schema[key], dict):
                    result[key] = recursive_fill(schema[key], obj.get(key, {}))
                else:
                    result[key] = obj[key]
        return result

    return recursive_fill(FIR_SCHEMA, data)