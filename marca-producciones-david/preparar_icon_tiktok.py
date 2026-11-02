import subprocess
from PIL import Image

src = "/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/marca-producciones-david/avatar_perfil_ig_tiktok.jpg"
dst = "/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/marca-producciones-david/app_icon_1024.jpg"

im = Image.open(src)
im_resized = im.resize((1024, 1024), Image.Resampling.LANCZOS)
im_resized.save(dst, "JPEG", quality=95)
print("Icono 1024x1024 creado:", dst)
