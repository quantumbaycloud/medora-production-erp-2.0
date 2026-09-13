import os  # <-- Add this missing import at the top
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the absolute path to the directory containing this config file
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial System API"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./financial.db"
    API_SECRET_KEY: str = "change-this-secret-key-in-production"

    # Razorpay
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    # Paytm
    PAYTM_MERCHANT_ID: str = ""
    PAYTM_MERCHANT_KEY: str = ""

    # CCAvenue
    CCAVENUE_MERCHANT_ID: str = ""
    CCAVENUE_WORKING_KEY: str = ""
    CCAVENUE_ACCESS_CODE: str = ""

    # Pine Labs
    PINELABS_MERCHANT_ID: str = ""
    PINELABS_SECRET: str = ""

    # BillDesk
    BILLDESK_MERCHANT_ID: str = ""
    BILLDESK_CLIENT_ID: str = ""
    BILLDESK_SECRET_KEY: str = ""

    # This tells Pydantic to search the current folder, then parent folders for a .env file
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"), 
        extra="ignore"
    )

settings = Settings()

