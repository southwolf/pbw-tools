#!/usr/bin/env python

from zipfile import ZipFile
from glob import glob
import sys, logging, os.path, os, struct, json
from libpebble.stm32_crc import crc32

log = logging.getLogger()
logging.basicConfig(format='%(message)s')
log.setLevel(logging.DEBUG)

class BMPResource:
    def __init__(self, data):
        (self.depth,self.unknown_1,self.unknown_2,self.width,self.height) = struct.unpack("<hhlhh", data[:12])
        assert(self.unknown_1 == 4096)
        assert(self.unknown_2 == 0)
        self.data = data[12:]
        
        #log.debug(repr(self))
    
    def __repr__(self):
        return "<BMP %dx%d %2dB/scanline size %d>" % (self.width,self.height,self.depth,len(self.data))

class Resource:
    def __init__(self, raw, file):
        (self.index, self.offset, self.size, self.crc) = struct.unpack("<LLLL", raw)
        #Resources are loaded sequentially, so...
        self.raw_data = file.read(self.size)
        self.png = BMPResource(self.raw_data)
        log.debug("%08X | %08X" % (self.crc, crc32(self.raw_data)))
        log.debug(repr(self))
        assert(self.crc == crc32(self.raw_data))
        
        
    
    def __str__(self):
        return self.png.data
    
    def __repr__(self):
        return "<Resource %2d @ %04x:%04x CRC:%08x %s>" % (self.index, self.offset, self.offset+self.size, self.crc, repr(self.png))

class PBPack:
    def __init__(self, pack):
        (self.resource_count, self.unknown_1, self.timestamp, self.name) = struct.unpack("<LLL16s", pack.read(12+16))
        resource_block = pack.read(4096)
        offset = 0
        self.resources = []
        for i in xrange(self.resource_count):
            offset = 16*i
            self.resources.append(Resource(resource_block[offset:offset+16], pack))
    
    def pack(self):
        return struct.pack("<LLL16s", self.resource_count, self.unknown_1, self.timestamp, self.name)
    
    def __repr__(self):
        return "<PBPack %08X \"%s\" [%d]>" % (self.unknown_1, self.name, self.resource_count)

if __name__=="__main__":
    
    log.info('Processing "%s"' % "app_resources.pbpack")
    p = PBPack(open("app_resources.pbpack", 'rb'))
    log.info(p)