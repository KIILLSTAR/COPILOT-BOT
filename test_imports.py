#!/usr/bin/env python3
"""
Test script to verify all consolidated modules can be imported correctly
"""
import sys

def test_imports():
    """Test all consolidated module imports"""
    print("🧪 Testing consolidated module imports...")
    
    try:
        # Test config import
        print("Testing app_config import...")
        import app_config
        print("✅ app_config imported successfully")
        
        # Test logger import
        print("Testing app_logger import...")
        import app_logger
        print("✅ app_logger imported successfully")
        
        # Test dashboard import
        print("Testing app_dashboard import...")
        import app_dashboard
        print("✅ app_dashboard imported successfully")
        
        # Test core_trading import
        print("Testing app_core_trading import...")
        import app_core_trading
        print("✅ app_core_trading imported successfully")
        
        # Test cli import
        print("Testing app_cli import...")
        import app_cli
        print("✅ app_cli imported successfully")
        
        # Test safe_wallet import
        print("Testing app_safe_wallet import...")
        import app_safe_wallet
        print("✅ app_safe_wallet imported successfully")
        
        print("\n🎉 All consolidated modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_functionality():
    """Test basic functionality of consolidated modules"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        # Test config functionality
        import app_config
        print(f"✅ Safety status: {app_config.safety.is_dry_run_forced()}")
        print(f"✅ Dry run mode: {app_config.DRY_RUN}")
        
        # Test logger functionality
        import app_logger
        app_logger.log_info("Test log message")
        print("✅ Logger functionality working")
        
        # Test dashboard functionality
        import app_dashboard
        print("✅ Dashboard classes available")
        
        # Test core_trading functionality
        import app_core_trading
        pnl = app_core_trading.get_simulated_pnl()
        print(f"✅ Simulated PnL: ${pnl}")
        
        print("\n🎉 All functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting consolidation test...")
    
    import_success = test_imports()
    if import_success:
        func_success = test_functionality()
        if func_success:
            print("\n✅ All tests passed! Consolidation successful.")
            sys.exit(0)
        else:
            print("\n❌ Functionality tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed.")
        sys.exit(1)