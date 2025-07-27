import os
from datetime import datetime
from typing import Optional

# Try to import WeasyPrint, fall back to reportlab if it fails
WEASYPRINT_AVAILABLE = True
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint not available: {e}")
    print("Falling back to reportlab for PDF generation...")

# Import reportlab as fallback
try:
    from .pdf_generator_reportlab import (
        generate_pdf_from_html_reportlab,
        generate_pdf_from_template_data_reportlab
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_from_html(html: str, output_filename: Optional[str] = None) -> str:
    """
    Converts the given HTML string to a PDF file using WeasyPrint or reportlab fallback.
    Saves the file in 'generated_pdfs/' directory and returns the file path.
    
    Args:
        html (str): The HTML string to convert to PDF
        output_filename (str, optional): Custom filename for the PDF. 
                                       If None, generates a unique name using timestamp.
    
    Returns:
        str: The full path to the generated PDF file
        
    Raises:
        Exception: If PDF generation fails
    """
    # Try WeasyPrint first if available
    if WEASYPRINT_AVAILABLE:
        try:
            return _generate_pdf_weasyprint(html, output_filename)
        except Exception as e:
            print(f"WeasyPrint failed: {e}")
            if REPORTLAB_AVAILABLE:
                print("Falling back to reportlab...")
                return generate_pdf_from_html_reportlab(html, output_filename)
            else:
                raise Exception(f"WeasyPrint failed and reportlab not available: {e}")
    
    # Use reportlab as fallback
    elif REPORTLAB_AVAILABLE:
        return generate_pdf_from_html_reportlab(html, output_filename)
    
    else:
        raise Exception("Neither WeasyPrint nor reportlab is available for PDF generation")


def _generate_pdf_weasyprint(html: str, output_filename: Optional[str] = None) -> str:
    """
    Internal function to generate PDF using WeasyPrint.
    """
    try:
        # Create the generated_pdfs directory if it doesn't exist
        pdf_dir = "generated_pdfs"
        os.makedirs(pdf_dir, exist_ok=True)
        
        # Generate filename if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"contract_{timestamp}.pdf"
        
        # Ensure the filename ends with .pdf
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        # Full path for the output file
        output_path = os.path.join(pdf_dir, output_filename)
        
        # Create font configuration for better rendering
        font_config = FontConfiguration()
        
        # Additional CSS for better PDF formatting
        pdf_css = CSS(string="""
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: 'DejaVu Sans', Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #333;
            }
            .header {
                page-break-after: avoid;
            }
            .signature-section {
                page-break-inside: avoid;
                margin-top: 2cm;
            }
            .terms {
                page-break-inside: avoid;
            }
        """, font_config=font_config)
        
        # Convert HTML to PDF
        html_doc = HTML(string=html)
        html_doc.write_pdf(
            output_path, 
            stylesheets=[pdf_css],
            font_config=font_config
        )
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error generating PDF: {e}")


def generate_pdf_from_template_data(template_data: dict, output_filename: Optional[str] = None) -> str:
    """
    Generates a PDF contract from template data by first rendering HTML then converting to PDF.
    Uses WeasyPrint if available, falls back to reportlab.
    
    Args:
        template_data (dict): Contract data for template rendering
        output_filename (str, optional): Custom filename for the PDF
        
    Returns:
        str: The full path to the generated PDF file
        
    Raises:
        Exception: If PDF generation or template rendering fails
    """
    # Try WeasyPrint first if available
    if WEASYPRINT_AVAILABLE:
        try:
            # Import here to avoid circular imports
            from .template_renderer import render_contract, validate_contract_data
            
            # Validate the template data
            validate_contract_data(template_data)
            
            # Render HTML from template
            html_content = render_contract(template_data)
            
            # Generate PDF from HTML using WeasyPrint
            pdf_path = _generate_pdf_weasyprint(html_content, output_filename)
            
            return pdf_path
        except Exception as e:
            print(f"WeasyPrint template generation failed: {e}")
            if REPORTLAB_AVAILABLE:
                print("Falling back to reportlab...")
                return generate_pdf_from_template_data_reportlab(template_data, output_filename)
            else:
                raise Exception(f"WeasyPrint failed and reportlab not available: {e}")
    
    # Use reportlab as fallback
    elif REPORTLAB_AVAILABLE:
        return generate_pdf_from_template_data_reportlab(template_data, output_filename)
    
    else:
        raise Exception("Neither WeasyPrint nor reportlab is available for PDF generation")


def get_generated_pdfs_list() -> list:
    """
    Returns a list of all generated PDF files in the generated_pdfs directory.
    
    Returns:
        list: List of dictionaries containing file information
    """
    try:
        pdf_dir = "generated_pdfs"
        if not os.path.exists(pdf_dir):
            return []
        
        pdf_files = []
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                file_stat = os.stat(file_path)
                
                pdf_files.append({
                    "filename": filename,
                    "file_path": file_path,
                    "size_bytes": file_stat.st_size,
                    "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        
        # Sort by creation time (newest first)
        pdf_files.sort(key=lambda x: x["created_at"], reverse=True)
        
        return pdf_files
        
    except Exception as e:
        raise Exception(f"Error listing PDF files: {e}")


def delete_pdf_file(filename: str) -> bool:
    """
    Deletes a specific PDF file from the generated_pdfs directory.
    
    Args:
        filename (str): Name of the PDF file to delete
        
    Returns:
        bool: True if file was deleted successfully, False otherwise
        
    Raises:
        Exception: If deletion fails
    """
    try:
        pdf_dir = "generated_pdfs"
        file_path = os.path.join(pdf_dir, filename)
        
        if not os.path.exists(file_path):
            return False
        
        if not filename.lower().endswith('.pdf'):
            return False
        
        os.remove(file_path)
        return True
        
    except Exception as e:
        raise Exception(f"Error deleting PDF file: {e}")


def cleanup_old_pdfs(days_old: int = 30) -> int:
    """
    Deletes PDF files older than the specified number of days.
    
    Args:
        days_old (int): Number of days after which PDFs should be deleted (default: 30)
        
    Returns:
        int: Number of files deleted
        
    Raises:
        Exception: If cleanup fails
    """
    try:
        pdf_dir = "generated_pdfs"
        if not os.path.exists(pdf_dir):
            return 0
        
        current_time = datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                file_stat = os.stat(file_path)
                file_age = current_time - datetime.fromtimestamp(file_stat.st_ctime)
                
                if file_age.days > days_old:
                    os.remove(file_path)
                    deleted_count += 1
        
        return deleted_count
        
    except Exception as e:
        raise Exception(f"Error during PDF cleanup: {e}") 