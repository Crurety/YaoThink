
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__)) + "/backend"))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/backend"))

try:
    print("Attempting to import app.core.auth...")
    from app.core.auth import PhoneSmsLoginRequest, ChangePasswordRequest
    print("Successfully imported classes from app.core.auth")
    
    print("Attempting to import app.api.auth...")
    from app.api.auth import router
    print("Successfully imported app.api.auth")

except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except NameError as e:
    print(f"NameError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
