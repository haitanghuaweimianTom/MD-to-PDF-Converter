#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter with LaTeX Math Support
Supports: $...$ (inline math) and $$...$$ (block math)
Requires: pandoc, miktex (xelatex)
"""

import argparse
import subprocess
import logging
import os
import tempfile
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('md2pdf.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    # Check pandoc
    try:
        result = subprocess.run(
            ['pandoc', '--version'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        logger.info(f"✓ Pandoc found: {result.stdout.splitlines()[0]}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("✗ Pandoc not found. Please install pandoc first.")
        return False
    except UnicodeDecodeError:
        logger.warning("⚠ Pandoc version check: Unicode decode error, but pandoc is available")
    
    # Check xelatex (miktex)
    try:
        result = subprocess.run(
            ['xelatex', '--version'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        # Try to get version info, but don't fail if it's not available
        try:
            version_line = result.stdout.splitlines()[0].strip()
            logger.info(f"✓ XeLaTeX found: {version_line}")
        except (IndexError, AttributeError):
            logger.info("✓ XeLaTeX found: Version information not available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("✗ XeLaTeX not found. Please install MikTeX first.")
        return False
    except UnicodeDecodeError:
        logger.warning("⚠ XeLaTeX version check: Unicode decode error, but xelatex is available")
    
    return True

def build_pandoc_command(input_file, output_file, debug=False):
    """Build the pandoc command with appropriate options"""
    # Use absolute paths for input and output to avoid issues
    input_abs = os.path.abspath(input_file)
    output_abs = os.path.abspath(output_file)
    
    # Use basic options that work reliably
    cmd = [
        'pandoc',
        input_abs,
        '-o', output_abs,
        '--syntax-highlighting=tango',  # Replace deprecated --highlight-style
        '-V', 'geometry:margin=1in',
        '-V', 'documentclass=article',
        '-V', 'fontsize=12pt',
        '-V', 'papersize=a4',
    ]
    
    # Debug mode: increase verbosity
    if debug:
        cmd.append('-v')
    
    return cmd

def convert_md_to_pdf(input_file, output_file, debug=False):
    """Convert Markdown file to PDF"""
    logger.info(f"Converting {input_file} to {output_file}...")
    
    # Check input file exists
    if not os.path.exists(input_file):
        logger.error(f"✗ Input file not found: {input_file}")
        return False
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")
    
    # Use absolute paths for input and output to avoid issues
    input_abs = os.path.abspath(input_file)
    output_abs = os.path.abspath(output_file)
    
    # Basic pandoc command with pdflatex for better reliability
    basic_cmd = [
        'pandoc',
        input_abs,
        '-o', output_abs,
        '--pdf-engine=pdflatex',  # Use pdflatex for better reliability
        '--from=markdown+raw_html+tex_math_dollars',  # Support math and raw html
        '--syntax-highlighting=default',  # Use default highlighting which requires fewer packages
        '-V', 'geometry:margin=1in',
        '-V', 'documentclass=article',
        '-V', 'fontsize=12pt'
    ]
    
    logger.debug(f"Using basic command: {' '.join(basic_cmd)}")
    
    # Try PDF conversion first
    pdf_success = False
    try:
        # Execute basic pandoc command
        result = subprocess.run(
            basic_cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        if result.stdout:
            logger.debug(f"Pandoc stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"Pandoc stderr: {result.stderr}")
        
        logger.info(f"✓ PDF conversion successful! Output: {output_file}")
        pdf_success = True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ PDF conversion failed with exit code {e.returncode}")
        logger.error(f"Command: {' '.join(basic_cmd)}")
        if e.stdout:
            logger.error(f"Stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
    except Exception as e:
        logger.error(f"✗ Unexpected error during PDF conversion: {str(e)}")
    
    # Always convert to HTML as fallback
    logger.info("Generating HTML fallback...")
    
    # Convert to HTML first
    html_output = output_abs.replace('.pdf', '.html')
    html_cmd = [
        'pandoc',
        input_abs,
        '-o', html_output,
        '--mathjax',
        '-s',  # Standalone HTML with header and footer
        '--syntax-highlighting=default'
    ]
    
    try:
        # Convert to HTML
        subprocess.run(
            html_cmd,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        logger.info(f"✓ HTML conversion successful: {html_output}")
        
        if not pdf_success:
            logger.warning("✗ PDF conversion failed. Please use the generated HTML file.")
        
        return True
        
    except subprocess.CalledProcessError as e2:
        logger.error(f"✗ HTML conversion also failed: {e2.returncode}")
        return False
    except Exception as e:
        logger.error(f"✗ Unexpected error during HTML conversion: {str(e)}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Markdown to PDF Converter with LaTeX Math Support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.md -o output.pdf
  %(prog)s input.md  # Output will be input.pdf
  %(prog)s input.md --debug  # Enable debug logging
  %(prog)s --check-deps  # Only check dependencies
        """
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        nargs='?',
        help='Input Markdown file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output PDF file path (default: input filename with .pdf extension)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Only check dependencies and exit'
    )
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # If only checking dependencies, exit
    if args.check_deps:
        logger.info("All dependencies are installed correctly.")
        sys.exit(0)
    
    # If no input file provided and not checking dependencies, show help
    if args.input_file is None:
        parser.print_help()
        sys.exit(1)
    
    # Determine output file path
    input_path = Path(args.input_file)
    if args.output:
        output_file = args.output
    else:
        output_file = str(input_path.with_suffix('.pdf'))
    
    # Convert the file
    success = convert_md_to_pdf(args.input_file, output_file, args.debug)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
