#!/usr/bin/env python

from zipfile import ZipFile
from glob import glob
import sys, logging, os.path, os

if __name__ == "__main__":
    log = logging.getLogger()
    logging.basicConfig(format='[%(levelname)-8s] %(message)s')
    log.setLevel(logging.DEBUG)
    
    if len(sys.argv) < 2:
        log.error("Syntax: %s <one or more PBW files to unpack>" % sys.argv[0])
        sys.exit(1)
    
    for gl in sys.argv[1:]:
        #Not sure if this is Windows-unique behavior.
        for fn in glob(gl):
            log.info("Opening %s" % fn)
            basename = os.path.basename(fn)
            dirname = basename[:basename.rindex(".")]
            if os.path.exists(dirname):
                log.warn("Skipping %s because %s exists" % (basename, dirname))
                continue
            log.info("Unpacking to %s" % dirname)
            os.mkdir(dirname)
            
            with ZipFile(fn, 'r') as zf:
                zf.extractall(dirname)