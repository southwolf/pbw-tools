#!/usr/bin/env python
URI = 'http://pebble-static.s3.amazonaws.com/watchfaces/index.html'

from urllib2 import urlopen
from urlparse import urljoin, urlsplit
import logging, os.path

if __name__ == "__main__":
    log = logging.getLogger()
    logging.basicConfig(format='[%(levelname)-8s] %(message)s')
    log.setLevel(logging.DEBUG)
    
    log.info("Downloading watchfaces linked from %s" % URI)
    
    ind = urlopen(URI)
    
    #This is intentionally fragile to make it easier to detect changes.
    for line in ind:
        if line.startswith('    <a href="'):
            face = line[13:line.index(">")-1]
            face = urljoin(URI, face)
            facefile = face[face.rindex("/")+1:]
            if os.path.exists(facefile):
                log.warn('Did not download "%s" because it would overwrite an existing file' % facefile)
                continue
            with open(facefile, "wb") as f:
                log.info("Downloading %s -> %s" % (face, facefile))
                f.write(urlopen(face).read())