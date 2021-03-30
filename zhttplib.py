#!/usr/bin/env python3

import http.server
from http import HTTPStatus
import socketserver
import time


frog = rb"""
                             .-----.
                            /7  .  (
                           /   .-.  \
                          /   /   \  \
                         / `  )   (   )
                        / `   )   ).  \
                      .'  _.   \_/  . |
     .--.           .' _.' )`.        |
    (    `---...._.'   `---.'_)    ..  \
     \            `----....___    `. \  |
      `.           _ ----- _   `._  )/  |
        `.       /"  \   /"  \`.  `._   |
          `.    ((O)` ) ((O)` ) `.   `._\
            `-- '`---'   `---' )  `.    `-.
               /                  ` \      `-.
             .'                      `.       `.
            /                     `  ` `.       `-.
     .--.   \ ===._____.======. `    `   `. .___.--`     .''''.
    ' .` `-. `.                )`. `   ` ` \          .' . '  8)
   (8  .  ` `-.`.               ( .  ` `  .`\      .'  '    ' /
    \  `. `    `-.               ) ` .   ` ` \  .'   ' .  '  /
     \ ` `.  ` . \`.    .--.     |  ` ) `   .``/   '  // .  /
      `.  ``. .   \ \   .-- `.  (  ` /_   ` . / ' .  '/   .'
        `. ` \  `  \ \  '-.   `-'  .'  `-.  `   .  .'/  .'
          \ `.`.  ` \ \    ) /`._.`       `.  ` .  .'  /
    LGB    |  `.`. . \ \  (.'               `.   .'  .'
        __/  .. \ \ ` ) \                     \.' .. \__
 .-._.-'     '"  ) .-'   `.                   (  '"     `-._.--.
(_________.-====' / .' /\_)`--..__________..-- `====-. _________)
                 (.'(.'"""


pagedict = {"/": b"Pagedict was not changed, so enjoy this pic of a frog with a hat\n\n\n" + frog}
dodebug = False

def setdebug(newdebug):
    global dodebug
    if isinstance(newdebug, bool):
        dodebug = newdebug
    else:
        raise Exception("Newdebug must be bool")

def setpagedict(newpd):
    global pagedict
    if isinstance(pagedict, dict):
        pagedict = newpd
        print(f"updated: {pagedict}")
    else:
        raise Exception("Pagedict must be dict")

def start(ip="", port=8080):
    httpd = socketserver.TCPServer((ip, port), zhttp)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Program Exiting...")


class zhttp(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.pages()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.pages(post_data)

    def logger(self, iloglevel, logmsg):
        loglevels = {0: "Debug", 1: "Info", 2: "Warn", 3: "Error", 4: "Fatal Error"}
        try:
            strloglevel = loglevels[iloglevel]
        except:
            strloglevel = loglevels[1]
        timelist = list(time.localtime())
        for i in [3,4,5]:
            if int(timelist[i]) < 10:
                timelist[i] = "0" + str(timelist[i]) 
        if iloglevel == 0 and dodebug or iloglevel != 0:
            print("[{0}/{1}/{2} {3}:{4}:{5}]".format(timelist[1],timelist[2],timelist[0],timelist[3],timelist[4],timelist[5]), end="")
            print(f"::{strloglevel}- ", end="")
            print(logmsg, flush=True)
        return 0

    def pages(self, data=None):
        try:
            selection = pagedict[self.path]
        except KeyError:
            selection = pagedict["/"]
        try:
            if isinstance(selection, bytes):
                    self.wfile.write(selection)
            elif isinstance(selection, str):
                    self.wfile.write(selection.encode("utf-8"))
            elif type(selection) == type(setdebug):
                    output = selection(data)
                    if isinstance(output, bytes):
                        self.wfile.write(output)
                    else:
                        try:
                            self.wfile.write(str(output).encode("utf-8"))
                        except:
                            raise Exception("Illegal type")
            else:
                try:
                    self.wfile.write(str(selection).encode("utf-8"))
                except:
                    raise Exception("Illegal type")
        except ConnectionAbortedError:
            self.logger(3, "ConnectionAbortedError")
