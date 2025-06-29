
from PIL import Image, ImageTk

class ImageLoader:
    def __init__(self):
        self.cache = {}
        self.blank = self._create_blank()

    def _create_blank(self):
        img = Image.new('RGBA', (1, 25), (0,0,0,0))
        return ImageTk.PhotoImage(img)

    def load_silent(self, paths):
        return [self._load_single(p) for p in paths]

    def _load_single(self, path):
        if not path: return self.blank
        if path in self.cache: return self.cache[path]
        try:
            img = Image.open(path)
            w, h = img.size
            scale = 25 / h
            new_w = int(w * scale)
            resized = img.resize((new_w,25), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            self.cache[path] = photo
            return photo
        except:
            return self.blank