from unpack_pbpack import BMPResource
import Tkinter, random, sys

class App:
    def __init__(self, t):
        bmp = BMPResource(open(sys.argv[1], 'rb').read())
        print repr(bmp)
        
        self.i = Tkinter.PhotoImage(width=bmp.width,height=bmp.height)
        row = 0; col = 0; line = 0
        buffer = bmp.data
        while len(buffer) > 0:
            scanline = buffer[:bmp.scanlines]
            buffer = buffer[bmp.scanlines:]
            col = 0
            for o in xrange(bmp.scanlines-1):
                c = ord(scanline[o])
                for i in xrange(8):
                    if col >= bmp.width:
                        break
                    if c & 1 == 1:
                        self.i.put("#FFFFFF", (col,row))
                    else:
                        self.i.put("#000000", (col,row))
                    c = c >> 1
                    col += 1
            row = row + 1
            if row >= bmp.height:
                break
        c = Tkinter.Canvas(t, width=bmp.width, height=bmp.height); c.pack()
        c.create_image(0, 0, image = self.i, anchor=Tkinter.NW)

t = Tkinter.Tk()
a = App(t)    
t.mainloop()