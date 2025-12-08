import importlib.util
spec = importlib.util.spec_from_file_location("settings", "oliveoshoppe/settings.py")
settings = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(settings)
    print("SUCCESS: Settings loaded")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
