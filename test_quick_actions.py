"""
Test script for Quick Actions module

This script tests all Quick Action functions to ensure they work correctly
after being separated into their own module.

Run this script to verify the Quick Actions functionality:
python test_quick_actions.py
"""

from quick_actions import (
    reset_password,
    request_admin_permission,
    unblock_account,
    submit_ticket,
    request_wifi_access,
    QUICK_ACTIONS,
    get_quick_action,
    list_available_actions
)

def test_individual_functions():
    """Test each Quick Action function individually"""
    print("🧪 Testing Individual Quick Action Functions")
    print("=" * 50)
    
    functions_to_test = [
        ("Reset Password", reset_password),
        ("Request Admin Permission", request_admin_permission),
        ("Unblock Account", unblock_account),
        ("Submit Ticket", submit_ticket),
        ("Request WiFi Access", request_wifi_access)
    ]
    
    for name, func in functions_to_test:
        try:
            result = func()
            print(f"✅ {name}: SUCCESS")
            print(f"   Preview: {result[:60]}...")
            print()
        except Exception as e:
            print(f"❌ {name}: FAILED - {str(e)}")
            print()

def test_utility_functions():
    """Test utility functions in the module"""
    print("🔧 Testing Utility Functions")
    print("=" * 50)
    
    # Test list_available_actions
    try:
        actions = list_available_actions()
        print(f"✅ list_available_actions(): {len(actions)} actions found")
        print(f"   Actions: {', '.join(actions)}")
        print()
    except Exception as e:
        print(f"❌ list_available_actions(): FAILED - {str(e)}")
        print()
    
    # Test get_quick_action
    try:
        func = get_quick_action('reset_password')
        if func:
            result = func()
            print("✅ get_quick_action('reset_password'): SUCCESS")
            print(f"   Preview: {result[:60]}...")
        else:
            print("❌ get_quick_action('reset_password'): FAILED - Function not found")
        print()
    except Exception as e:
        print(f"❌ get_quick_action('reset_password'): FAILED - {str(e)}")
        print()
    
    # Test invalid action
    try:
        func = get_quick_action('invalid_action')
        if func is None:
            print("✅ get_quick_action('invalid_action'): SUCCESS (correctly returned None)")
        else:
            print("❌ get_quick_action('invalid_action'): FAILED - Should return None")
        print()
    except Exception as e:
        print(f"❌ get_quick_action('invalid_action'): FAILED - {str(e)}")
        print()

def test_quick_actions_registry():
    """Test the QUICK_ACTIONS registry"""
    print("📋 Testing Quick Actions Registry")
    print("=" * 50)
    
    try:
        print(f"Registry contains {len(QUICK_ACTIONS)} actions:")
        for action_name, action_func in QUICK_ACTIONS.items():
            try:
                result = action_func()
                print(f"✅ {action_name}: SUCCESS")
            except Exception as e:
                print(f"❌ {action_name}: FAILED - {str(e)}")
        print()
    except Exception as e:
        print(f"❌ Registry test: FAILED - {str(e)}")
        print()

def main():
    """Run all tests"""
    print("🚀 Quick Actions Module Test Suite")
    print("=" * 50)
    print()
    
    test_individual_functions()
    test_utility_functions()
    test_quick_actions_registry()
    
    print("🎉 Test Suite Complete!")
    print("If you see ✅ for all tests, the Quick Actions module is working correctly.")

if __name__ == "__main__":
    main()
