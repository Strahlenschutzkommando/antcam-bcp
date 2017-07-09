#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
This code was inspired by the third python coding example on
http://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream
However, multiple customizations were applied and thus only the basic setup is
identical.

2017 Strahlenschutzkommando@Github
'''

import socket
import picamera

with picamera.PiCamera() as cam:
    cam.resolution = (640, 480)
    cam.framerate = 1/60

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept exclusively one connection and convert stream to file-like object
    connection = server_socket.accept()[0].makefile('wb')
    try:
        cam.start_recording(connection, format='h264')
        cam.wait_recording(60)
        cam.stop_recording()
    finally:
        connection.close()
        server_socket.close()
