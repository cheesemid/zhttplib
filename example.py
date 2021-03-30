#!/usr/bin/env python3

import zhttplib


zhttplib.setpagedict({"/": "it works!"})
zhttplib.start(ip="127.0.0.1",port=9999)