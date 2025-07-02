#!/usr/bin/env python3
"""
Test script for iBaza Tech Resale Market Bot
This script tests the core functionality without running the actual bot
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("✅ config.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import config.py: {e}")
        return False
    
    try:
        import keyboards
        print("✅ keyboards.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import keyboards.py: {e}")
        return False
    
    try:
        import utils
        print("✅ utils.py imported successfully")
    except Exception as e:
        print(f"❌ Failed to import utils.py: {e}")
        return False
    
    try:
        from handlers import user, admin, installment
        print("✅ All handlers imported successfully")
    except Exception as e:
        print(f"❌ Failed to import handlers: {e}")
        return False
    
    return True

def test_utils():
    """Test utility functions"""
    print("\nTesting utility functions...")
    
    try:
        import utils
        
        # Test distance calculation
        distance = utils.calculate_distance(41.2995, 69.2401, 39.6270, 66.9749)
        print(f"✅ Distance calculation: {distance:.2f} km")
        
        # Test data loading
        locations = utils.get_locations()
        print(f"✅ Loaded {len(locations)} locations")
        
        models = utils.get_models()
        print(f"✅ Loaded {len(models)} models")
        
        # Test price formatting
        formatted_price = utils.format_price(15000000)
        print(f"✅ Price formatting: {formatted_price}")
        
        return True
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False

def test_installment_calculation():
    """Test installment calculation"""
    print("\nTesting installment calculation...")
    
    try:
        from handlers.installment import calculate_installments_with_interest
        
        # Test calculation
        installments = calculate_installments_with_interest(1000, 400)
        print(f"✅ Installment calculation: {len(installments)} payment plans")
        
        for months, payment in installments.items():
            print(f"   {months}: ${payment}")
        
        return True
    except Exception as e:
        print(f"❌ Installment test failed: {e}")
        return False

def test_keyboards():
    """Test keyboard generation"""
    print("\nTesting keyboard generation...")
    
    try:
        import keyboards
        
        # Test main menu keyboard
        main_kb = keyboards.get_main_menu_keyboard(is_admin=False)
        print("✅ Main menu keyboard (user) generated")
        
        main_kb_admin = keyboards.get_main_menu_keyboard(is_admin=True)
        print("✅ Main menu keyboard (admin) generated")
        
        # Test map keyboard
        map_kb = keyboards.get_map_keyboard()
        print("✅ Map keyboard generated")
        
        # Test models keyboard
        models = [{"id": "1", "name": "iPhone 14 Pro"}]
        models_kb = keyboards.get_models_keyboard(models)
        print("✅ Models keyboard generated")
        
        return True
    except Exception as e:
        print(f"❌ Keyboard test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing iBaza Tech Resale Market Bot\n")
    
    tests = [
        test_imports,
        test_utils,
        test_installment_calculation,
        test_keyboards
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 