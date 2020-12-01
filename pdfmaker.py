#script for classkick
from PIL import Image
import os
import sys

# deal with filepaths so the terminal does its thing in the right place
path, pdfname = sys.argv[1:]
os.chdir(path)

#extract the trash ppm
for pdf in [i for i in os.listdir(path) if i.endswith(".pdf")]:
    os.system(f'pdfimages "{path}/{pdf}" image')
os.system(f'mkdir {path}/processed')
for fn in sorted([i for i in os.listdir(path) if i.endswith(".ppm")]):
    os.system(f"pnmcrop -black {path}/{fn} > {path}/processed/{fn[:-3]}.png") #take out annoying black thing

os.system(f"rm {path}/*.ppm")

#take the images, process(remove black garbage) and put into pdf
images = [Image.open(f"{path}/processed/{fn}").convert('RGB') for fn in sorted([i for i in os.listdir(path+"/processed") if i.endswith(".png")])][::2]

processed = []
for im in images:
    #get A4 or make it a bit bigger so it fits whatever squashed in the side
    h = max(1265, im.size[1])
    if h != 1265:
        h+=50
    w = max(903, im.size[0])
    a4im = Image.new('RGB', #make A4 page
                    (w, h),   # hopefully size stays the same
                    (255, 255, 255))  # White
    width, height = im.size
    pixdata = im.load()
    for y in range(im.size[1]): #attempt to fix black thing
        for x in range(im.size[0]):
            if pixdata[x, y] == (0, 0, 0):
                pixdata[x, y] = (255, 255, 255)
    a4im.paste(im, ((w-width)//2, (h-height)//2))  #slap image on a4 and center
    processed.append(a4im)
    
processed[0].save(pdfname, save_all=True, append_images=processed[1:])
os.system("rm *.ppm")
os.system("rm -r processed")

#links
#https://stackoverflow.com/questions/27271138/python-pil-pillow-pad-image-to-desired-size-eg-a4?rq=1
#probably more but i can't rmb