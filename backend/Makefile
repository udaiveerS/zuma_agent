# Zuma Agent Makefile
# Quick commands for development and testing

.PHONY: test unit-test integration-test install run clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make test           - Run all tests (unit + integration)"
	@echo "  make unit-test      - Run unit tests only"
	@echo "  make integration-test - Run integration tests only"
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Start the development server"
	@echo "  make clean          - Clean cache files"
	@echo "  make help           - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync

# Run all tests (unit + integration with auto server management)
test: unit-test test-auto
	@echo "✅ All tests completed!"

# Run unit tests
unit-test:
	@echo "🧪 Running unit tests..."
	uv run python tests/test_unit_simple.py

# Run integration tests (requires server to be running)
integration-test:
	@echo "🔗 Running integration tests..."
	@echo "⚠️  Make sure the server is running: make run"
	uv run python tests/integration_tests.py

# Start development server
run:
	@echo "🚀 Starting development server..."
	uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Start server in background for testing
run-bg:
	@echo "🚀 Starting server in background for testing..."
	uv run uvicorn app:app --host 0.0.0.0 --port 8000 &
	@echo "Server PID: $$!"
	@sleep 3  # Give server time to start

# Stop background server
stop-bg:
	@echo "🛑 Stopping background server..."
	pkill -f "uvicorn app:app"

# Run tests with background server (full automated testing)
test-auto: run-bg
	@echo "🤖 Running automated test suite..."
	@sleep 3  # Ensure server is ready
	uv run python tests/integration_tests.py
	$(MAKE) stop-bg

# Clean cache files
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

# Development workflow - install, test, run
dev: install test run

# Quick test (unit tests only - no server required)
quick-test: unit-test
	@echo "⚡ Quick tests completed!"
