#!/usr/bin/env python3
"""
Quick Test Runner for Zuma Agent

Alternative to Makefile for systems without 'make' command.
Runs the required unit tests as specified in the assignment.

Usage:
    python run_tests.py              # Run unit tests only
    python run_tests.py --all        # Run unit + integration tests
    python run_tests.py --integration # Run integration tests only
"""

import subprocess
import sys
import argparse
import time
import requests
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def check_server_running():
    """Check if the development server is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def run_unit_tests():
    """Run the 4 required unit tests"""
    print("\n" + "="*50)
    print("🧪 RUNNING UNIT TESTS")
    print("="*50)
    print("Testing the 4 required scenarios:")
    print("1. ✅ Availability success")
    print("2. ❌ No availability scenario") 
    print("3. 💰 Pricing lookup")
    print("4. 🐱 Pet policy lookup")
    print()
    
    # Install pytest if not available
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest"], 
                  capture_output=True, check=False)
    
    # Run unit tests - try pytest first, fallback to direct execution
    if subprocess.run([sys.executable, "-c", "import pytest"], capture_output=True).returncode == 0:
        success = run_command(
            f"{sys.executable} -m pytest tests/test_unit_simple.py -v --tb=short",
            "Unit Tests (4 required scenarios)"
        )
    else:
        # Fallback to direct execution
        success = run_command(
            f"{sys.executable} tests/test_unit_simple.py",
            "Unit Tests (4 required scenarios)"
        )
    
    return success

def run_integration_tests():
    """Run integration tests"""
    print("\n" + "="*50)
    print("🔗 RUNNING INTEGRATION TESTS")
    print("="*50)
    
    if not check_server_running():
        print("⚠️  Server not running at http://localhost:8000")
        print("Please start the server first:")
        print("   cd backend && uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return False
    
    success = run_command(
        f"{sys.executable} tests/integration_tests.py",
        "Integration Tests (Full Agent Flow)"
    )
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Zuma Agent Test Runner")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only (default)")
    
    args = parser.parse_args()
    
    print("🚀 Zuma Agent Test Runner")
    print("="*50)
    
    # Change to backend directory if not already there
    if not os.path.exists("tests/test_tools.py"):
        if os.path.exists("backend/tests/test_tools.py"):
            os.chdir("backend")
        else:
            print("❌ Error: Could not find tests directory")
            print("Please run this script from the project root or backend directory")
            sys.exit(1)
    
    success = True
    
    if args.integration:
        # Integration tests only
        success = run_integration_tests()
    elif args.all:
        # Both unit and integration tests
        success = run_unit_tests()
        if success:
            success = run_integration_tests()
    else:
        # Default: unit tests only (meets assignment requirements)
        success = run_unit_tests()
    
    print("\n" + "="*50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The agent is working correctly")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("Check the output above for details")
        sys.exit(1)

if __name__ == "__main__":
    main()
