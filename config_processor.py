
# Configuration-based Input System
# Allows users to specify inputs via a simple config file

import asyncio
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any

from main_system import PromptRefinementSystem


class ConfigBasedProcessor:
    """Process inputs based on configuration files"""
    
    def __init__(self, config_path: str = "input_config.yaml"):
        self.config_path = config_path
        self.system = PromptRefinementSystem()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML or JSON file"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        # Determine file type and load
        if config_file.suffix in ['.yaml', '.yml']:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        elif config_file.suffix == '.json':
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_file.suffix}")
    
    async def process_from_config(self) -> List[Dict]:
        """Process all inputs defined in config file"""
        config = self.load_config()
        
        print("=" * 70)
        print("CONFIG-BASED PROCESSING")
        print("=" * 70)
        print(f"\nLoaded config from: {self.config_path}")
        
        # Handle single input or multiple inputs
        if 'inputs' in config:
            # Single project configuration
            projects = [config]
        elif 'projects' in config:
            # Multiple projects configuration
            projects = config['projects']
        else:
            raise ValueError("Config must contain 'inputs' or 'projects' key")
        
        results = []
        
        for i, project in enumerate(projects, 1):
            print(f"\n{'='*70}")
            print(f"Processing Project {i}/{len(projects)}")
            if 'name' in project:
                print(f"Name: {project['name']}")
            print(f"{'='*70}")
            
            inputs = project.get('inputs', [])
            output_name = project.get('name', project.get('output_name'))
            
            print(f"\nInputs: {len(inputs)}")
            for inp in inputs:
                if isinstance(inp, str) and Path(inp).exists():
                    print(f"  - File: {Path(inp).name}")
                else:
                    print(f"  - Text: {str(inp)[:50]}...")
            
            result = await self.system.process_and_refine(inputs, output_name)
            results.append({
                'project': project,
                'result': result
            })
            
            # Display result
            if result['status'] == 'success':
                refined = result['result']
                print(f"\n Success!")
                print(f"   Domain: {refined.domain}")
                print(f"   Confidence: {refined.confidence_score:.1%}")
                print(f"   Output: {result['files']['markdown']}")
            else:
                print(f"\n Failed: {result.get('reason') or result.get('error')}")
        
        # Summary
        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        successful = sum(1 for r in results if r['result']['status'] == 'success')
        print(f"Total: {len(results)} | Successful: {successful} | Failed: {len(results) - successful}")
        
        return results
    
    @staticmethod
    def create_sample_config(output_path: str = "input_config.yaml"):
        """Create a sample configuration file"""
        sample_config = {
            'projects': [
                {
                    'name': 'my_first_project',
                    'inputs': [
                        'path/to/requirements.pdf',
                        'path/to/design_sketch.png',
                        'Additional context: This is for a mobile app targeting young adults'
                    ]
                },
                {
                    'name': 'my_second_project',
                    'inputs': [
                        '''
                        Build a RESTful API for managing user accounts.
                        Must include: registration, login, profile updates.
                        Should use JWT authentication.
                        Target deployment: AWS Lambda
                        '''
                    ]
                }
            ]
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(sample_config, f, default_flow_style=False, sort_keys=False)
        
        print(f" Sample config created: {output_path}")
        print("\nEdit this file to add your own inputs, then run:")
        print(f"   python config_processor.py {output_path}")


# Command-line interface
async def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--create-sample':
            # Create sample config
            output_path = sys.argv[2] if len(sys.argv) > 2 else "input_config.yaml"
            ConfigBasedProcessor.create_sample_config(output_path)
        else:
            # Process specified config file
            config_path = sys.argv[1]
            processor = ConfigBasedProcessor(config_path)
            await processor.process_from_config()
    else:
        print("Usage:")
        print("  python config_processor.py input_config.yaml        # Process config")
        print("  python config_processor.py --create-sample          # Create sample config")
        print("  python config_processor.py --create-sample my_config.yaml  # Create named sample")


if __name__ == "__main__":
    asyncio.run(main())