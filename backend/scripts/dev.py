#!/usr/bin/env python3
"""
Development server script using uv
"""
import subprocess
import sys

def main():
    """Run the development server with uv"""
    try:
        subprocess.run([
            "uv", "run", "uvicorn", "app:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
