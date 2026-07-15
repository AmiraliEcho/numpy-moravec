import numpy as np
from PIL import Image, ImageDraw


img=Image.open("images/mouse.png").convert("L")  
img= img.resize((256, 256))                 
gray = np.array(img, dtype=np.float32)       


window_size = 3
offset = window_size // 2
shifts = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]


gray = np.pad(gray, pad_width=1, mode='constant', constant_values=0)


response = np.zeros_like(gray)


height, width = gray.shape
for x in range(offset + 1, height - offset - 1, 2):    
    for y in range(offset + 1, width - offset - 1, 2):
        window = gray[x - offset:x + offset + 1, y - offset:y + offset + 1]
        ssd_list = []
        for dx, dy in shifts:
            shifted = gray[
                x - offset + dx:x + offset + 1 + dx,
                y - offset + dy:y + offset + 1 + dy
            ]
            diff = (window - shifted) ** 2
            ssd = np.sum(diff)
            ssd_list.append(ssd)
        response[x, y] = min(ssd_list)


response = response / (response.max() + 1e-5)
threshold = 0.050
corners = np.argwhere(response > threshold)
print("Detected corners:", len(corners))


rgb_img = img.convert("RGB")
draw = ImageDraw.Draw(rgb_img)

for (x, y) in corners:
    r = 2
    draw.ellipse((y - r, x - r, y + r, x + r), outline="red", width=2)



rgb_img.show()
rgb_img.save('outputs\moravec_output.png')

print("Response max:", response.max())
print("Response mean:", np.mean(response))
print("Response min:", response.min())