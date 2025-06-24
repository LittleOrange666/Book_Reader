import os

from PIL import Image

if __name__ == '__main__':
    with open("data/book_dictionary", encoding="utf8") as f:
        bookfolder = f.read()
    cnt = len(os.listdir(bookfolder))
    i = 0
    for folder in os.listdir(bookfolder):
        book = os.path.join(bookfolder, folder)
        print(f"process {book}")
        for name in os.listdir(book):
            if name.endswith(".png"):
                file = os.path.join(book, name)
                img = Image.open(file)
                if img.mode != "RGB":
                    img = img.convert('RGB')
                img.save(file[:-4]+".jpg")
                os.remove(file)
        i += 1
        print(f"{i}/{cnt}")
