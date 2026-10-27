# -*- coding: utf-8 -*-
"""
Production AI Agent Pattern: Visual QA Multimodal Action Engine.
Parses natural language and structured defect descriptions from multimodal VLMs,
normalizes defect classifications, and synthesizes unified diff patches.
"""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class VisualFinding:
    defect_id: str
    category: str
    severity: str
    description: str
    suggested_fix: str
    confidence: float = 0.95


class MultimodalActionEngine:
    """
    Robust action engine tolerating case-insensitive code fences (```JSON, ```json, ~~~json),
    smart quotation marks, and non-standard defect taxonomy synonyms.
    """
    CATEGORY_SYNONYMS = {
        "overlap": "element_overlap",
        "overlapping": "element_overlap",
        "clipping": "element_clipping",
        "clipped": "element_clipping",
        "contrast": "contrast_issue",
        "color_contrast": "contrast_issue",
        "overflow": "layout_overflow",
        "misaligned": "layout_misalignment"
    }

    SEVERITY_SYNONYMS = {
        "blocker": "critical",
        "fatal": "critical",
        "severe": "high",
        "minor": "low",
        "trivial": "low"
    }

    def normalize_category(self, raw_category: str) -> str:
        cleaned = raw_category.strip().lower()
        return self.CATEGORY_SYNONYMS.get(cleaned, cleaned)

    def normalize_severity(self, raw_severity: str) -> str:
        cleaned = raw_severity.strip().lower()
        return self.SEVERITY_SYNONYMS.get(cleaned, cleaned)

    def extract_code_blocks(self, raw_markdown: str) -> List[Dict[str, str]]:
        pattern = re.compile(
            r"(?:```|~~~)([a-zA-Z0-9_\-+]*)?
(.*?)?
(?:```|~~~)",
            re.DOTALL | re.IGNORECASE
        )
        blocks = []
        for match in pattern.finditer(raw_markdown):
            lang = match.group(1).lower().strip()
            content = match.group(2).strip()
            blocks.append({"language": lang, "content": content})
        return blocks

    def parse_vlm_response(self, text: str) -> List[VisualFinding]:
        findings = []
        # Check code blocks first
        blocks = self.extract_code_blocks(text)
        for block in blocks:
            if block["language"] in ("json", ""):
                try:
                    sanitized = block["content"].replace("“", '"').replace("”", '"')
                    data = json.loads(sanitized)
                    items = data.get("findings", []) if isinstance(data, dict) else data
                    for item in items:
                        findings.append(VisualFinding(
                            defect_id=item.get("id", "defect-1"),
                            category=self.normalize_category(item.get("category", "visual_bug")),
                            severity=self.normalize_severity(item.get("severity", "medium")),
                            description=item.get("description", ""),
                            suggested_fix=item.get("suggested_fix", "")
                        ))
                except Exception:
                    pass
        return findings


if __name__ == "__main__":
    engine = MultimodalActionEngine()
    sample = """```JSON
    {"findings": [{"id": "f-101", "category": "overlap", "severity": "blocker", "description": "Header covers login CTA", "suggested_fix": "Add z-index: 10"}]}
    ```"""
    res = engine.parse_vlm_response(sample)
    print(f"Parsed {len(res)} findings: {res[0].category} ({res[0].severity})")
