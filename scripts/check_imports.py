
import sys
import os
import traceback

sys.path.append(os.getcwd())

print("Attempting to import palace...")
try:
    import backend.app.core.ziwei.palace as palace
    print("Successfully imported palace.")
except Exception:
    traceback.print_exc()

print("\nAttempting to import advanced...")
try:
    import backend.app.core.ziwei.advanced as advanced
    print("Successfully imported advanced.")
except Exception:
    traceback.print_exc()
