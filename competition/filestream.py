# Run with python3
import io
import cv2
import logging
import SocketServer
from threading import Condition
import threading
import SimpleHTTPServer as server
import BaseHTTPServer as baseserver

PAGE="""\
<html>
<head>
<title>JPEG File streaming demo</title>
<script>console.log("Hello, world!");</script>
</head>
<body>
<h1>JPEG File Streaming Demo</h1>
<img src="img.jpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buff = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buff.truncate()
            self.buff.write(buf)
            self.frame = self.buff.getvalue()
            self.buff.seek(0)
        return self.frame
class StreamingHandler(baseserver.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/img.jpg':
            self.send_response(200)
            frame = output.frame
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', len(frame))
            self.end_headers()
            self.wfile.write(frame)

            '''
            frame = output.frame
            self.send_response(200)
            #self.send_header('Age', 0)
            #self.send_header('Cache-Control', 'no-cache, private')
            #self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', len(frame))
            self.end_headers()
            #self.wfile.write(b'--FRAME\r\n')
            self.wfile.write(frame)
            #self.wfile.write(b'\r\n')
            try:
                while True:
                    frame = output.frame
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
            except Exception as e:
                print(e)
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
            '''
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(SocketServer.ThreadingMixIn, baseserver.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class StreamingThread(object):
    def __init__(self, output):
        self.stopped = False
        self.output = output
        self.counter = 0

    def start(self, data0, data1):
        threading.Thread(target=self.stream_file, args=(data0, data1, self.output)).start()

    def stream_file(self, data0, data1, output):
        while not self.stopped:
            self.counter += 1
            if self.counter % 2 == 0:    
                 output.write(data0)
            else:
                 output.write(data1)

    def stop(self):
        self.stopped = True

output = StreamingOutput()
stream = StreamingThread(output)

img0 = cv2.imread("./twotargets1.jpg")
data0 = cv2.imencode('.jpg', img0)[1].tostring()

img1 = cv2.imread("./twotargets4.jpg")
data1 = cv2.imencode('.jpg', img1)[1].tostring()

stream.start(data0, data1)

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print("Keyboard interrupted program!")
finally:
    print("Stopping stream...")
    stream.stop()
    #camera.stop_recording()
