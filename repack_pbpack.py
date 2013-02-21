#!/usr/bin/env python

import sys, logging, os.path, os, struct, json
from libpebble.stm32_crc import crc32
from validate_pbpack import BMPResource, Resource, PBPack

if __name__=="__main__":
    log = logging.getLogger()
    logging.basicConfig(format='%(message)s')
    log.setLevel(logging.DEBUG)

    #log.info('Processing "%s"' % "app_resources.pbpack")
    #p = PBPack(open("app_resources.pbpack.backup"))
    #log.info(p)
    
    manifest = None
    with open("manifest.json", "r") as mf:
        manifest = json.load(mf)
    
    if manifest is None:
        sys.exit(1)
    
    with open("app_resources.pbpack", "wb") as pbf:
        pbf.write("\0"*28)
        index = 1
        offset = 0
        raws = []
        for resource in manifest['debug']['resourceMap']['media']:
            fn = "%s.%s" % (resource['defName'],resource['type'])
            size = os.stat(fn).st_size
            raw = open(fn, 'rb').read()
            crc = crc32(raw)
            raws.append(raw)
            pbf.write(struct.pack("<LLLL", index, offset, size, crc))
            print "<Resource %2d @ %04x:%04x CRC:%08x>" % (index, offset, offset+size, crc)
            index += 1
            offset += size
        pbf.write("\0" * (4096+28-pbf.tell()))
        for raw in raws:
            pbf.write(raw)
        
        pbf.seek(0)
        pbf.write(struct.pack("<LLL16s", index-1, crc32(''.join(raws)), manifest['resources']['timestamp'], str(manifest['resources']['friendlyVersion'])))
