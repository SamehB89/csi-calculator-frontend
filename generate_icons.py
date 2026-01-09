from PIL import Image
import os

source_path = r'd:\SUPERMANn\CSI_Project\frontend\assets\icon-1024.jpg'
dest_dir = r'd:\SUPERMANn\CSI_Project\frontend\assets'

try:
    with Image.open(source_path) as img:
        # Convert to RGB (ensure no weird modes)
        img = img.convert('RGB')
        
        # Save 512x512 PNG
        img512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img512.save(os.path.join(dest_dir, 'icon-512.png'), 'PNG')
        print("Created icon-512.png")
        
        # Save 192x192 PNG
        img192 = img.resize((192, 192), Image.Resampling.LANCZOS)
        img192.save(os.path.join(dest_dir, 'icon-192.png'), 'PNG')
        print("Created icon-192.png")
        
except Exception as e:
    print(f"Error converting icons: {e}")
