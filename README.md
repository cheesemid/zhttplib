# ZHTTPLIB

**Don't host server publicly!!!** Run over VPN or Proxy (Uses http.server which only has basic security)  
Follow the example in `example.py` or below

    #!/usr/bin/env python3

    import zhttplib
    import time

    # All methods must have a parameter incase of POST requests to the endpoint
    # data will be passed as bytestring
    def sayhello(data):
        return "hello"

    def gettime(data):
        return time.time()

    # Pagedict values can be any type that have __str__() or __repr__() functions 
    # or functions themselves which will be run to return these types
    pagedict = {"/": b"it works!",
                "/list": [1,2,3,4,"5"],
                "/fish": "><>",
                "/sayhello": sayhello,
                "/whatsthetime": gettime,
                }

    zhttplib.setpagedict(pagedict)

    zhttplib.start(ip="127.0.0.1",port=9999)