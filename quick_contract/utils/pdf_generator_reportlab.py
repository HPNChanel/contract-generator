import os
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import html


def generate_pdf_from_html_reportlab(html_content: str, output_filename: Optional[str] = None) -> str:
    """
    Converts HTML content to PDF using reportlab.
    This is a Windows-friendly alternative to WeasyPrint.
    
    Args:
        html_content (str): The HTML string to convert to PDF
        output_filename (str, optional): Custom filename for the PDF
    
    Returns:
        str: The full path to the generated PDF file
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
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )
        
        # Parse the HTML and create PDF content
        story = _parse_html_to_reportlab(html_content)
        
        # Build the PDF
        doc.build(story)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error generating PDF with reportlab: {e}")


def generate_pdf_from_template_data_reportlab(template_data: dict, output_filename: Optional[str] = None) -> str:
    """
    Generates a PDF contract from template data using reportlab.
    
    Args:
        template_data (dict): Contract data for template rendering
        output_filename (str, optional): Custom filename for the PDF
        
    Returns:
        str: The full path to the generated PDF file
    """
    try:
        # Import here to avoid circular imports
        from .template_renderer import render_contract, validate_contract_data
        
        # Validate the template data
        validate_contract_data(template_data)
        
        # Render HTML from template
        html_content = render_contract(template_data)
        
        # Generate PDF from HTML using reportlab
        pdf_path = generate_pdf_from_html_reportlab(html_content, output_filename)
        
        return pdf_path
        
    except Exception as e:
        raise Exception(f"Error generating PDF from template data with reportlab: {e}")


def _parse_html_to_reportlab(html_content: str) -> list:
    """
    Parse HTML content and convert to reportlab elements.
    This is a simplified HTML parser for contract documents.
    """
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.black
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=colors.black
    )
    
    story = []
    
    # Simple HTML parsing (you might want to use BeautifulSoup for complex HTML)
    lines = html_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract text content from HTML tags
        if '<title>' in line and '</title>' in line:
            title_text = _extract_text_from_html(line)
            if 'CONTRACT' in title_text.upper():
                story.append(Paragraph(title_text, title_style))
                story.append(Spacer(1, 12))
                
        elif '<h1>' in line and '</h1>' in line:
            h1_text = _extract_text_from_html(line)
            story.append(Paragraph(h1_text, title_style))
            story.append(Spacer(1, 12))
            
        elif '<h2>' in line and '</h2>' in line:
            h2_text = _extract_text_from_html(line)
            story.append(Paragraph(h2_text, heading_style))
            story.append(Spacer(1, 6))
            
        elif '<h3>' in line and '</h3>' in line:
            h3_text = _extract_text_from_html(line)
            story.append(Paragraph(h3_text, heading_style))
            story.append(Spacer(1, 6))
            
        elif '<p>' in line and '</p>' in line:
            p_text = _extract_text_from_html(line)
            if p_text:
                story.append(Paragraph(p_text, normal_style))
                story.append(Spacer(1, 6))
    
    # If no content was parsed, create a simple contract structure
    if not story:
        story = _create_simple_contract_structure(html_content, styles)
    
    return story


def _extract_text_from_html(html_line: str) -> str:
    """Extract text content from HTML tags."""
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_line)
    # Decode HTML entities
    text = html.unescape(text)
    return text.strip()


def _create_simple_contract_structure(html_content: str, styles) -> list:
    """Create a simple contract structure when HTML parsing fails."""
    story = []
    
    # Title
    story.append(Paragraph("CONTRACT", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Contract content (simplified)
    content_lines = html_content.replace('<br>', '\n').replace('<br/>', '\n').split('\n')
    
    for line in content_lines[:50]:  # Limit to prevent overly long documents
        clean_line = _extract_text_from_html(line)
        if clean_line and len(clean_line) > 3:
            story.append(Paragraph(clean_line, styles['Normal']))
            story.append(Spacer(1, 6))
    
    # Signature section
    story.append(Spacer(1, 30))
    
    signature_data = [
        ['Party A Signature:', 'Party B Signature:'],
        ['', ''],
        ['_' * 30, '_' * 30],
        ['Date: _______________', 'Date: _______________']
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    story.append(signature_table)
    
    return story


# Utility functions for file management (same as WeasyPrint version)
def get_generated_pdfs_list() -> list:
    """Returns a list of all generated PDF files."""
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
        
        pdf_files.sort(key=lambda x: x["created_at"], reverse=True)
        return pdf_files
        
    except Exception as e:
        raise Exception(f"Error listing PDF files: {e}")


def delete_pdf_file(filename: str) -> bool:
    """Deletes a specific PDF file."""
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
    """Deletes PDF files older than specified days."""
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