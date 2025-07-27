import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

def render_contract(data: Dict[str, Any]) -> str:
    """
    Renders a contract using Jinja2 template and provided data.
    Returns HTML string.
    
    Args:
        data (dict): Dictionary containing contract data including:
            - contract_type: str
            - party_a: dict with name, address, email, phone
            - party_b: dict with name, address, email, phone  
            - terms: str
            - start_date: str
            - end_date: str
            - additional_clauses: list (optional)
    
    Returns:
        str: Rendered HTML contract string
    
    Raises:
        FileNotFoundError: If template file is not found
        Exception: If template rendering fails
    """
    try:
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to quick_contract directory, then to templates
        templates_dir = os.path.join(os.path.dirname(current_dir), 'templates')
        
        # Create Jinja2 environment with FileSystemLoader
        env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True  # Enable auto-escaping for security
        )
        
        # Load the contract template
        template = env.get_template('contract_template.html')
        
        # Add generation timestamp to data
        enhanced_data = data.copy()
        enhanced_data['generation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Render the template with provided data
        rendered_html = template.render(**enhanced_data)
        
        return rendered_html
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Template file not found: {e}")
    except Exception as e:
        raise Exception(f"Error rendering contract template: {e}")


def validate_contract_data(data: Dict[str, Any]) -> bool:
    """
    Validates that the required contract data fields are present.
    
    Args:
        data (dict): Contract data to validate
        
    Returns:
        bool: True if all required fields are present
        
    Raises:
        ValueError: If required fields are missing
    """
    required_fields = [
        'contract_type', 
        'party_a', 
        'party_b', 
        'terms', 
        'start_date', 
        'end_date'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    # Check party data structure
    for party_key in ['party_a', 'party_b']:
        if party_key in data and isinstance(data[party_key], dict):
            if 'name' not in data[party_key] or not data[party_key]['name']:
                missing_fields.append(f'{party_key}.name')
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return True


def get_sample_contract_data() -> Dict[str, Any]:
    """
    Returns sample contract data for testing purposes.
    
    Returns:
        dict: Sample contract data
    """
    return {
        "contract_type": "Service Agreement",
        "party_a": {
            "name": "ABC Company Inc.",
            "address": "123 Business St, City, State 12345",
            "email": "contact@abccompany.com",
            "phone": "+1 (555) 123-4567"
        },
        "party_b": {
            "name": "John Doe",
            "address": "456 Client Ave, Town, State 67890",
            "email": "john.doe@email.com", 
            "phone": "+1 (555) 987-6543"
        },
        "terms": "This agreement establishes the terms for providing consulting services. The service provider agrees to deliver high-quality consulting services according to the specifications outlined in this contract.",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "additional_clauses": [
            "All work must be completed within the agreed timeframe.",
            "Payment terms are Net 30 days from invoice date.",
            "This contract may be terminated by either party with 30 days written notice."
        ]
    } 