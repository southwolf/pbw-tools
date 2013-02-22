import sys, struct
from libpebble.stm32_crc import crc32

if __name__ == "__main__":
    name = sys.argv[1]
    company = sys.argv[2]
    
    raw = open('pebble-app.bin', 'rb').read()
    
    with open('pebble-app.bin', 'rb') as f:
        header = f.read(8+8+8+32+32+20)
        (magic, version, sdk_version, app_version, size, entry_point, crc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs) = struct.unpack("<8sHHHHII32s32sIIIII", header)
        crc = long(crc)
        print (magic, version, sdk_version, app_version, size, entry_point, hex(crc), old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs)
        binary = f.read()
        
        print "EXP: 0x%08X (%d)" % (crc,crc)
        rc = crc32(raw)
        print "RAW: 0x%08X (%d)" % (rc,rc)
        rc = crc32(binary)
        print "BIN: 0x%08X (%d)" % (rc,rc)
        
        
        
        with open("log.crc.txt", 'w') as f:
            for i in xrange(len(raw)+1):
                for j in xrange(i,len(raw)+1):
                    nc = crc32(raw[i:j])
                    if crc == nc:
                        print "(%d,%d) - %08X" % (i,j,crc)
                        f.write("(%d,%d) - %08X" % (i,j,crc))
                print "Pass %d of %d complete" % (i, len(raw))
                f.write("Pass %d of %d complete" % (i, len(raw)))
    
    #struct.pack("<8sHHHHII32s32sIIIII"
    
    #with open('pebble-app.bin', 'wb') as f:
    #    f.write(