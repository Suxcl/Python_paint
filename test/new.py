from PIL import Image
import numpy as np

    
# img_array = np.array(self.PILImage)   
# D = 0

# hist_r = np.histogram(img_array[:,:,0], bins=256, range=(0,255))[0]
# hist_g = np.histogram(img_array[:,:,1], bins=256, range=(0,255))[0]
# hist_b = np.histogram(img_array[:,:,2], bins=256, range=(0,255))[0]

hist = [2,5,0,3,9,1]

# get amount of pixels
pixel_count = 


D_r = []
D_g = []
D_b = []
r_sum = 0
g_sum = 0
b_sum = 0
# calculate D
for i in range(len(hist_r)):
    r_sum = r_sum + hist_r[i]
    g_sum = g_sum + hist_g[i]
    b_sum = b_sum + hist_b[i]
    D_r.append(r_sum/pixel_count)
    D_g.append(g_sum/pixel_count)
    D_b.append(b_sum/pixel_count)

# find first D non-zero value
non_zero_D_r = 0
non_zero_D_g = 0
non_zero_D_b = 0
for i in range(len(D_r)):
    if D_r[i] != 0:
        non_zero_D_r = D_r[i]
        break
for i in range(len(D_g)):
    if D_g[i] != 0:
        non_zero_D_g = D_g[i]
        break
for i in range(len(D_b)):
    if D_b[i] != 0:
        non_zero_D_b = D_b[i]
        break

LUT = [0] * 256
# calculate LUT
for a in range(len(D_r)):
    a_licznik = D_r[a] - non_zero_D_r
    a_mianownik = 1 - non_zero_D_r
    a_a = a_licznik/a_mianownik
    a_b = a_a * 255
    LUT[a] = a_b
