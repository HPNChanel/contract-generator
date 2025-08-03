"""
Email utility for sending contract PDFs via SMTP
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration - these should be set as environment variables in production
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)
SENDER_NAME = os.getenv("SENDER_NAME", "Quick Contract Generator")

def send_contract_email(
    recipient_email: str,
    pdf_path: str,
    contract_type: str,
    contract_id: int,
    sender_email: Optional[str] = None,
    sender_name: Optional[str] = None,
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    smtp_username: Optional[str] = None,
    smtp_password: Optional[str] = None
) -> bool:
    """
    Send contract PDF via email using SMTP.
    
    Args:
        recipient_email: Email address to send the contract to
        pdf_path: Full path to the PDF file
        contract_type: Type of contract for the email subject
        contract_id: Contract ID for reference
        sender_email: Override sender email (uses SENDER_EMAIL env var by default)
        sender_name: Override sender name (uses SENDER_NAME env var by default)
        smtp_server: Override SMTP server (uses SMTP_SERVER env var by default)
        smtp_port: Override SMTP port (uses SMTP_PORT env var by default)
        smtp_username: Override SMTP username (uses SMTP_USERNAME env var by default)
        smtp_password: Override SMTP password (uses SMTP_PASSWORD env var by default)
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    
    Raises:
        Exception: If email configuration is missing or email sending fails
    """
    
    # Use provided values or fall back to environment variables
    smtp_server = smtp_server or SMTP_SERVER
    smtp_port = smtp_port or SMTP_PORT
    smtp_username = smtp_username or SMTP_USERNAME
    smtp_password = smtp_password or SMTP_PASSWORD
    sender_email = sender_email or SENDER_EMAIL
    sender_name = sender_name or SENDER_NAME
    
    # Validate email configuration
    if not all([smtp_server, smtp_username, smtp_password, sender_email]):
        missing_vars = []
        if not smtp_server: missing_vars.append("SMTP_SERVER")
        if not smtp_username: missing_vars.append("SMTP_USERNAME") 
        if not smtp_password: missing_vars.append("SMTP_PASSWORD")
        if not sender_email: missing_vars.append("SENDER_EMAIL")
        
        error_msg = f"Email configuration missing. Please set environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    # Check if PDF file exists
    if not os.path.exists(pdf_path):
        error_msg = f"PDF file not found: {pdf_path}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Your {contract_type} Contract (ID: {contract_id})"
        
        # Create email body
        body = f"""
Dear Customer,

Thank you for using Quick Contract Generator. Please find your {contract_type} contract attached to this email.

Contract Details:
- Contract ID: {contract_id}
- Contract Type: {contract_type}
- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

If you have any questions about this contract, please contact us.

Best regards,
Quick Contract Generator Team
        """.strip()
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
            pdf_filename = os.path.basename(pdf_path)
            pdf_attachment.add_header('Content-Disposition', f'attachment; filename="{pdf_filename}"')
            msg.attach(pdf_attachment)
        
        # Connect to server and send email
        logger.info(f"Connecting to SMTP server {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(smtp_username, smtp_password)
        
        logger.info(f"Sending contract email to {recipient_email}")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        logger.info(f"Contract email sent successfully to {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP authentication failed. Check username/password: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except smtplib.SMTPRecipientsRefused as e:
        error_msg = f"Invalid recipient email address: {recipient_email}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error occurred: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)


def test_email_configuration() -> bool:
    """
    Test email configuration without sending an actual email.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL]):
            return False
            
        # Test SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.quit()
        
        return True
    except Exception as e:
        logger.error(f"Email configuration test failed: {e}")
        return False


def get_email_config_status() -> dict:
    """
    Get the current email configuration status.
    
    Returns:
        dict: Configuration status information
    """
    return {
        "smtp_server_configured": bool(SMTP_SERVER),
        "smtp_username_configured": bool(SMTP_USERNAME),
        "smtp_password_configured": bool(SMTP_PASSWORD),
        "sender_email_configured": bool(SENDER_EMAIL),
        "smtp_server": SMTP_SERVER if SMTP_SERVER else "Not configured",
        "smtp_port": SMTP_PORT,
        "sender_email": SENDER_EMAIL if SENDER_EMAIL else "Not configured",
        "configuration_complete": all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL])
    }


if __name__ == "__main__":
    # Test email configuration when running this module directly
    print("Testing email configuration...")
    config_status = get_email_config_status()
    print("Email Configuration Status:")
    for key, value in config_status.items():
        print(f"  {key}: {value}")
    
    if config_status["configuration_complete"]:
        if test_email_configuration():
            print("✅ Email configuration is working!")
        else:
            print("❌ Email configuration test failed.")
    else:
        print("❌ Email configuration is incomplete.")