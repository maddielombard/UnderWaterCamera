import io
import socket
import struct

from PIL import Image
import matplotlib.pyplot as pl

sever_socket = socket.socket()
sever_socket.bind(('INSERT RASP PI IP ADDRESS HERE', 8000))
sever_socket.listen(0)

connection =sever_socket.accept()[0].makefile('rb')
try:
    img = None
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        image_stream.seek(0)
        image = Image.open(image_stream)

        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

        pl.pause(0.01)
        pl.draw()

        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')

finally:
    connection.close()
    sever_socket.close()
