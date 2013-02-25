import sys, struct
from libpebble.stm32_crc import crc32

class PebbleApp:
    @staticmethod
    def validate_magic(value, raw):
        assert value==PebbleApp.PEBBLE_MAGIC, "Invalid Pebble Magic - expected %s got %s" % (repr(PebbleApp.PEBBLE_MAGIC), repr(value))
    
    @staticmethod
    def validate_size(value, raw):
        assert value==PebbleApp.PEBBLE_MAGIC, "Invalid Pebble Magic - expected %s got %s" % (repr(PebbleApp.PEBBLE_MAGIC), repr(value))

    @staticmethod
    def validate_offset(value, raw):
        assert value==PebbleApp.PEBBLE_MAGIC, "Invalid Pebble Magic - expected %s got %s" % (repr(PebbleApp.PEBBLE_MAGIC), repr(value))

    @staticmethod
    def validate_crc(value, raw):
        assert value==PebbleApp.PEBBLE_MAGIC, "Invalid Pebble Magic - expected %s got %s" % (repr(PebbleApp.PEBBLE_MAGIC), repr(value))

    
    PEBBLE_HEADER_FORMAT = [
    ("magic", "8s", validate_magic),
    ("version", "H"),
    ("sdk_version", "H"),
    ("app_version", "H"),
    ("size", "I", validate_size),
    ("entry_point", "I", validate_offset),
    ("crc", "I", validate_crc),
    ("name", "32s"),
    ("company", "32s"),
    ("unknown3", "I"),
    ("jump_table", "I", validate_offset),
    ("flags", "I", validate_offset),
    ("reloc_list", "I", validate_offset),
    ("num_relocs", "I"),
    ]
    
    PEBBLE_JOINED_HEADER = "<"+"".join([x[1] for x in PEBBLE_HEADER_FORMAT])
    PEBBLE_MAGIC="PBLAPP\x00\x00"
    
    def __init__(self, raw):
        self.header = {}
        offset = 0
        offset = struct.calcsize(PebbleApp.PEBBLE_JOINED_HEADER)
        print struct.unpack_from(PebbleApp.PEBBLE_JOINED_HEADER, raw)
        print offset

if __name__ == "__main__":
    
    raw = open('pebble-app.bin', 'rb').read()
    
    pa = PebbleApp(raw)
    
    with open('pebble-app.bin', 'rb') as f:
        header = f.read(8+8+8+32+32+20)
        (magic, version, sdk_version, app_version, size, entry_point, crc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs) = struct.unpack("<8sHHHHII32s32sIIIII", header)
        crc = long(crc)
        print (magic, version, sdk_version, app_version, size, hex(entry_point), hex(crc), old_name, old_company, unknown3, hex(jump_table), flags, hex(reloc_list), num_relocs)
        binary = f.read()
        
        print "EXP: 0x%08X (%d)" % (crc,crc)
        rc = crc32(raw[108:len(raw)-8])
        print "MIN: 0x%08X (%d)" % (rc,rc)
        rc = crc32(raw[108:len(raw)-11])
        print "MAX: 0x%08X (%d)" % (rc,rc)
        rc = crc32(binary)
        print "BIN: 0x%08X (%d)" % (rc,rc)
        
        (end1,end2) = struct.unpack("<II", binary[-8:])
        print "END1: 0x%08X (%d)" % (end1, end1)
        print "END2: 0x%08X (%d)" % (end2, end2)
        print "SIZE: 0x%08X (%d)" % (size, size)
        print "DIFF: 0x%08X (%d)" % (size-end1, size-end1)
        (en1,) = struct.unpack("<I", binary[end1-108:end1+4-108])
        (en2,) = struct.unpack("<I", binary[end2-108:end2+4-108])
        print "*EN1: 0x%08X (%d)" % (en1, en1)
        print "*EN2: 0x%08X (%d)" % (en2, en2)
        (n1,) = struct.unpack("<I", binary[en1-108:en1+4-108])
        (n2,) = struct.unpack("<I", binary[en2-108:en2+4-108])
        print "**N1: 0x%08X (%d)" % (n1, n1)
        print "**N2: 0x%08X (%d)" % (n2, n2)
        
    
    #struct.pack("<8sHHHHII32s32sIIIII"
    
    #with open('pebble-app.bin', 'wb') as f:
    #    f.write(