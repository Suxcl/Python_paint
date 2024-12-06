from tkinter import *
from threading import Thread



class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args, **kwargs):
        # super().join(*args, **kwargs)
        Thread.join(self, *args)
        return self._return

# Brief:
#   filters lines from comments
#   splits lines into values
# Return:
#   list of values ['1','2','3'...]

def filterPPM3(lines):
    filtered_values = []
    for a in lines:
        if '#' in a:
            a = a.split('#')[0]
        if a: filtered_values.extend(a.split())
    return filtered_values

def mergeLine(pixels, max_val):
    pixels_len = len(pixels)
    line_data = ""
    for i in range(0, pixels_len, 3):
        r = int(int(pixels[i])*255 // max_val)
        g = int(int(pixels[i+1])*255// max_val)
        b = int(int(pixels[i+2])*255// max_val)
        line_data += '"#%02x%02x%02x" ' % (r, g, b)
    ret_val = "{" + line_data + "}"
    return ret_val


def loadPPM(file_path):
        with open(file_path, 'rb') as f:      
            width = 0
            height = 0
            max_val = 0
            data = []
            
            header = f.readline().decode().strip() 

            if(header == 'P3'):
                # Read headers
                for line in f:
                    line = line.decode('ascii', errors='ignore')
                    line = line.replace('\n','')
                    if '#' in line:
                        line = line.split('#')[0]
                    if line:
                        line_val = line.split()
                        for a in line_val:
                            data.append(a)
                    if len(data) >= 3:
                        width = int(data.pop(0))
                        height = int(data.pop(0))
                        max_val = int(data.pop(0))
                        break                      
                
                prefix = b''
                if len(data) > 0 :
                    prefix = b'\n'
                    data.reverse()
                    for a in data:
                        prefix = a.encode() + prefix
                    
                data = f.read()                                 # read whole file
                data = prefix+data                              # add prefix if somethink was read while finding headers
                data = data.decode('ascii', errors='ignore')    # decode into string
                data = data.split('\n')                         # split into list
                 
                data_len = len(data)
                
                photo_image = PhotoImage(width=width, height=height)        

                threads = []
                filtered_data = []
                val = int(data_len*0.03)                        # change this value to set Thread amount
                                                                # for comment removal
                if(val == 0):
                    filtered_data = filterPPM3(data)
                else:
                    for a in range(0, data_len, val):
                        target = a+val
                        if data_len > target:
                            threads.append(CustomThread(target=filterPPM3, args=(data[a:a+val],)))
                        else:
                            threads.append(CustomThread(target=filterPPM3, args=(data[a:data_len],)))
                        threads[-1].start()
                    # for a in threads:
                    #     a.start()
                    for a in threads:
                        lines = a.join()
                        filtered_data.extend(lines)
                
            
                fil_data_len = len(filtered_data)
                y = 0
                threads = []
                for a in range(0, fil_data_len, width*3):           # Thread each row
                    line_chunk = a+width*3
                    if fil_data_len > line_chunk:
                        threads.append(CustomThread(target=mergeLine, args=(filtered_data[a:line_chunk],max_val,)))
                    else:
                        threads.append(CustomThread(target=mergeLine, args=(filtered_data[a:fil_data_len],max_val,)))
                    y+=1
                    threads[-1].start()
                # for a in threads:
                #     a.start()
                for a in range(len(threads)):
                    line = threads[a].join()
                    photo_image.put(line, (0, a))

                return photo_image   
            
            elif(header == 'P6'):
                data = f.read()
                data = data.decode('ascii', errors='ignore')
                # split file by \n chars into list of lines
                
                
                # read values for size
                # divide by rgb and put into image
            else:
                raise ValueError("BAD PPM file")
            
              
            
            
            
            # if header == "P3":
            #     for index, line in enumerate(filtered_lines):
            #         if(index not in [0,1,2]):
            #             data.append(list(map(int, line.split())))

            # elif header == "P6":
            #     # width * 3
            #     data = list(f.read())
            #     x = width*3
            #     for index, line in enumerate(filtered_lines):
            #         if index not in [0,1,2]:
            #             data.append(line)        
                
                
                    
                

            # pixels = []
            # photo_image = PhotoImage(width=width, height=height)
            
            # for j in range(len(data)):
            #     line = data[j]
            #     pixel_line = []
            #     for i in range(0, len(line),3):
            #         try:
            #             r,g,b = data[j][i], data[j][i+1], data[j][i+2]
            #             pixel_line.append((r,g,b))
            #         except IndexError:
            #             print("Index error")
            #             print(r,g,b)
            #             print(i,j)
            #     pixels.append(pixel_line)

            # for y,line in enumerate(pixels):
            #     for x,rgb in enumerate(line):
            #         photo_image.put("#%02x%02x%02x" % (rgb[0],rgb[1],rgb[2]), (x, y))
                    
