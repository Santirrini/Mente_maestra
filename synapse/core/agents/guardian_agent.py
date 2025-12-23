from typing import List
from pydantic import BaseModel
from synapse.core.models import AgentContribution

class ValidationResult(BaseModel):
    is_compliant: bool
    logs: List[str]

class GuardianAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.restricted_keywords = ["CONFIDENTIAL", "SECRET", "PRIVATE"]

    async def validate(self, contribution: AgentContribution) -> ValidationResult:
        """
        Validates the content of a contribution against security policies.
        """
        logs = []
        is_compliant = True
        
        # Check for restricted keywords
        for keyword in self.restricted_keywords:
            if keyword in contribution.content:
                is_compliant = False
                logs.append(f"Violation detected: Found restricted keyword '{keyword}'")
        
        return ValidationResult(is_compliant=is_compliant, logs=logs)
