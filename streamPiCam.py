#!/usr/bin/env python3

'''
This code was inspired by the third python coding example on
http://picamera.readthedocs.io/en/release-1.10/recipes1.html
                              #recording-to-a-network-stream
However, multiple customizations were applied and thus only the basic setup is
identical.

Availible under the MIT license.
2017 Strahlenschutzkommando@Github
'''

import socket
import picamera

with picamera.PiCamera() as cam:
    cam.resolution = (960, 720)
    cam.framerate = 1/60

    server_socket = socket.socket()
    try:
        server_socket.bind(('0.0.0.0', 8000))
        while(True):
            server_socket.listen(0)

            # Accept exactly one connection once and convert stream to file-like object
            connection = server_socket.accept()[0].makefile('wb')
            try:
                cam.start_recording(connection, format='h264')
                cam.wait_recording(60)
                cam.stop_recording()
            finally:
                connection.close()
    finally:
        server_socket.close()
