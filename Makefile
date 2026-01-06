# Career Architect - Makefile
# ===========================

.PHONY: help install check build build-all build-latest watch clean lint

# Default target
help:
	@echo "Career Architect - Build Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install     Install Python dependencies"
	@echo "  make check       Verify all required tools are installed"
	@echo ""
	@echo "Building:"
	@echo "  make build       Build most recent application (default)"
	@echo "  make build-all   Build all applications that need updating"
	@echo "  make build APP=<name>  Build specific application"
	@echo ""
	@echo "Development:"
	@echo "  make watch       Watch for changes and auto-rebuild"
	@echo "  make clean       Remove generated files"
	@echo "  make lint        Check Python code style"
	@echo ""
	@echo "Examples:"
	@echo "  make build APP=2025-01-06-acme-senior-engineer"
	@echo ""

# Setup
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

check:
	@echo "🔍 Checking required tools..."
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found"; exit 1; }
	@command -v pandoc >/dev/null 2>&1 || { echo "❌ Pandoc not found. Install: https://pandoc.org/installing.html"; exit 1; }
	@command -v pdflatex >/dev/null 2>&1 || { echo "❌ pdflatex not found. Install LaTeX distribution."; exit 1; }
	@echo "✅ All required tools are installed"
	@echo ""
	@echo "Tool versions:"
	@python3 --version
	@pandoc --version | head -1
	@pdflatex --version | head -1

# Building
build:
ifdef APP
	@echo "🔨 Building application: $(APP)"
	python scripts/compile_all.py --application "$(APP)"
else
	@echo "🔨 Building most recent application..."
	python scripts/compile_all.py
endif

build-all:
	@echo "🔨 Building all applications..."
	python scripts/compile_all.py --all

build-latest:
	@echo "🔨 Building most recent application..."
	python scripts/compile_all.py

# Development
watch:
	@echo "👀 Watching for changes in applications/..."
	@echo "Press Ctrl+C to stop"
	@while true; do \
		find applications -name "*.md" -newer .last_build 2>/dev/null | head -1 | grep -q . && \
		make build && touch .last_build; \
		sleep 2; \
	done

clean:
	@echo "🧹 Cleaning generated files..."
	find applications -name "*.pdf" -type f -delete 2>/dev/null || true
	find applications -name "*.docx" -type f -delete 2>/dev/null || true
	find applications -name "*.txt" -type f -delete 2>/dev/null || true
	find . -name "*.aux" -type f -delete 2>/dev/null || true
	find . -name "*.log" -type f -delete 2>/dev/null || true
	find . -name "*.out" -type f -delete 2>/dev/null || true
	rm -f .last_build
	@echo "✅ Cleaned"

lint:
	@echo "🔍 Checking Python code..."
	@python3 -m py_compile scripts/build_resume.py && echo "✅ build_resume.py OK"
	@python3 -m py_compile scripts/compile_all.py && echo "✅ compile_all.py OK"

# Create new application directory
new:
ifndef COMPANY
	@echo "❌ Usage: make new COMPANY=acme ROLE=senior-engineer"
	@exit 1
endif
ifndef ROLE
	@echo "❌ Usage: make new COMPANY=acme ROLE=senior-engineer"
	@exit 1
endif
	@DATE=$$(date +%Y-%m-%d); \
	SLUG=$$(echo "$(COMPANY)-$(ROLE)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-'); \
	DIR="applications/$$DATE-$$SLUG"; \
	mkdir -p "$$DIR"; \
	echo "---\ncompany: $(COMPANY)\nrole: $(ROLE)\ndate: $$DATE\n---\n\n# Job Description\n\nPaste the job description here." > "$$DIR/job_desc.md"; \
	echo "✅ Created $$DIR/job_desc.md"
