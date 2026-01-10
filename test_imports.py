import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deaddrop.settings')
django.setup()

print("Django setup successful!")

try:
    from board import views
    print("Views imported successfully!")
    
    from board import models
    print("Models imported successfully!")
    
    from board import urls
    print("URLs imported successfully!")
    
    print("\nAll imports working! Starting server should work.")
    
except Exception as e:
    print(f"Error during import: {e}")
    import traceback
    traceback.print_exc()
