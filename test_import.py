#!/usr/bin/env python3
"""
Simple test script to verify all modules can be imported
"""

import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...\n")

    errors = []

    # Test data_fetcher
    try:
        from data_fetcher import DataFetcher
        print("✅ data_fetcher.py - OK")
    except Exception as e:
        print(f"❌ data_fetcher.py - FAILED: {e}")
        errors.append(("data_fetcher", e))

    # Test indicators
    try:
        from indicators import TechnicalIndicators
        print("✅ indicators.py - OK")
    except Exception as e:
        print(f"❌ indicators.py - FAILED: {e}")
        errors.append(("indicators", e))

    # Test position_calculator
    try:
        from position_calculator import PositionCalculator
        print("✅ position_calculator.py - OK")
    except Exception as e:
        print(f"❌ position_calculator.py - FAILED: {e}")
        errors.append(("position_calculator", e))

    # Test alerts
    try:
        from alerts import AlertSystem
        print("✅ alerts.py - OK")
    except Exception as e:
        print(f"❌ alerts.py - FAILED: {e}")
        errors.append(("alerts", e))

    # Test config
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ config.json - OK")
    except Exception as e:
        print(f"❌ config.json - FAILED: {e}")
        errors.append(("config.json", e))

    print("\n" + "="*60)
    if errors:
        print(f"❌ {len(errors)} module(s) failed to import")
        for module, error in errors:
            print(f"   - {module}: {error}")
        return False
    else:
        print("✅ All modules imported successfully!")
        return True

if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
