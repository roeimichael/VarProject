"""
Verify VarProject setup and configuration.
Run this script after installation to ensure everything is configured correctly.
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your credentials")
        return False
    print("✅ .env file exists")
    return True

def check_env_variables():
    """Check if required environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()

    required_vars = ['TELEGRAM_BOT_TOKEN']
    optional_vars = ['NET_LIQUIDITY', 'INITIAL_INVESTMENT']

    all_good = True
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is NOT set (required)")
            all_good = False

    for var in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is using default value")

    return all_good

def check_data_directory():
    """Check if data directory exists."""
    data_dir = Path('data')
    if not data_dir.exists():
        print("❌ data/ directory not found")
        print("   Creating it now...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print("✅ data/ directory created")
        return True
    print("✅ data/ directory exists")
    return True

def check_dependencies():
    """Check if key dependencies are installed."""
    dependencies = [
        'pandas',
        'numpy',
        'yfinance',
        'telebot',
        'ib_insync',
        'dotenv'
    ]

    all_installed = True
    for dep in dependencies:
        try:
            __import__(dep if dep != 'dotenv' else 'dotenv')
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is NOT installed")
            all_installed = False

    if not all_installed:
        print("\n   Run: pip install -r requirements.txt")

    return all_installed

def main():
    """Run all verification checks."""
    print("VarProject Setup Verification")
    print("=" * 50)

    checks = [
        ("Environment file", check_env_file),
        ("Data directory", check_data_directory),
        ("Dependencies", check_dependencies),
        ("Environment variables", check_env_variables),
    ]

    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())

    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Place your portfolio CSV in data/actualportfolio.csv")
        print("2. Run: python main.py")
        print("3. Start Telegram bot: python TelegramBot.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
