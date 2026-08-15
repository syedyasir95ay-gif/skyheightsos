# Sky Heights AI Agent — Online Starter

Cloud-ready Streamlit app for recruitment, sales leads, performance/MIS, HR, and management AI queries.

## Deploy

Recommended: deploy this folder as a Streamlit app on a cloud host. Add `OPENAI_API_KEY` as a secret/environment variable.

## Local fallback

`pip install -r requirements.txt`
`streamlit run app.py`

## Production next steps

- Move SQLite to managed Postgres/Supabase.
- Add authenticated staff/admin roles.
- Connect WhatsApp Business API through an approved provider.
- Connect Google Sheets/CRM.
- Add audit logs and consent controls.
- Do not put bank/card credentials or sensitive customer financial data into the AI prompt.
