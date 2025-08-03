# Email Configuration Setup

This document explains how to configure email functionality for the Quick Contract Generator.

## Overview

The email feature allows you to:
- Automatically send generated contract PDFs to recipients
- Send contracts via email after creation
- Test email configuration

## Environment Variables

To enable email functionality, set these environment variables:

### Required Variables

```bash
# SMTP Server Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Sender Information
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME="Your Company Name"
```

### Gmail Configuration

For Gmail, you'll need to:

1. Enable 2-factor authentication
2. Generate an "App Password" (not your regular password)
3. Use the app password as `SMTP_PASSWORD`

### Other Email Providers

- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's SMTP settings

## Setting Environment Variables

### Windows (PowerShell)
```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_NAME="Quick Contract Generator"
```

### Windows (Command Prompt)
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set SENDER_EMAIL=your-email@gmail.com
set SENDER_NAME=Quick Contract Generator
```

### Linux/Mac
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_NAME="Quick Contract Generator"
```

### .env File (Recommended)

Create a `.env` file in the `quick_contract` directory:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=your-email@gmail.com
SENDER_NAME=Quick Contract Generator
```

Then install python-dotenv and load the environment variables:

```bash
pip install python-dotenv
```

Add to your `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Testing Email Configuration

### Using the API

1. **Check configuration status:**
   ```
   GET /api/v1/email/config
   ```

2. **Test email connection:**
   ```
   POST /api/v1/email/test
   ```

### Using the Python module directly

```bash
cd quick_contract
python -m utils.email_sender
```

## Using Email Features

### Automatic Email on Contract Creation

Include `recipient_email` in your contract creation request:

```json
{
  "contract_type": "Service Agreement",
  "recipient_email": "client@example.com",
  // ... other contract fields
}
```

### Send Email for Existing Contract

```
POST /api/v1/contracts/{contract_id}/email
{
  "recipient_email": "client@example.com"
}
```

## Troubleshooting

### Common Issues

1. **Authentication Failure**
   - Double-check username/password
   - For Gmail, ensure you're using an App Password
   - Verify 2FA is enabled for Gmail

2. **Connection Timeout**
   - Check SMTP server and port
   - Verify firewall settings
   - Try different ports (465 for SSL, 587 for TLS)

3. **Invalid Recipient**
   - Verify email address format
   - Check for typos in recipient email

### Error Messages

- `"Email configuration missing"`: Set required environment variables
- `"SMTP authentication failed"`: Check username/password
- `"Invalid recipient email address"`: Verify email format
- `"PDF file not found"`: Contract PDF wasn't generated properly

## Security Notes

- Never commit SMTP passwords to version control
- Use App Passwords instead of regular passwords when available
- Consider using environment-specific configurations
- Rotate credentials regularly

## Email Template

The system sends a professional email with:
- Contract type and ID in subject line
- PDF attachment
- Contract details in email body
- Generation timestamp

You can customize the email template by modifying the `send_contract_email` function in `utils/email_sender.py`.