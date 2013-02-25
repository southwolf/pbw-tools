import sys, struct
from libpebble.stm32_crc import crc32
import validate_pbpack

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
<<<<<<< HEAD
    
    raw = open('pebble-app.bin', 'rb').read()
    
    pa = PebbleApp(raw)
    
    with open('pebble-app.bin', 'rb') as f:
=======
    r2 = open(sys.argv[1], 'rb').read()
    with open(sys.argv[1], 'rb') as f:
>>>>>>> refs/remotes/origin/master
        header = f.read(8+8+8+32+32+20)
        (magic, version, sdk_version, app_version, size, entry_point, app_crc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs) = struct.unpack("<8sHHHHII32s32sIIIII", header)
        print (magic, version, sdk_version, app_version, size, hex(entry_point), hex(app_crc), old_name, old_company, unknown3, hex(jump_table), flags, hex(reloc_list), num_relocs)
        binary = f.read()
        
        #WARNING: THE BELOW WORK ISN'T COMPLETE AND WILL ONLY WORK FOR BIG-TIME-12 and BIG-TIME-24
        raw = header + binary
        coda = binary[-(4*num_relocs):]
        rheader = binary[-132:-(4*num_relocs)]
        
        binary = binary[:-132]
        
        (resource_crc, resource_timestamp, resource_name) = struct.unpack("<LL16s", rheader[:24])
        
        
        pbp = validate_pbpack.PBPack(open("app_resources.pbpack", 'rb'))
        res_header = struct.pack("<LL16s", pbp.crc, pbp.timestamp, pbp.name)
        
        crheader = rheader[24:]
        
        crcs = [x.crc for x in pbp.resources]
        out_crc = ""
        for c in crcs:
            out_crc += struct.pack("<I", c)
        
        rheader = res_header + out_crc + rheader[24+len(out_crc):]
        
        print "EXP: 0x%08X (%d)" % (app_crc,app_crc)
        rc = crc32(binary+rheader)
        print "CRC: 0x%08X (%d)" % (rc,rc)
        header = struct.pack("<8sHHHHII32s32sIIIII", magic, version, sdk_version, app_version, size, entry_point, rc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs)
        
        
    
    with open('pebble-app.bin', 'wb') as f:
        f.write(header + binary + rheader + coda)
