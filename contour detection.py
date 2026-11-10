import sys

import numpy as np
from PIL import Image

"""
    Direction Reference:

                1
                |
                |
         2 <- - | - -> 0
                |
                |
                3
    """

def border_follow(img,current,direction,numbers,parent,border_type,border):
    numbers[0]+=1
    if img[current[0]][current[1]]>1: numbers[1]=img[current[0]][current[1]]
    parent.append(numbers[1])

    start=list(current)
    contour=[]
    contour.append(list(current))

    while True:
        save=None
        while True:
            next=list(current)
            if direction==0:
                next[0] -= 1
                direction=1
                if save==None:
                    save=[current[0],current[1]+1]
            elif direction==1:
                next[1] -= 1
                direction=2
            elif direction==2:
                next[0] += 1
                direction=3
            elif direction==3:
                next[1] += 1
                direction=0
            if img[next[0]][next[1]]!=0:
                break
        
        if save!=None and img[save[0]][save[1]]==0:
            img[current[0]][current[1]]=-numbers[0] # right
        elif img[current[0]][current[1]]==1:
            img[current[0]][current[1]]=numbers[0] # left

        current=list(next)
        direction += 2
        direction %= 4

        contour.append(list(current))
        if current==start:
            break

    border_type.append(border)
    if border_type[numbers[0]-2]==0:
        parent.append(parent[numbers[0]-2])
    elif img[start[0]][start[1]]!=1:
        numbers[1]=abs(img[start[0]][start[1]])
        
    return contour

def raster_scan(img):
    rows,cols=img.shape
    numbers=[1, 1] # NBD, LNBD
    contours=[]
    parent=[-1]
    border_type=[0]
    for i in range(1,rows-1):
        numbers[1]=0
        for j in range(1,cols-1):
            if img[i][j]==1 and img[i][j-1]==0:
                contours.append(border_follow(img,[i,j],1,numbers,parent,border_type,1))
                continue
            if img[i][j]>=1 and img[i][j+1]==0:
                contours.append(border_follow(img,[i,j],3,numbers,parent,border_type,0))
                continue
    return contours,parent,border_type

source=Image.open(sys.argv[1]).convert("L")
img=np.array(source)
img=(img>127).astype(np.int8)
contours,parent,border_type=raster_scan(img)
print(parent)
print(border_type)
contour_image=Image.new("L",source.size,0)
contour_pixels=contour_image.load()
for contour in contours:
    for row,column in contour:
        contour_pixels[column,row]=255

output_path=sys.argv[2]
contour_image.save(output_path)
print(f"Saved contour image to {output_path}")

