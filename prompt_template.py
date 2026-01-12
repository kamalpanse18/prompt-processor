
# Prompt Template Data Structure

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from enum import Enum
import json
from datetime import datetime

class PriorityLevel(Enum):
    """Priority levels for requirements"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class InputType(Enum):
    """Types of inputs processed"""
    TEXT = "text"
    IMAGE = "image"
    PDF = "pdf"
    DOCX = "docx"
    MIXED = "mixed"

@dataclass
class Requirement:
    """Individual requirement with priority"""
    description: str
    priority: PriorityLevel
    category: str

@dataclass
class TechnicalConstraint:
    """Technical constraints and limitations"""
    constraint_type: str
    description: str
    is_mandatory: bool

@dataclass
class RefinedPrompt:
    """
    Standardized output template for refined prompts
    """
    
    # ESSENTIAL FIELDS
    prompt_id: str
    timestamp: str
    input_types: List[InputType]
    
    # CORE INTENT
    core_intent: str
    detailed_description: str
    domain: str
    
    # FUNCTIONAL REQUIREMENTS
    functional_requirements: List[Requirement] = field(default_factory=list)
    
    # TECHNICAL CONSTRAINTS
    technical_constraints: List[TechnicalConstraint] = field(default_factory=list)
    
    # EXPECTED OUTPUTS
    expected_outputs: List[str] = field(default_factory=list)
    deliverable_format: Optional[str] = None
    
    # OPTIONAL CONTEXT
    background_context: Optional[str] = None
    success_criteria: List[str] = field(default_factory=list)
    additional_notes: Optional[str] = None
    
    # METADATA
    confidence_score: float = 0.0
    ambiguities: List[str] = field(default_factory=list)
    assumptions_made: List[str] = field(default_factory=list)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        data = asdict(self)
        data['input_types'] = [it.value for it in self.input_types]
        data['functional_requirements'] = [
            {**req, 'priority': req['priority'].value if isinstance(req['priority'], PriorityLevel) else req['priority']}
            for req in data['functional_requirements']
        ]
        return json.dumps(data, indent=2)
    
    def to_markdown(self) -> str:
        """Convert to human-readable markdown format"""
        md = f"""# Refined Prompt: {self.prompt_id}

## Core Intent
**Domain:** {self.domain}
**Summary:** {self.core_intent}

{self.detailed_description}

## Functional Requirements
"""
        for req in self.functional_requirements:
            priority = req.priority.value if isinstance(req.priority, PriorityLevel) else req.priority
            md += f"- [{priority.upper()}] **{req.category}**: {req.description}\n"
        
        if self.technical_constraints:
            md += "\n## Technical Constraints\n"
            for constraint in self.technical_constraints:
                mandatory = "MANDATORY" if constraint.is_mandatory else "PREFERRED"
                md += f"- [{mandatory}] **{constraint.constraint_type}**: {constraint.description}\n"
        
        if self.expected_outputs:
            md += "\n## Expected Outputs\n"
            for output in self.expected_outputs:
                md += f"- {output}\n"
            if self.deliverable_format:
                md += f"\n**Format:** {self.deliverable_format}\n"
        
        if self.success_criteria:
            md += "\n## Success Criteria\n"
            for criterion in self.success_criteria:
                md += f"- {criterion}\n"
        
        if self.ambiguities:
            md += "\n## ⚠️ Ambiguities Detected\n"
            for amb in self.ambiguities:
                md += f"- {amb}\n"
        
        if self.assumptions_made:
            md += "\n## Assumptions Made\n"
            for assumption in self.assumptions_made:
                md += f"- {assumption}\n"
        
        md += f"\n---\n*Confidence Score: {self.confidence_score:.2f} | Generated: {self.timestamp}*\n"
        
        return md