from unpack_pbpack import BMPResource
import sys, glob

if __name__ == "__main__":
    for a in sys.argv[1:]:
        for n in glob.glob(a):
            bmp = open(n, 'rb').read()
            
            with open(n, 'wb') as f:
                f.write(bmp[:12])
                bmp = bmp[12:]
                for c in [~ord(x) & 0xFF for x in bmp]:
                    f.write(chr(c))