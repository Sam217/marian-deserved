#!/usr/bin/env python3
"""
Build Script for CSV Processing Application
-------------------------------------------
This script automates the creation of a standalone executable from Python code.
It handles installing PyInstaller if needed and runs the build process.

Usage:
    python buildExe.py
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Configuration
from buildStrings import APP_IMAGE, MAIN_SCRIPT
from buildStrings import APP_NAME
from buildStrings import APP_VERSION
from buildStrings import APP_ICON
from buildStrings import EXTRA_DATA
from buildStrings import INCLUDE_PACKAGES


def check_pyinstaller():
    """Check if PyInstaller is installed, install if not."""
    print("Checking for PyInstaller...")
    try:
        # Try to run PyInstaller to check if it's installed
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(
                f"✓ PyInstaller version {result.stdout.strip()} is installed.")
            return True
        else:
            raise ImportError("PyInstaller not properly installed")
    except (ImportError, FileNotFoundError, subprocess.SubprocessError):
        print("✗ PyInstaller not found or not working properly. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"])
            print("✓ PyInstaller has been installed successfully.")

            # Verify the installation worked
            verify = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if verify.returncode == 0:
                print(
                    f"✓ Verified PyInstaller version {verify.stdout.strip()}")
                return True
            else:
                print("✗ PyInstaller installation verification failed.")
                return False
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install PyInstaller: {e}")
            print("  Please install it manually: pip install pyinstaller")
            return False


def create_spec_file():
    """Create a spec file for PyInstaller with appropriate options."""
    print("\nCreating spec file...")

    # Base command with all needed options
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--clean",  # Clean PyInstaller cache
        "--add-data", f"{APP_ICON};.",
        "--add-data", f"{APP_IMAGE};."
    ]

    # Add icon if specified
    if APP_ICON and os.path.exists(APP_ICON):
        cmd.extend(["--icon", APP_ICON])

    # Add version info if on Windows
    # if platform.system() == "Windows":
    #     file_version = '.'.join([str(int(x)) for x in APP_VERSION.split('.')])
    #     cmd.extend([
    #         "--version-file",
    #         f"version-file={file_version}"
    #     ])

    # Add hidden imports if specified
    for pkg in INCLUDE_PACKAGES:
        cmd.extend(["--hidden-import", pkg])

    # Add extra data files if specified
    for src, dst in EXTRA_DATA:
        cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])

    # Add the main script
    cmd.append(MAIN_SCRIPT)

    try:
        subprocess.check_call(cmd)
        print(f"✓ Spec file '{APP_NAME}.spec' created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create spec file. Error: {e}")
        return False


def modify_spec_file():
    """Modify the spec file to include additional options."""
    spec_file = f"{APP_NAME}.spec"

    if not os.path.exists(spec_file):
        print("✗ Spec file not found.")
        return False

    print("\nModifying spec file...")

    # Instead of modifying an existing spec file, let's create a new one
    # with all options directly in the PyInstaller command

    # We'll skip modifications for simplicity and reliability
    # This avoids indentation issues that can occur when modifying Python files

    print("✓ Using spec file as-is. Additional options will be passed during build.")
    return True


def build_executable():
    """Build the executable using the spec file."""
    spec_file = f"{APP_NAME}.spec"

    if not os.path.exists(spec_file):
        print("✗ Spec file not found.")
        return False

    print("\nBuilding executable...")
    try:
        # Use the direct build command instead of the spec file to avoid indentation issues
        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",  # Clean PyInstaller cache
            spec_file
        ]

        # Show the command being run for debugging
        print(f"Running command: {' '.join(cmd)}")

        subprocess.check_call(cmd)
        print(f"✓ Executable built successfully! It's located in the 'dist' folder.")

        # Get the executable path
        exe_extension = ".exe" if platform.system() == "Windows" else ""
        exe_path = os.path.join("dist", f"{APP_NAME}{exe_extension}")

        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"  - Executable size: {size_mb:.2f} MB")
            print(f"  - Location: {os.path.abspath(exe_path)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to build executable. Error: {e}")
        return False


def main():
    """Main build process."""
    print("=" * 60)
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)

    # Check for main script
    if not os.path.exists(MAIN_SCRIPT):
        print(f"✗ Main script '{MAIN_SCRIPT}' not found.")
        return False

    # Check and install PyInstaller if needed
    if not check_pyinstaller():
        return False

    # Clean up old build files if they exist
    print("\nCleaning up old build files...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"✓ Removed old {folder} folder.")
            except Exception as e:
                print(f"! Warning: Could not remove {folder} folder: {e}")

    # Remove old spec file if it exists
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
            print(f"✓ Removed old {spec_file} file.")
        except Exception as e:
            print(f"! Warning: Could not remove {spec_file} file: {e}")

    # Create a new spec file
    if not create_spec_file():
        return False

    # Build the executable
    if not build_executable():
        return False

    print("\n" + "=" * 60)
    print(f"{APP_NAME} has been built successfully!")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
