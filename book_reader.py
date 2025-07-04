import json
import os
import platform
import re
import time
import uuid
from flask import Flask, render_template, request, jsonify, send_file

os.chdir(os.path.dirname(__file__))

if "BOOK_DIR" in os.environ:
    bookfolder = os.environ["BOOK_DIR"]
else:
    if not os.path.isfile("data/book_dictionary"):
        print("file 'book_dictionary' missing")
        exit()
    with open("data/book_dictionary", encoding="utf8") as f:
        bookfolder = f.read()
app = Flask(__name__, static_folder='static', static_url_path='')
books = {}
booktitles = {}
bookids = []
bookdata = []
bookcodes = {}
preload_cnt = 90
loading_step = 90
port = 6756
last_update = 0
last_run_update = 0
query_cnt = 0


def read_ctime(folder, s):
    if platform.system() != 'Windows' and s.count("_") == 2:
        return float(s.split("_")[1])
    return os.path.getctime(os.path.join(folder, s))


def update_books():
    global books, bookids, bookdata, bookcodes, last_update, last_run_update, query_cnt, booktitles
    query_cnt = 0
    last_update = os.path.getmtime(bookfolder)
    last_run_update = time.time()
    l = os.listdir(bookfolder)
    names = {}
    if os.path.exists(os.path.join(bookfolder, "names.json")):
        with open(os.path.join(bookfolder, "names.json"), encoding="utf8") as f:
            names = json.load(f)
    d = [(read_ctime(bookfolder, s), names.get(s, s), s) for s in l if
         os.path.exists(os.path.join(bookfolder, s, "icon.ico"))]
    d.sort(reverse=True)
    bookids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, o[1])) for o in d]
    books = {bookids[i]: o[2] for i, o in enumerate(d)}
    booktitles = {bookids[i]: o[1] for i, o in enumerate(d)}
    bookdata = [[str(uuid.uuid5(uuid.NAMESPACE_DNS, o[1])), o[1]] for o in d]
    if os.path.isfile("data/codes.json"):
        bookcodes = {}
        with open("data/codes.json") as f:
            obj = json.load(f)
        for k, v in obj.items():
            for ch in r'\/:*?"<>|':
                v = v.replace(ch, "_")
            bookcodes[v] = k


def check_update():
    if last_update < os.path.getmtime(
            bookfolder) and time.time() - last_run_update > 60 or time.time() - last_run_update > 1000 or query_cnt > 10:
        update_books()


def checkMobile(request):
    userAgent = request.headers.get('User-Agent', '')
    if userAgent == '':
        return False

    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) is not None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) is not None:
        return True
    return False


@app.route('/')
@app.route('/index')
def index():
    global query_cnt
    query_cnt += 1
    check_update()
    preload_cnt_local = min(preload_cnt, len(bookdata))
    if request.headers.get("host") == f"127.0.0.1:{port}":
        preload_cnt_local = len(bookdata)
    return render_template('index.html', mobile=checkMobile(request), data=bookdata[:preload_cnt_local],
                           preload_cnt=str(preload_cnt_local), loading_step=str(loading_step))


@app.route('/get', methods=['POST'])
def get():
    check_update()
    start = int(request.form['start']) if "start" in request.form else 0
    stop = int(request.form["stop"])
    stop = min(stop, len(books))
    start = max(0, start)
    return jsonify(bookdata[start:stop])


@app.route('/icon/<name>', methods=['GET'])
def icon(name):
    return send_file(os.path.join(bookfolder, books[name], "icon.ico"), mimetype='image/x-icon')


@app.route('/book/<name>', methods=['GET'])
def book(name):
    folder = os.path.join(bookfolder, books[name])
    l = os.listdir(folder)
    if "icon.ico" in l:
        l.remove("icon.ico")
    if "desktop.ini" in l:
        l.remove("desktop.ini")
    l.sort(key=lambda x: int(x.split(".")[0]))
    source = ""
    if booktitles[name] in bookcodes:
        source = bookcodes[booktitles[name]]
    return render_template('book.html', name=name, title=booktitles[name], pages=l, mobile=checkMobile(request),
                           source=source)


@app.route('/book/<name>/<page>', methods=['GET'])
def readbook(name, page):
    tp = 'image/jpeg'
    if page.endswith(".png"):
        tp = 'image/png'
    return send_file(os.path.join(bookfolder, books[name], page), mimetype=tp)


if __name__ == '__main__':
    update_books()
    app.run("0.0.0.0", port=port)
