#!/usr/bin/env python3
"""
Setup script for the chat API backend using uv
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    """Setup the development environment"""
    print("🚀 Setting up Chat API Backend with uv")
    print("=" * 50)
    
    # Check if uv is installed
    if not run_command("uv --version", "Checking uv installation"):
        print("❌ uv is not installed. Please install it first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("📝 Creating .env file from template...")
        if os.path.exists("env.example"):
            run_command("cp env.example .env", "Copying environment template")
            print("✅ Please edit .env file with your database credentials")
        else:
            print("⚠️  No env.example found. Please create .env manually")
    
    # Setup database (optional)
    setup_db = input("\n🗄️  Do you want to setup the database tables now? (y/N): ").lower()
    if setup_db in ['y', 'yes']:
        if run_command("uv run python setup_db.py", "Setting up database tables"):
            print("✅ Database tables created successfully!")
        else:
            print("❌ Failed to setup database. Please check your database connection.")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your database credentials")
    print("2. Run: uv run python scripts/dev.py")
    print("3. Visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
