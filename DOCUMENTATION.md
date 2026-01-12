# Multi-Modal Prompt Refinement System - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Data Structures](#data-structures)
5. [Workflows](#workflows)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### Purpose
The Multi-Modal Prompt Refinement System transforms raw, unstructured inputs (text, images, PDFs, Word documents) into standardized, structured prompts suitable for AI processing, project planning, and requirements documentation.

### Key Features
- **Multi-Modal Input Processing:** Accepts text, images (OCR), PDF, DOCX files
- **Intelligent Extraction:** Automatically identifies requirements, constraints, and deliverables
- **Structured Output:** Generates both JSON (machine-readable) and Markdown (human-readable) formats
- **Relevance Validation:** Filters out non-task-related inputs
- **Multiple Interfaces:** Interactive CLI, command-line, and configuration-based processing

### Use Cases
- **Software Development:** Convert project ideas into structured requirements
- **Product Design:** Transform design mockups into feature specifications
- **Project Planning:** Standardize project proposals and requirements
- **Documentation:** Generate consistent requirement documents
- **Team Communication:** Create clear, structured task descriptions

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│  (Text, Images, PDF, DOCX, or Combinations)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   INPUT PROCESSOR                            │
│  - Text File Reader                                          │
│  - PDF Extractor (PyPDF2)                                    │
│  - DOCX Parser (python-docx)                                 │
│  - Image OCR (Tesseract/pytesseract)                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               RELEVANCE VALIDATOR                            │
│  - Keyword Analysis                                          │
│  - Length Validation                                         │
│  - Spam Detection                                            │
│  - Input Type Consideration                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              REFINEMENT ENGINE                               │
│  - Domain Detection                                          │
│  - Requirement Extraction                                    │
│  - Constraint Identification                                 │
│  - Priority Assignment                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                STRUCTURED OUTPUT                             │
│  - JSON (Machine-readable)                                   │
│  - Markdown (Human-readable)                                 │
│  - Confidence Scores                                         │
│  - Ambiguity Flags                                           │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Diagram

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│                  │     │                  │     │                  │
│  Interactive CLI │────▶│  Main System     │────▶│ Input Processor  │
│                  │     │                  │     │                  │
└──────────────────┘     └────────┬─────────┘     └──────────────────┘
                                  │
                                  │
┌──────────────────┐              │              ┌──────────────────┐
│                  │              │              │                  │
│ Config Processor │──────────────┘              │ Refinement       │
│                  │                             │ Engine           │
└──────────────────┘                             └────────┬─────────┘
                                                          │
                                                          ▼
                                                 ┌──────────────────┐
                                                 │  Prompt Template │
                                                 │  (Data Structure)│
                                                 └──────────────────┘
```

---

## Core Components

### 1. Input Processor (`input_processor.py`)

**Purpose:** Handles all input types and extracts text content

**Key Classes:**
- `InputProcessor`: Main class for processing various file formats

**Supported Formats:**
| Format | Extensions | Dependency | Notes |
|--------|-----------|------------|-------|
| Text | `.txt`, `.md` | None | Direct processing |
| PDF | `.pdf` | PyPDF2 | Text extraction only |
| DOCX | `.docx` | python-docx | Paragraphs and tables |
| Images | `.jpg`, `.png`, `.gif`, `.bmp` | Tesseract, pytesseract, Pillow | OCR required |

**Key Methods:**
```python
process_input(input_path: str) -> Dict
    # Main entry point for any input type
    
process_text(text: str) -> Dict
    # Process plain text
    
process_pdf(pdf_path: str) -> Dict
    # Extract text from PDF
    
process_docx(docx_path: str) -> Dict
    # Extract text from Word document
    
process_image(image_path: str) -> Dict
    # OCR text from image
    
process_multiple_inputs(input_paths: List[str]) -> Dict
    # Combine multiple inputs
```

**Return Format:**
```python
{
    'type': 'text|image|pdf|docx|mixed',
    'content': 'extracted text content',
    'metadata': {
        'filename': 'file.pdf',
        'length': 1234,
        'source': 'pdf_extraction'
    },
    'success': True|False,
    'error': 'error message (if any)'
}
```

---

### 2. Refinement Engine (`refinement_engine.py`)

**Purpose:** Extracts structured information from raw content

**Key Classes:**
- `PromptRefinementEngine`: Core refinement logic

**Key Methods:**
```python
is_relevant_prompt(content: str, input_type: str) -> tuple
    # Validates if input is task-related
    # Returns: (is_relevant: bool, reason: str)
    
async refine_with_claude(raw_content: str, input_metadata: Dict) -> RefinedPrompt
    # Main refinement method
    # Uses Claude API or falls back to rule-based
    
_fallback_extraction(raw_content: str, input_metadata: Dict) -> RefinedPrompt
    # Rule-based extraction when API unavailable
```

**Validation Rules:**
- Minimum 5 words for text input
- Minimum 3 words for image input (more lenient)
- Keyword presence check
- Greeting detection
- Spam pattern detection

**Domain Detection:**
```python
Domains:
- software_development: app, software, code, program, system, api
- product_design: design, ui, ux, interface, mockup, wireframe
- data_analysis: analyze, data, statistics, report, dashboard
- content_creation: content, article, blog, copy, write
- automation: automate, script, workflow, process
- other: default
```

**Requirement Extraction:**
- Authentication/Login detection
- Database/Storage detection
- UI/Interface detection
- Mobile/Responsive detection
- API/Backend detection

---

### 3. Prompt Template (`prompt_template.py`)

**Purpose:** Defines standardized data structures

**Key Classes:**

#### `PriorityLevel(Enum)`
```python
CRITICAL = "critical"
HIGH = "high"
MEDIUM = "medium"
LOW = "low"
```

#### `InputType(Enum)`
```python
TEXT = "text"
IMAGE = "image"
PDF = "pdf"
DOCX = "docx"
MIXED = "mixed"
```

#### `Requirement`
```python
@dataclass
class Requirement:
    description: str
    priority: PriorityLevel
    category: str
```

#### `TechnicalConstraint`
```python
@dataclass
class TechnicalConstraint:
    constraint_type: str
    description: str
    is_mandatory: bool
```

#### `RefinedPrompt`
```python
@dataclass
class RefinedPrompt:
    # Essential fields
    prompt_id: str
    timestamp: str
    input_types: List[InputType]
    
    # Core intent
    core_intent: str
    detailed_description: str
    domain: str
    
    # Requirements and constraints
    functional_requirements: List[Requirement]
    technical_constraints: List[TechnicalConstraint]
    
    # Expected outputs
    expected_outputs: List[str]
    deliverable_format: Optional[str]
    
    # Context and metadata
    background_context: Optional[str]
    success_criteria: List[str]
    confidence_score: float
    ambiguities: List[str]
    assumptions_made: List[str]
```

---

### 4. Main System (`main_system.py`)

**Purpose:** Orchestrates the entire refinement pipeline

**Key Classes:**
- `PromptRefinementSystem`: Main orchestrator

**Processing Pipeline:**
```python
1. Process inputs → InputProcessor
2. Validate relevance → RefinementEngine
3. Refine content → RefinementEngine
4. Save outputs → File system
```

**Key Methods:**
```python
async process_and_refine(inputs: List[str], output_name: Optional[str]) -> Dict
    # Main pipeline execution
    # Returns: status dict with result
```

**Output Structure:**
```
refined_prompts/
├── {output_name}.json     # Machine-readable
└── {output_name}.md       # Human-readable
```

---

### 5. Interactive CLI (`interactive_refinement.py`)

**Purpose:** User-friendly interactive interface

**Menu Options:**
1. Enter text directly
2. Process a single file
3. Process multiple files
4. Combine files and text
5. Run example demonstration
6. Exit

**Features:**
- Step-by-step guidance
- File path validation
- Real-time feedback
- Error handling with clear messages

---

### 6. Config Processor (`config_processor.py`)

**Purpose:** Batch processing from configuration files

**Supported Formats:**
- YAML (`.yaml`, `.yml`)
- JSON (`.json`)

**Configuration Structure:**
```yaml
projects:
  - name: project_name
    inputs:
      - path/to/file1.pdf
      - path/to/file2.txt
      - "Direct text input"
```

---

## Data Structures

### Input Processing Result
```python
{
    'type': str,              # 'text', 'image', 'pdf', 'docx', 'mixed'
    'content': str,           # Extracted text content
    'metadata': {
        'filename': str,      # Source filename
        'length': int,        # Content length
        'source': str,        # 'file', 'ocr', 'pdf_extraction', etc.
        # Type-specific metadata
    },
    'success': bool,          # Processing success status
    'error': str             # Error message (if failed)
}
```

### Refinement Result
```python
{
    'status': str,           # 'success', 'failed', 'rejected'
    'stage': str,            # Pipeline stage
    'result': RefinedPrompt, # Structured prompt (if success)
    'files': {
        'json': str,         # Path to JSON output
        'markdown': str      # Path to Markdown output
    },
    'error': str,            # Error message (if failed)
    'reason': str            # Rejection reason (if rejected)
}
```

### JSON Output Format
```json
{
  "prompt_id": "PROMPT_ABC123",
  "timestamp": "2026-01-12T10:30:00",
  "input_types": ["text"],
  "core_intent": "Build a task management application",
  "detailed_description": "Create a web-based system...",
  "domain": "software_development",
  "functional_requirements": [
    {
      "description": "User authentication",
      "priority": "critical",
      "category": "authentication"
    }
  ],
  "technical_constraints": [
    {
      "constraint_type": "platform",
      "description": "Must be web-based",
      "is_mandatory": true
    }
  ],
  "expected_outputs": ["Working application", "Source code"],
  "deliverable_format": "code",
  "confidence_score": 0.85,
  "ambiguities": ["Technology stack not specified"],
  "assumptions_made": ["Used rule-based extraction"]
}
```

---

## Workflows

### Workflow 1: Single File Processing

```
User → Select file → Validation → Processing → Output
```

**Steps:**
1. User selects a file (PDF, DOCX, image, or text)
2. System validates file exists and is readable
3. InputProcessor extracts text content
4. RefinementEngine validates relevance
5. RefinementEngine extracts structure
6. System saves JSON and Markdown outputs
7. User receives file paths

---

### Workflow 2: Multiple File Processing

```
User → Select files → Combine → Validation → Processing → Output
```

**Steps:**
1. User selects multiple files
2. InputProcessor processes each file
3. System combines extracted content
4. Single refinement process on combined content
5. Output includes metadata from all sources

---

### Workflow 3: Batch Configuration Processing

```
Config File → Parse → Loop Projects → Process Each → Summary
```

**Steps:**
1. Load configuration file (YAML/JSON)
2. Parse project definitions
3. For each project:
   - Process inputs
   - Refine content
   - Save outputs
4. Generate summary report

---

## API Reference

### InputProcessor API

```python
processor = InputProcessor()

# Process single input
result = processor.process_input("path/to/file.pdf")

# Process multiple inputs
result = processor.process_multiple_inputs([
    "file1.pdf",
    "file2.txt",
    "Direct text"
])

# Check supported formats
status = processor.get_supported_formats_status()
# Returns: {'text': True, 'pdf': True, 'docx': True, 'image': False}
```

### RefinementEngine API

```python
engine = PromptRefinementEngine()

# Check relevance
is_relevant, reason = engine.is_relevant_prompt(
    "Build an app",
    input_type="text"
)

# Refine content
refined = await engine.refine_with_claude(
    raw_content="Build a task app",
    input_metadata={'type': 'text'}
)
```

### PromptRefinementSystem API

```python
system = PromptRefinementSystem()

# Process single input
result = await system.process_and_refine(
    inputs=["path/to/file.pdf"],
    output_name="my_project"
)

# Access results
if result['status'] == 'success':
    json_path = result['files']['json']
    md_path = result['files']['markdown']
    refined_prompt = result['result']
```

### RefinedPrompt API

```python
# Convert to JSON
json_str = refined_prompt.to_json()

# Convert to Markdown
markdown_str = refined_prompt.to_markdown()

# Access fields
prompt_id = refined_prompt.prompt_id
domain = refined_prompt.domain
requirements = refined_prompt.functional_requirements
confidence = refined_prompt.confidence_score
```

---

## Configuration

### Environment Setup

**Python Version:** 3.6+

**Required Dependencies:**
```
PyPDF2>=3.0.0          # PDF processing
python-docx>=0.8.11    # DOCX processing
Pillow>=9.0.0          # Image processing
pytesseract>=0.3.10    # OCR interface
PyYAML>=6.0            # YAML config support
```

**Optional Dependencies:**
- Tesseract OCR (system-level) for image processing

### Configuration Files

**YAML Format:**
```yaml
projects:
  - name: project_one
    inputs:
      - file1.pdf
      - "text input"
  
  - name: project_two
    inputs:
      - file2.docx
```

**JSON Format:**
```json
{
  "projects": [
    {
      "name": "project_one",
      "inputs": ["file1.pdf", "text input"]
    }
  ]
}
```

### Output Configuration

**Default Output Directory:** `refined_prompts/`

**Output Files:**
- `{name}.json` - Structured data
- `{name}.md` - Human-readable format

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Module not found"
**Cause:** Missing dependencies
**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue 2: "Tesseract not found"
**Cause:** Tesseract OCR not installed or not in PATH
**Solution:** See `TESSERACT_INSTALL.md`

#### Issue 3: "UnicodeEncodeError on Windows"
**Cause:** Windows default encoding (CP1252)
**Solution:** Use `encoding='utf-8'` in file operations (already fixed in provided files)

#### Issue 4: "Input rejected: appears to be greeting"
**Cause:** Short or vague input
**Solution:**
- Provide more detailed input (10+ words)
- Include action keywords (build, create, develop)
- Use improved refinement_engine.py for images

#### Issue 5: "File not found"
**Cause:** Incorrect file path
**Solution:**
- Use absolute paths: `C:\Users\...\file.pdf`
- Or relative paths from project directory
- Check path with quotes if it contains spaces

#### Issue 6: Low confidence scores
**Cause:** Vague or incomplete input
**Solution:**
- Add technical details
- Specify requirements clearly
- Include expected deliverables
- Mention constraints and priorities

---

## Performance Considerations

### Processing Speed
- **Text:** Near-instant
- **PDF:** 1-5 seconds (depends on pages)
- **DOCX:** 1-3 seconds
- **Images:** 2-10 seconds (OCR overhead)

### Resource Usage
- **Memory:** ~50-200 MB typical
- **Disk:** Minimal (outputs are small)
- **CPU:** Moderate during OCR

### Optimization Tips
1. Preprocess images for better OCR
2. Limit PDF pages if very large
3. Use configuration files for batch processing
4. Process multiple projects in parallel (advanced)

---

## Security Considerations

### Data Privacy
- All processing is local (no external API calls in current version)
- Files are not transmitted over network
- Outputs saved locally only

### File Handling
- Input validation prevents path traversal
- Safe file operations with error handling
- UTF-8 encoding for all text files

### Best Practices
- Review outputs before sharing
- Don't process sensitive data unnecessarily
- Keep outputs directory secure
- Regular cleanup of old files

---


### Future Enhancements
- Claude API integration for intelligent extraction
- Web interface
- Database storage for history
- Template customization
- Plugin system for custom processors
- Multi-language support
- Cloud deployment options

---


### Code Structure
- Follow existing patterns
- Add docstrings to all functions
- Include type hints
- Write descriptive variable names
- Keep functions focused and small


## License and Credits

**System:** Multi-Modal Prompt Refinement System
**Purpose:** Educational and productivity tool
**Dependencies:** See requirements.txt

**Third-Party Libraries:**
- PyPDF2 - PDF text extraction
- python-docx - DOCX file parsing
- Pillow - Image processing
- pytesseract - Tesseract OCR wrapper
- PyYAML - YAML configuration support
- Tesseract OCR - Open source OCR engine

---


