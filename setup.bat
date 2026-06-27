@echo off
echo Setting up Ghost Founder...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo.
echo Setup complete!
echo.
echo NEXT STEP: Edit the .env file and add your API keys
echo Then run: streamlit run app.py
pause
