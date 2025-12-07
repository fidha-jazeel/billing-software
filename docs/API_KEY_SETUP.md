# AI Features - API Key Setup Guide

## Overview
The AI Features in the Travel Billing Software use Google's Gemini AI to provide intelligent insights about your billing data. To use these features, you need to configure a Google AI API key.

## Getting Your API Key

1. **Visit Google AI Studio**
   - Go to: https://aistudio.google.com/app/apikey
   - Sign in with your Google account

2. **Create an API Key**
   - Click "Create API Key"
   - Select your project or create a new one
   - Copy the generated API key

3. **Free Tier Information**
   - Google AI Studio offers a generous free tier
   - No credit card required for basic usage
   - Suitable for small to medium-sized travel agencies

## Configuring the API Key in Software

### Method 1: Settings Page (Recommended)
1. Open the software
2. Navigate to **Settings** from the sidebar
3. Find the **🤖 AI Configuration** section
4. Paste your API key in the "Google AI API Key" field
5. Click the **🧪 Test** button to verify it works
6. Click **💾 Save All Settings**

### Method 2: Manual Configuration
If you need to configure the key manually:
1. Navigate to `travel_billing_software/config/`
2. Create a file named `.api_keys.json` (note the dot at the beginning)
3. Add the following content:
```json
{
    "google_ai": "YOUR_API_KEY_HERE"
}
```
4. Save the file
5. Restart the application

## Security Features

### How API Keys are Stored
- API keys are stored in a separate configuration file (`.api_keys.json`)
- Keys are encoded using base64 for basic obfuscation
- The file is automatically excluded from version control (.gitignore)
- Keys persist between software sessions

### Security Best Practices
1. **Never share your API key** with others
2. **Don't commit** the `.api_keys.json` file to version control
3. **Rotate keys regularly** if you suspect unauthorized access
4. **Use API quotas** in Google Cloud Console to limit usage
5. **Delete old keys** from Google AI Studio when no longer needed

## Using AI Features

Once configured, you can:

### Quick Insights
- **This Month Overview**: Get a summary of current month's business
- **This vs Last Month**: Compare performance between months
- **Top Customers**: See your most valuable customers
- **Pending Payments**: Track outstanding invoices

### Custom Questions
Ask natural language questions like:
- "How much revenue did we generate this week?"
- "Who are my top 5 customers by total billing?"
- "How many pending invoices do we have?"
- "Show me all international flights this month"

## Troubleshooting

### "AI features are disabled" Message
**Solution**: Configure your API key in Settings → AI Configuration

### "API key test failed"
**Possible causes**:
1. Invalid API key - verify it's copied correctly
2. No internet connection - check your network
3. API quota exceeded - check Google Cloud Console
4. Key permissions issue - regenerate the key

### API Key Not Persisting
**Solution**: 
1. Check file permissions on the `config` folder
2. Ensure the software has write access
3. Verify `.api_keys.json` is being created in `travel_billing_software/config/`

### AI Gives Unexpected Results
**Tips**:
1. Be specific in your questions
2. Use proper date formats
3. Refer to database table names if known
4. Break complex questions into simpler parts

## API Usage and Costs

### Free Tier Limits
- Google AI Studio provides generous free usage
- Sufficient for most small business needs
- Monitor usage in Google Cloud Console

### If You Exceed Free Tier
1. Check Google Cloud Console for usage details
2. Consider upgrading to a paid plan
3. Optimize queries to reduce API calls
4. Use preset questions instead of custom queries

## Privacy and Data

### What Data is Sent to Google AI
- Your billing database schema (table and column names)
- SQL query results based on your questions
- No raw database is uploaded - only query results

### What's NOT Sent
- Your entire database
- Customer personal information (unless specifically queried)
- Your API key (stays local)

## Support

For issues or questions:
1. Check this documentation first
2. Verify API key is correctly configured
3. Test with simple questions first
4. Check application logs in the `logs/` folder
5. Contact software support with error details

## Advanced Configuration

### Using Environment Variables (Alternative)
Instead of the Settings page, you can also set:
```bash
GOOGLE_API_KEY=your_key_here
```
in a `.env` file in the `travel_billing_software` folder.

**Note**: Settings page configuration takes precedence over environment variables.

### Multiple API Keys
The system supports storing multiple API keys for different services:
- `google_ai` - Google Gemini AI
- Future integrations can be added

---

**Last Updated**: December 2025
**Version**: 1.0
