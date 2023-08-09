import os

from PIL import Image

if __name__ == '__main__':
    with open("book_dictionary", encoding="utf8") as f:
        bookfolder = f.read()
    cnt = len(os.listdir(bookfolder))
    i = 0
    for folder in os.listdir(bookfolder):
        book = os.path.join(bookfolder, folder)
        print(f"process {book}")
        for name in os.listdir(book):
            if name.endswith(".jpg"):
                file = os.path.join(book, name)
                img = Image.open(file)
                img.save(file, quality=50)
        i += 1
        print(f"{i}/{cnt}")
