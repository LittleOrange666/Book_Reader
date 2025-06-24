import json
import os
import shutil
import uuid
import tqdm

if not os.path.isfile("data/book_dictionary"):
    print("file 'book_dictionary' missing")
    exit()
with open("data/book_dictionary", encoding="utf8") as f:
    bookfolder = f.read()


def main():
    names = {}
    if os.path.exists(os.path.join(bookfolder, "names.json")):
        with open(os.path.join(bookfolder, "names.json"), encoding="utf8") as f:
            names = json.load(f)
    for folder in tqdm.tqdm(os.listdir(bookfolder)):
        try:
            book = os.path.join(bookfolder, folder)
            if not os.path.isdir(book):
                continue
            if folder in names:
                continue
            name = "book_" + str(os.path.getctime(book)) + "_" + uuid.uuid5(uuid.NAMESPACE_DNS, folder).hex[:8]
            names[name] = folder
            shutil.move(book, os.path.join(bookfolder, name))
        except Exception as e:
            print(f"Error processing folder {folder}: {e}")
    with open(os.path.join(bookfolder, "names.json"), "w", encoding="utf8") as f:
        json.dump(names, f, ensure_ascii=False, indent=4)
    print(f"Created {len(names)} names.")
    input("Press Enter to exit...")


if __name__ == '__main__':
    main()
    print("Names created and saved to names.json")
