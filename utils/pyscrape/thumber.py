import urllib
from PIL import ImageFile


def get_sizes(uri):
    """
    http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil

    needs libjpg etc on system-wide
    """
    # get file size *and* image size (None if not known)
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size:
        size = int(size)

    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None

if __name__ == '__main__':
    url = "http://i.imgur.com/5oUJ97s.png"
    print get_sizes(url)
