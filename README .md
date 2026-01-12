# Multi-Modal Prompt Refinement System

> Transform raw inputs (text, images, PDFs, Word documents) into structured, actionable prompts for AI processing and project planning.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

The **Multi-Modal Prompt Refinement System** is a Python-based tool that converts various input types into standardized, structured prompts. It's perfect for:

- 📝 **Software Developers** - Convert project ideas into structured requirements
- 🎨 **Product Designers** - Transform mockups into feature specifications
- 📊 **Project Managers** - Standardize project proposals
- 🤖 **AI Engineers** - Generate consistent prompts for LLMs
- 👥 **Teams** - Create clear, structured task descriptions

### What It Does

```
INPUT (Raw & Unstructured)          OUTPUT (Structured & Actionable)
┌─────────────────────┐            ┌────────────────────────────┐
│ Text descriptions   │            │ ✓ Core intent              │
│ Design mockups      │    ───►    │ ✓ Functional requirements  │
│ PDF requirements    │            │ ✓ Technical constraints    │
│ Word documents      │            │ ✓ Expected deliverables    │
└─────────────────────┘            │ ✓ Priority levels          │
                                   │ ✓ Confidence scores        │
                                   └────────────────────────────┘
```

---

## ✨ Features

### 🎯 Core Capabilities

- **Multi-Modal Input Processing**
  - ✅ Plain text (direct input or files)
  - ✅ PDF documents (text extraction)
  - ✅ Word documents (.docx)
  - ✅ Images (OCR with Tesseract)
  - ✅ Multiple files at once

- **Intelligent Extraction**
  - 🔍 Automatic domain detection (software, design, analysis, etc.)
  - 📌 Requirement identification with priority levels
  - ⚙️ Technical constraint extraction
  - 🎯 Deliverable specification
  - 📊 Confidence scoring

- **Flexible Interfaces**
  - 💻 Interactive CLI menu system
  - ⚡ Quick command-line processing
  - 📁 Batch processing via configuration files
  - 🔄 Single or multiple input handling

- **Structured Outputs**
  - 📄 JSON format (machine-readable)
  - 📝 Markdown format (human-readable)
  - 🏷️ Metadata and provenance tracking
  - ⚠️ Ambiguity flagging

---

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### 30-Second Setup

```bash
# 1. Clone or download the project
cd prompt-refinement-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run interactive mode
python interactive_refinement.py
```

That's it! You're ready to go! 🎉

---

## 📥 Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `PyPDF2` - PDF processing
- `python-docx` - Word document processing
- `Pillow` - Image processing
- `pytesseract` - OCR interface
- `PyYAML` - Configuration file support

### Step 2: Install Tesseract OCR (Optional, for images)

**Only needed if you want to process image files.**

#### Windows
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Add to PATH during installation

#### macOS
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### Step 3: Verify Installation

```bash
python system_check.py
```

This will show you what's installed and what's working.

---

## 💻 Usage

### Method 1: Interactive Mode (Recommended for Beginners)

The easiest way to use the system:

```bash
python interactive_refinement.py
```

You'll see a menu:

```
======================================================================
              PROMPT REFINEMENT SYSTEM - INTERACTIVE MODE
======================================================================

MENU OPTIONS:
----------------------------------------------------------------------
1. Enter text directly
2. Process a single file
3. Process multiple files
4. Combine files and text
5. Run example demonstration
6. Exit
----------------------------------------------------------------------
Select option (1-6):
```

**Example Session:**

```bash
Select option (1-6): 1

📝 Enter your text (press Enter twice when done):
----------------------------------------------------------------------
Build a task management web application with user authentication,
task creation, editing, deletion, and priority levels.
Must work on both desktop and mobile devices.

[Press Enter]
[Press Enter]

💾 Output name (optional): task_manager

[Processing...]
✅ SUCCESS!
📁 Output files:
   refined_prompts/task_manager.md
```

---

### Method 2: Command Line (Fastest)

For quick, one-off processing:

```bash
# Process text
python interactive_refinement.py "Build a mobile fitness tracking app"

# Process a file
python interactive_refinement.py requirements.pdf

# Process multiple files
python interactive_refinement.py spec.pdf design.png notes.txt

# Mix files and text
python interactive_refinement.py requirements.pdf "Additional: budget is $50k"
```

---

### Method 3: Configuration File (Best for Batches)

For processing multiple projects at once:

**Step 1: Create a config file** (`my_projects.yaml`)

```yaml
projects:
  - name: web_app
    inputs:
      - requirements.pdf
      - "Must support 10k concurrent users"
  
  - name: mobile_app
    inputs:
      - mobile_spec.docx
      - mockup.png
  
  - name: api_service
    inputs:
      - |
        Build a RESTful API with:
        - User authentication
        - CRUD operations
        - Rate limiting
```

**Step 2: Process the config**

```bash
python config_processor.py my_projects.yaml
```

---

## 📚 Examples

### Example 1: Text Input

**Input:**
```bash
python interactive_refinement.py "Create an e-commerce platform for handmade crafts with vendor storefronts, product listings, shopping cart, and payment processing."
```

**Output:** (`refined_prompts/PROMPT_*.md`)
```markdown
# Refined Prompt: PROMPT_ABC123

## Core Intent
**Domain:** software_development
**Summary:** Create an e-commerce platform for handmade crafts

## Functional Requirements
- [CRITICAL] **authentication**: User authentication and vendor accounts
- [CRITICAL] **core_functionality**: Product listing and management
- [HIGH] **payment**: Shopping cart and payment processing

## Expected Outputs
- Working web application
- Source code
- Documentation
```

---

### Example 2: PDF Processing

**Input:**
```bash
python interactive_refinement.py project_requirements.pdf
```

**What happens:**
1. ✅ Extracts text from PDF
2. ✅ Analyzes content
3. ✅ Generates structured output
4. ✅ Saves to `refined_prompts/`

---

### Example 3: Multiple Files

**Input:**
```bash
python interactive_refinement.py requirements.pdf design_mockup.png notes.txt
```

**What happens:**
1. ✅ Processes each file
2. ✅ Combines extracted content
3. ✅ Creates unified structured output
4. ✅ Tracks all sources in metadata

---

### Example 4: Batch Processing

**Config file:** (`startup_mvp.yaml`)
```yaml
projects:
  - name: authentication
    inputs:
      - auth_requirements.pdf
      - "Priority: CRITICAL"
  
  - name: payment_integration
    inputs:
      - payment_spec.docx
      - stripe_docs.png
  
  - name: user_dashboard
    inputs:
      - dashboard_mockup.png
      - user_stories.txt
```

**Process:**
```bash
python config_processor.py startup_mvp.yaml
```

**Output:**
```
Processing batch item 1/3
✓ authentication: Success

Processing batch item 2/3
✓ payment_integration: Success

Processing batch item 3/3
✓ user_dashboard: Success

Total Processed: 3
✓ Successful: 3
```

---

## 📖 Documentation

### Complete Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete technical documentation
- **[VSCODE_STEP_BY_STEP.md](VSCODE_STEP_BY_STEP.md)** - Detailed setup guide for VS Code
- **[CUSTOM_INPUT_GUIDE.md](CUSTOM_INPUT_GUIDE.md)** - How to use your own files
- **[UNDERSTANDING_GUIDE.md](UNDERSTANDING_GUIDE.md)** - How the system works

### Troubleshooting Guides

- **[WINDOWS_FIX.md](WINDOWS_FIX.md)** - Windows encoding issues
- **[TESSERACT_INSTALL.md](TESSERACT_INSTALL.md)** - Tesseract OCR setup
- **[TESSERACT_PATH_FIX.md](TESSERACT_PATH_FIX.md)** - PATH configuration
- **[IMAGE_OCR_GUIDE.md](IMAGE_OCR_GUIDE.md)** - Image processing tips

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

---

#### ❌ "Tesseract not found" (when processing images)

**Quick Fix:**
1. Images not needed? Skip them - use text/PDF/DOCX instead
2. Need images? Install Tesseract - see [TESSERACT_INSTALL.md](TESSERACT_INSTALL.md)

---

#### ❌ "File not found"

**Solution:**
- Use absolute paths: `C:\Users\...\file.pdf`
- Or run from the same directory as your files
- Put quotes around paths with spaces

---

#### ❌ "Input rejected"

**Solution:**
- Make input longer (10+ words)
- Include action keywords: build, create, develop, design
- Add more detail about requirements

---

#### ❌ Windows encoding error

**Solution:**
Already fixed in provided files! If you still see it:
1. Download fixed `main_system.py`
2. Replace your current file
3. See [WINDOWS_FIX.md](WINDOWS_FIX.md)

---

### Check System Status

Run this anytime to see what's working:

```bash
python system_check.py
```

Output:
```
✅ Essential: OK
   - Python 3.6+: ✅
   - Project files: ✅

📄 File Format Support:
   - Text files (.txt, .md): ✅ Always supported
   - PDF files (.pdf): ✅
   - Word documents (.docx): ✅
   - Images (.jpg, .png): ❌ (Tesseract needed)
```

---

## 📂 Project Structure

```
prompt-refinement-system/
│
├── 📄 Core System Files
│   ├── prompt_template.py          # Data structures
│   ├── input_processor.py          # File processing
│   ├── refinement_engine.py        # Extraction logic
│   └── main_system.py              # Main orchestrator
│
├── 🎯 User Interfaces
│   ├── interactive_refinement.py   # Interactive CLI
│   └── config_processor.py         # Batch processor
│
├── 🔧 Configuration & Setup
│   ├── requirements.txt            # Dependencies
│   └── input_config_template.yaml # Config template
│ 
├── 📚 Documentation
│   ├── README.md                   # This file
│   └── DOCUMENTATION.md            # Technical docs
│
└── 📁 Output Directory
    └── refined_prompts/            # Generated outputs (auto-created)
        ├── *.json                  # Machine-readable
        └── *.md                    # Human-readable
```

---

## 🎯 Use Cases

### Software Development

```bash
# Convert vague idea to structured requirements
python interactive_refinement.py "Build a social media app for pet owners"

# Output: Complete requirement spec with priorities and constraints
```

### Product Design

```bash
# Process design mockup
python interactive_refinement.py design_mockup.png

# Output: Feature list extracted from visual design
```

### Project Management

```bash
# Standardize project proposal
python interactive_refinement.py project_proposal.docx

# Output: Structured project spec with deliverables
```

### Team Collaboration

```bash
# Process multiple input sources
python interactive_refinement.py spec.pdf mockup.png meeting_notes.txt

# Output: Unified requirement document
```

---

## 🔐 Privacy & Security

- ✅ **100% Local Processing** - No data sent to external servers
- ✅ **No Cloud Dependencies** - All processing happens on your machine
- ✅ **File Safety** - Input files are never modified
- ✅ **Output Control** - All outputs saved locally in `refined_prompts/`

---

## 🛠️ System Requirements

### Minimum Requirements
- **OS:** Windows 10+, macOS 10.14+, or Linux
- **Python:** 3.6 or higher
- **RAM:** 2 GB minimum
- **Disk Space:** 100 MB for system + space for outputs

### Recommended for Best Performance
- **OS:** Windows 11, macOS 12+, or Ubuntu 20.04+
- **Python:** 3.9 or higher
- **RAM:** 4 GB or more
- **Disk Space:** 500 MB

---

## 📊 Performance

### Processing Speed

| Input Type | Size | Time |
|------------|------|------|
| Text | 10 KB | < 1 second |
| PDF | 50 pages | 2-5 seconds |
| DOCX | 20 pages | 1-3 seconds |
| Image | 1920x1080 | 3-8 seconds |
| Multiple files | 5 files | 5-15 seconds |

*Times are approximate and depend on system specifications.*

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Report Issues
1. Check existing issues
2. Create detailed bug report
3. Include system info and error messages

### Suggest Features
1. Open feature request
2. Describe use case
3. Provide examples

### Submit Code
1. Fork the repository
2. Create feature branch
3. Follow existing code style
4. Add tests if applicable
5. Submit pull request

---


## 🙏 Acknowledgments

### Dependencies
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX parsing
- **Pillow** - Image processing
- **pytesseract** - Tesseract OCR wrapper
- **PyYAML** - YAML configuration
- **Tesseract OCR** - Open source OCR engine

### Inspiration
Built to solve the common problem of inconsistent requirement gathering and documentation across teams and projects.

---


### Getting Help

1. **Check Documentation:**
   - Start with this README
   - See [UNDERSTANDING_GUIDE.md](UNDERSTANDING_GUIDE.md) for concepts
   - Check specific guides for your issue

2. **Run System Check:**
   ```bash
   python system_check.py
   ```

3. **Common Issues:**
   - See [Troubleshooting](#troubleshooting) section above
   - Check platform-specific guides

4. **Still Stuck?**
   - Review error messages carefully
   - Check you're running from correct directory
   - Verify all dependencies installed

---


## 📈 Quick Tips

### Get Better Results

1. **Be Specific:** Include technical details, constraints, and requirements
2. **Use Keywords:** Include words like "build", "create", "implement", "design"
3. **Add Context:** Mention target users, timeline, budget constraints
4. **Combine Inputs:** Use multiple files for complete picture
5. **Review Output:** Check ambiguities section for areas to clarify

### Process Faster

1. **Text First:** Text input is fastest
2. **Batch Process:** Use config files for multiple projects
3. **Preprocess Images:** Improve quality before OCR
4. **Reuse Config:** Save successful configurations

---

## 🎓 Learning Resources

### For Beginners
1. Run the example (Option 5 in interactive mode)
2. Try processing your own text
3. Gradually add more complex inputs

### For Advanced Users
1. Read [DOCUMENTATION.md](DOCUMENTATION.md) for architecture
2. Explore configuration file options
3. Customize data structures in `prompt_template.py`
4. Add custom domain detection in `refinement_engine.py`

---


## ⭐ Star This Project

If you find this tool useful, please consider starring the repository!

---


**Built with ❤️ for better requirement gathering and project planning**

---


**Ready to get started? Run:**
```bash
python interactive_refinement.py
```

**Happy prompt refining! 🎉**
