"""
Cleanup script to delete screenshots and media files from .gemini folder
"""
import os
import glob

# Paths to clean
base_path = r"C:\Users\super\.gemini\antigravity\brain"

# Extensions to delete
extensions = ['*.png', '*.jpg', '*.jpeg', '*.webp', '*.gif', '*.mp4', '*.webm', '*.avi', '*.mov']

total_files = 0
total_size = 0

print("🧹 Starting cleanup of media files...")
print("=" * 50)

for ext in extensions:
    pattern = os.path.join(base_path, '**', ext)
    files = glob.glob(pattern, recursive=True)
    
    for file_path in files:
        try:
            size = os.path.getsize(file_path)
            os.remove(file_path)
            total_files += 1
            total_size += size
            print(f"  ✅ Deleted: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"  ❌ Error: {file_path} - {e}")

print("=" * 50)
print(f"🎉 Cleanup complete!")
print(f"   Files deleted: {total_files}")
print(f"   Space freed: {total_size / (1024*1024):.2f} MB")
