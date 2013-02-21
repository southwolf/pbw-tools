import sys, struct
from libpebble.stm32_crc import crc32

if __name__ == "__main__":
    name = sys.argv[1]
    company = sys.argv[2]
    
    raw = open('pebble-app.bin', 'rb').read()
    
    with open('pebble-app.bin', 'rb') as f:
        header = f.read(8+8+8+32+32+20)
        (magic, version, sdk_version, app_version, size, entry_point, crc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs) = struct.unpack("<8sHHHHII32s32sIIIII", header)
        print (magic, version, sdk_version, app_version, size, entry_point, crc, old_name, old_company, unknown3, jump_table, flags, reloc_list, num_relocs)
        binary = f.read()
        
        for i in xrange(len(raw)):
            nc = crc32(raw[i:])
            if crc == nc:
                print "%d - %08X" % (crc, i)
    
    #struct.pack("<8sHHHHII32s32sIIIII"
    
    #with open('pebble-app.bin', 'wb') as f:
    #    f.write(