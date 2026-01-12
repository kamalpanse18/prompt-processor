# Interactive Multi-Modal Prompt Refinement System

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Optional

from main_system import PromptRefinementSystem


class InteractiveRefinementCLI:
    """Interactive command-line interface"""
    
    def __init__(self):
        self.system = PromptRefinementSystem()
    
    def print_header(self):
        print("\n" + "=" * 70)
        print("  PROMPT REFINEMENT SYSTEM - INTERACTIVE MODE".center(70))
        print("=" * 70)
        print("\nTransform your inputs into structured prompts!")
        print("Supports: Text, PDF, DOCX, Images\n")
    
    def print_menu(self):
        print("\n" + "-" * 70)
        print("MENU OPTIONS:")
        print("-" * 70)
        print("1. Enter text directly")
        print("2. Process a single file")
        print("3. Process multiple files")
        print("4. Combine files and text")
        print("5. Run example")
        print("6. Exit")
        print("-" * 70)
    
    def get_text_input(self) -> str:
        print("\n Enter your text (press Enter twice when done):")
        print("-" * 70)
        lines = []
        empty_count = 0
        while empty_count < 1:
            line = input()
            if line.strip() == "":
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        return "\n".join(lines)
    
    def get_file_input(self, prompt="Enter file path") -> Optional[str]:
        while True:
            print(f"\n {prompt} (or 'cancel'):")
            file_path = input("   > ").strip()
            
            if file_path.lower() == 'cancel':
                return None
            
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            
            if os.path.exists(file_path):
                print(f"   ✓ Found: {os.path.basename(file_path)}")
                return file_path
            else:
                print(f"   ✗ File not found: {file_path}")
    
    def get_multiple_files(self) -> List[str]:
        files = []
        print("\n📁 Enter file paths (one per line, empty to finish):")
        while True:
            file_path = input(f"   File {len(files) + 1} (or Enter): ").strip()
            if not file_path:
                break
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            if os.path.exists(file_path):
                files.append(file_path)
                print(f"      ✓ Added: {os.path.basename(file_path)}")
        return files
    
    async def process_option_1(self):
        print("\n" + "=" * 70)
        print("OPTION 1: TEXT INPUT")
        print("=" * 70)
        text = self.get_text_input()
        if text.strip():
            output_name = input("\n Output name (optional): ").strip() or None
            result = await self.system.process_and_refine([text], output_name)
            self.display_result(result)
    
    async def process_option_2(self):
        print("\n" + "=" * 70)
        print("OPTION 2: SINGLE FILE")
        print("=" * 70)
        file_path = self.get_file_input()
        if file_path:
            output_name = input("\n Output name (optional): ").strip() or None
            result = await self.system.process_and_refine([file_path], output_name)
            self.display_result(result)
    
    async def process_option_3(self):
        print("\n" + "=" * 70)
        print("OPTION 3: MULTIPLE FILES")
        print("=" * 70)
        files = self.get_multiple_files()
        if files:
            output_name = input("\n Output name (optional): ").strip() or None
            result = await self.system.process_and_refine(files, output_name)
            self.display_result(result)
    
    async def process_option_4(self):
        print("\n" + "=" * 70)
        print("OPTION 4: COMBINED INPUT")
        print("=" * 70)
        inputs = []
        files = self.get_multiple_files()
        inputs.extend(files)
        add_text = input("\n   Add text? (y/n): ").lower()
        if add_text == 'y':
            text = self.get_text_input()
            if text.strip():
                inputs.append(text)
        if inputs:
            output_name = input("\n Output name (optional): ").strip() or None
            result = await self.system.process_and_refine(inputs, output_name)
            self.display_result(result)
    
    async def process_option_5(self):
        print("\n" + "=" * 70)
        print("OPTION 5: EXAMPLE")
        print("=" * 70)
        example = "Build a task management web app with user authentication"
        print(f"\nExample: {example}")
        result = await self.system.process_and_refine([example], "example_task_app")
        self.display_result(result)
    
    def display_result(self, result: dict):
        print("\n" + "=" * 70)
        print("RESULT")
        print("=" * 70)
        if result['status'] == 'success':
            refined = result['result']
            print("\n SUCCESS!")
            print(f"   Prompt ID: {refined.prompt_id}")
            print(f"   Domain: {refined.domain}")
            print(f"   Confidence: {refined.confidence_score:.1%}")
            print(f"\n Output files:")
            print(f"   {result['files']['markdown']}")
        else:
            print(f"\n FAILED: {result.get('reason') or result.get('error')}")
    
    async def run(self):
        self.print_header()
        while True:
            self.print_menu()
            try:
                choice = input("\nSelect option (1-6): ").strip()
                if choice == '1':
                    await self.process_option_1()
                elif choice == '2':
                    await self.process_option_2()
                elif choice == '3':
                    await self.process_option_3()
                elif choice == '4':
                    await self.process_option_4()
                elif choice == '5':
                    await self.process_option_5()
                elif choice == '6':
                    print("\n Goodbye!")
                    break
                else:
                    print("\n  Invalid option")
                if choice in ['1', '2', '3', '4', '5']:
                    input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\n\n Exiting...")
                break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Quick mode
        system = PromptRefinementSystem()
        asyncio.run(system.process_and_refine(sys.argv[1:]))
    else:
        # Interactive mode
        cli = InteractiveRefinementCLI()
        asyncio.run(cli.run())