# Comic Book Reader

A simple comic book reader

## Installation

### Install the Python

Python version is not important for this program

but Python 3.10.6 is suggested

### Install this repository

Using git:
```cmd
git clone https://github.com/LittleOrange666/Book_Reader.git
```
Or you can download zip file from github and unzip it.

### Install Python dependencies

```cmd
pip install -r requirements.txt
```

### setup target folder

create a file named "book_dictionary" without any filename extension

and write full path of the book dictionary in it.

### Requires of the book dictionary

+ the book dictionary should all book directly by folders
+ the folder name of books should be their name
+ the pages should be JPEG or PNG images
+ the pages' order should equal to the alphabetical order of the filenames
+ in the folder of every book should contain "icon.ico" to be the cover of book

### "makeicon.py"

this file can automatically add "icon.ico" to every book.

It use alphabetical first file to be the book cover,

and it use "book_dictionary" to find books too.

### start reading

Double click the "book_reader.py" or use python to open it.

It will start a local website on port 6756,

and you can enjoy it by open "http://127.0.0.1:6756".

It is suggested to use this with NAT traversal to read books on the mobile device.

It is suggested to use with the [Web Tool Manager](https://github.com/LittleOrange666/Web_Tool_Manager)