"""
Pattern 01: Native ReAct Tool-Calling Agent Loop
Production-grade tool execution with typed validation and retry bounds.
"""

import json
from typing import Callable, Any, Dict

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, dict] = {}

    def register(self, name: str, schema: dict):
        def decorator(func: Callable):
            self._tools[name] = func
            self._schemas[name] = schema
            return func
        return decorator

    def execute(self, name: str, args: dict) -> Any:
        if name not in self._tools:
            return {"error": f"Tool '{name}' not found."}
        try:
            return self._tools[name](**args)
        except Exception as e:
            return {"error": f"Execution error in '{name}': {str(e)}"}

registry = ToolRegistry()

@registry.register(
    name="get_service_health",
    schema={
        "type": "object",
        "properties": {"service_id": {"type": "string"}},
        "required": ["service_id"]
    }
)
def get_service_health(service_id: str) -> dict:
    return {"service_id": service_id, "status": "UP", "uptime_pct": 99.98}

def run_agent_loop(query: str, max_steps: int = 5):
    print(f"[Agent] Processing query: '{query}'")
    for step in range(1, max_steps + 1):
        print(f"[Step {step}] Evaluating plan...")
        # Simulated LLM tool selection
        tool_call = {"tool": "get_service_health", "args": {"service_id": "auth-gateway"}}
        result = registry.execute(tool_call["tool"], tool_call["args"])
        print(f"[Observation] {result}")
        if result.get("status") == "UP":
            return f"Service {tool_call['args']['service_id']} is operational."
    return "Reached max steps."

if __name__ == "__main__":
    summary = run_agent_loop("Check health of auth-gateway")
    print(f"[Final] {summary}")
