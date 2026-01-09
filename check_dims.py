import struct
import glob
import os

def get_png_size(file_path):
    with open(file_path, 'rb') as f:
        data = f.read(24)
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            w, h = struct.unpack('>LL', data[16:24])
            return w, h, data
        return None, None, data

print("Checking assets dimensions...")
assets_path = r'd:\SUPERMANn\CSI_Project\frontend\assets'
for img_path in glob.glob(os.path.join(assets_path, '*.png')):
    w, h, data = get_png_size(img_path)
    if w:
        print(f"{os.path.basename(img_path)}: {w}x{h}")
    else:
        print(f"{os.path.basename(img_path)}: Not a valid PNG signature. Header: {data[:16].hex()}")
