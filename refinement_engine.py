
# Prompt Refinement Engine

import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import uuid

from prompt_template import (
    RefinedPrompt, Requirement, TechnicalConstraint,
    PriorityLevel, InputType
)

class PromptRefinementEngine:
    """Core engine that refines inputs into structured format"""
    
    def __init__(self):
        self.relevance_keywords = [
            'build', 'create', 'develop', 'design', 'implement', 'make',
            'generate', 'analyze', 'calculate', 'write', 'produce',
            'system', 'application', 'app', 'software', 'tool', 'solution',
            'website', 'dashboard', 'platform', 'service', 'api'
        ]
    
    def is_relevant_prompt(self, content: str) -> tuple:
        """Check if input is relevant for prompt refinement"""
        content_lower = content.lower()
        
        if len(content.split()) < 5:
            return False, "Input too short (less than 5 words)"
        
        greetings = ['hello', 'hi', 'hey', 'greetings']
        if any(greeting in content_lower for greeting in greetings) and len(content.split()) < 10:
            return False, "Input appears to be a greeting"
        
        spam_patterns = ['buy now', 'click here', 'limited offer', 'act now']
        if any(pattern in content_lower for pattern in spam_patterns):
            return False, "Input appears to be spam"
        
        has_keywords = any(keyword in content_lower for keyword in self.relevance_keywords)
        if not has_keywords:
            return False, "Input does not contain task-related keywords"
        
        return True, "Input appears relevant"
    
    async def refine_with_claude(self, raw_content: str, input_metadata: Dict) -> RefinedPrompt:
        """Use Claude API to extract and structure information"""
        
        analysis_prompt = f"""You are a prompt refinement expert. Analyze the following input and extract structured information.

INPUT CONTENT:
{raw_content}

INPUT METADATA:
{json.dumps(input_metadata, indent=2)}

Extract information into this JSON format:

{{
  "core_intent": "Single sentence summary",
  "detailed_description": "2-3 sentence explanation",
  "domain": "software_development/product_design/data_analysis/content_creation/automation/other",
  "functional_requirements": [
    {{
      "description": "Requirement description",
      "priority": "critical/high/medium/low",
      "category": "Type (e.g., authentication, ui, performance)"
    }}
  ],
  "technical_constraints": [
    {{
      "constraint_type": "platform/technology/performance/security/other",
      "description": "Constraint description",
      "is_mandatory": true/false
    }}
  ],
  "expected_outputs": ["List of deliverables"],
  "deliverable_format": "code/document/design/analysis/other",
  "background_context": "Additional context or null",
  "success_criteria": ["How to measure success"],
  "confidence_score": 0.0-1.0,
  "ambiguities": ["Unclear aspects"],
  "assumptions_made": ["Assumptions made"]
}}

Return ONLY the JSON, no other text."""

        try:
            # I have used Claude API 
            # This is a placeholder for Claude API call
            return self._fallback_extraction(raw_content, input_metadata)
            
        except Exception as e:
            return self._fallback_extraction(raw_content, input_metadata)
    
    def _create_refined_prompt(self, structured_data: Dict, input_metadata: Dict) -> RefinedPrompt:
        """Convert structured data to RefinedPrompt object"""
        
        input_type_map = {
            'text': InputType.TEXT,
            'image': InputType.IMAGE,
            'pdf': InputType.PDF,
            'docx': InputType.DOCX,
            'mixed': InputType.MIXED
        }
        
        input_types = [input_type_map.get(input_metadata.get('type', 'text'), InputType.TEXT)]
        
        requirements = [
            Requirement(
                description=req['description'],
                priority=PriorityLevel(req['priority']),
                category=req['category']
            )
            for req in structured_data.get('functional_requirements', [])
        ]
        
        constraints = [
            TechnicalConstraint(
                constraint_type=const['constraint_type'],
                description=const['description'],
                is_mandatory=const['is_mandatory']
            )
            for const in structured_data.get('technical_constraints', [])
        ]
        
        return RefinedPrompt(
            prompt_id=f"PROMPT_{uuid.uuid4().hex[:8].upper()}",
            timestamp=datetime.now().isoformat(),
            input_types=input_types,
            core_intent=structured_data['core_intent'],
            detailed_description=structured_data['detailed_description'],
            domain=structured_data['domain'],
            functional_requirements=requirements,
            technical_constraints=constraints,
            expected_outputs=structured_data.get('expected_outputs', []),
            deliverable_format=structured_data.get('deliverable_format'),
            background_context=structured_data.get('background_context'),
            success_criteria=structured_data.get('success_criteria', []),
            confidence_score=structured_data.get('confidence_score', 0.5),
            ambiguities=structured_data.get('ambiguities', []),
            assumptions_made=structured_data.get('assumptions_made', [])
        )
    
    def _fallback_extraction(self, raw_content: str, input_metadata: Dict) -> RefinedPrompt:
        """Rule-based extraction when API is unavailable"""
        
        content_lower = raw_content.lower()
        
        domain = "other"
        if any(word in content_lower for word in ['app', 'software', 'code', 'program', 'system']):
            domain = "software_development"
        elif any(word in content_lower for word in ['design', 'ui', 'ux', 'interface', 'mockup']):
            domain = "product_design"
        elif any(word in content_lower for word in ['analyze', 'data', 'statistics', 'report']):
            domain = "data_analysis"
        
        requirements = []
        if 'authentication' in content_lower or 'login' in content_lower:
            requirements.append(
                Requirement("User authentication", PriorityLevel.CRITICAL, "authentication")
            )
        if 'database' in content_lower or 'data storage' in content_lower:
            requirements.append(
                Requirement("Data persistence", PriorityLevel.HIGH, "data")
            )
        
        return RefinedPrompt(
            prompt_id=f"PROMPT_{uuid.uuid4().hex[:8].upper()}",
            timestamp=datetime.now().isoformat(),
            input_types=[InputType.TEXT],
            core_intent=raw_content[:100] + "..." if len(raw_content) > 100 else raw_content,
            detailed_description=raw_content,
            domain=domain,
            functional_requirements=requirements,
            confidence_score=0.3,
            ambiguities=["Automatic extraction - may be incomplete"],
            assumptions_made=["Used rule-based extraction"]
        )