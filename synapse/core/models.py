from enum import Enum
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class AgentPhase(str, Enum):
    IDLE = 'IDLE'
    ANALYZING = 'ANALYZING'
    VALIDATING = 'VALIDATING'
    EXECUTING = 'EXECUTING'

class AgentContribution(BaseModel):
    agent_id: str
    timestamp: float
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BlackboardState(BaseModel):
    contributions: List[AgentContribution] = Field(default_factory=list)
    is_compliant: bool = False
    logs: List[str] = Field(default_factory=list)

class SynapseState(BaseModel):
    current_phase: AgentPhase = AgentPhase.IDLE
    blackboard: BlackboardState

class MultimodalInput(BaseModel):
    type: Literal['IMAGE', 'VIDEO', 'AUDIO', 'TEXT', 'SENSORY']
    source_url: str
    sampling_rate: Optional[int] = None
    resolution: Optional[Dict[str, int]] = None
