from tkinter import PhotoImage, messagebox
from threads import CustomThread
from PIL import ImageTk, Image
def filterPPM3(lines):
    # Brief:
    #   filters lines from comments
    #   splits lines into values
    # Return:
    #   list of values ['1','2','3'...]
    
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
        r = int(pixels[i])*255 // max_val
        g = int(pixels[i+1])*255// max_val
        b = int(pixels[i+2])*255// max_val
        line_data += '"#%02x%02x%02x" ' % (r, g, b)
    ret_val = "{" + line_data + "}"
    return ret_val




def loadPPM(file_path):
        with open(file_path, 'rb') as f:      
            width = 0
            height = 0
            max_val = 0
            data = []
            threads = []
            
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
                
                photo_image = PhotoImage(width=width, height=height) 
                data = list(f.read())
                data_len = len(data)
                first_half = width//2
                
                
                for a in range(0, data_len, width*3):           # Thread each row
                    line_end = a+width*3                      # line starts at a ends at line_chunk
                    zakres = data[a:line_end]
                    first_part = data[a:a+first_half*3]                 #   
                    second_part = data[a+first_half*3:line_end]  #
                    if data_len > line_end:
                        
                        threads.append(CustomThread(target=mergeLine, args=(first_part,max_val,)))
                        threads.append(CustomThread(target=mergeLine, args=(second_part,max_val,)))
                        
                    else:
                        threads.append(CustomThread(target=mergeLine, args=(first_part,max_val,)))
                        threads.append(CustomThread(target=mergeLine, args=(data[a+first_half*3:line_end],max_val,)))
                    
                    
                for a in threads:
                    a.start()
                for a in range(len(threads)):
                    line = threads[a].join()
                    photo_image.put(line, (0, a))



                
                return photo_image   
            else:
                messagebox.showerror("Error", "Bad PPM header")
                raise ValueError("BAD PPM file")
                

            
    
