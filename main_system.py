
# Main integration file


import asyncio
import json
import os
from typing import List, Dict, Optional
from pathlib import Path

from input_processor import InputProcessor
from refinement_engine import PromptRefinementEngine
from prompt_template import RefinedPrompt


class PromptRefinementSystem:
    """Main system that orchestrates the refinement process"""
    
    def __init__(self):
        self.input_processor = InputProcessor()
        self.refinement_engine = PromptRefinementEngine()
        self.output_dir = Path("refined_prompts")
        self.output_dir.mkdir(exist_ok=True)
    
    async def process_and_refine(self, inputs: List[str], output_name: Optional[str] = None) -> Dict:
        """Main pipeline: Input → Process → Refine → Output"""
        
        print("=" * 60)
        print("MULTI-MODAL PROMPT REFINEMENT SYSTEM")
        print("=" * 60)
        
        # Step 1: Process inputs
        print("\n[1/4] Processing inputs...")
        if len(inputs) == 1:
            processed = self.input_processor.process_input(inputs[0])
        else:
            processed = self.input_processor.process_multiple_inputs(inputs)
        
        if not processed['success']:
            return {
                'status': 'failed',
                'stage': 'input_processing',
                'error': processed.get('error', 'Unknown error'),
                'result': None
            }
        
        print(f" Successfully processed {processed['type']} input")
        print(f"  Content length: {len(processed['content'])} characters")
        
        # Step 2: Check relevance
        print("\n[2/4] Validating relevance...")
        is_relevant, reason = self.refinement_engine.is_relevant_prompt(processed['content'])
        
        if not is_relevant:
            print(f" Input rejected: {reason}")
            return {
                'status': 'rejected',
                'stage': 'relevance_check',
                'reason': reason,
                'result': None
            }
        
        print(f" Input validated: {reason}")
        
        # Step 3: Refine with AI
        print("\n[3/4] Refining prompt...")
        try:
            refined_prompt = await self.refinement_engine.refine_with_claude(
                processed['content'],
                processed['metadata']
            )
            print(f" Refined prompt generated: {refined_prompt.prompt_id}")
            print(f"  Domain: {refined_prompt.domain}")
            print(f"  Confidence: {refined_prompt.confidence_score:.2f}")
        except Exception as e:
            print(f" Refinement error: {e}")
            return {
                'status': 'failed',
                'stage': 'refinement',
                'error': str(e),
                'result': None
            }
        
        # Step 4: Save outputs (WITH UTF-8 ENCODING FOR WINDOWS)
        print("\n[4/4] Saving outputs...")
        output_basename = output_name or refined_prompt.prompt_id
        
        # Save JSON with UTF-8 encoding
        json_path = self.output_dir / f"{output_basename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(refined_prompt.to_json())
        print(f" Saved JSON: {json_path}")
        
        # Save Markdown with UTF-8 encoding
        md_path = self.output_dir / f"{output_basename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(refined_prompt.to_markdown())
        print(f" Saved Markdown: {md_path}")
        
        print("\n" + "=" * 60)
        print("REFINEMENT COMPLETE")
        print("=" * 60)
        
        return {
            'status': 'success',
            'stage': 'complete',
            'result': refined_prompt,
            'files': {
                'json': str(json_path),
                'markdown': str(md_path)
            }
        }