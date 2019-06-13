import numpy as np
import ast
# four-connected case
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
def next_cell(curr_pixel,curr_dir):
    i,j=curr_pixel
    save=None
    if curr_dir==0:
        r=i-1
        c=j
        new_dir=1
        save=[i,j+1]
    elif curr_dir==1:
        r=i
        c=j-1
        new_dir=2
    elif curr_dir==2:
        r=i+1
        c=j
        new_dir=3
    elif curr_dir==3:
        r=i
        c=j+1
        new_dir=0
    return r,c,new_dir,save

def border_follow(img,start,prev,direction,NBD):
    curr=list(start)
    exam=list(prev)
    save=None
    save2=list(exam)
    contour=[]
    contour.append(list(curr))
    while img[exam[0]][exam[1]]==0:
        exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
        if save_pixel!=None:
            save=list(save_pixel)
        if save2==exam:
            img[curr[0],curr[1]]=-NBD
            return contour
    if save!=None:
        img[curr[0]][curr[1]]=-NBD
        save=None
    elif (save==None or (save!=None and img[save[0]][save[1]]!=0)) and img[curr[0]][curr[1]]==1: img[curr[0]][curr[1]]=NBD
    else: pass
    prev=list(curr)
    curr=list(exam)
    contour.append(list(curr))
    if direction>=2: direction=direction-2
    else: direction=2+direction
    flag=0
    start_next=list(curr)
    while True:
        if not(curr==start_next and prev==start and flag==1):
            flag=1
            exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
            if save_pixel!=None:
                save=list(save_pixel)
            while img[exam[0]][exam[1]]==0:
                exam[0],exam[1],direction,save_pixel=next_cell(curr,direction)
                if save_pixel!=None:
                    save=list(save_pixel)
            if save!=None and img[save[0]][save[1]]==0:
                img[curr[0]][curr[1]]=-NBD
                save=None
            elif (save==None or (save!=None and img[save[0]][save[1]]!=0)) and img[curr[0]][curr[1]]==1: img[curr[0]][curr[1]]=NBD
            else: pass
            prev=list(curr)
            curr=list(exam)
            contour.append(list(curr))
            if direction>=2: direction=direction-2
            else: direction=2+direction
        else:
            break
    return contour
        
def raster_scan(img):
    rows,cols=img.shape
    LNBD=1
    NBD=1
    contours=[]
    parent=[]
    parent.append(-1)
    border_type=[]
    border_type.append(0)
    for i in range(1,rows-1):
        LNBD=1
        for j in range(1,cols-1):
            if img[i][j]==1 and img[i][j-1]==0:
                NBD+=1
                direction=2
                parent.append(LNBD) 
                contour=border_follow(img,[i,j],[i,j-1],direction,NBD)
                contours.append(contour)
                border_type.append(1)
                if border_type[NBD-2]==1: parent.append(parent[NBD-2])
                else:
                    if img[i][j]!=1: LNBD=abs(img[i][j])              
            elif img[i][j]>=1 and img[i][j+1]==0:
                NBD+=1
                direction=0
                if img[i][j]>1: LNBD=img[i][j]
                parent.append(LNBD)
                contour=border_follow(img,[i,j],[i,j+1],direction,NBD)
                contours.append(contour)
                border_type.append(0)
                if border_type[NBD-2]==0: parent.append(parent[NBD-2])
                else:
                    if img[i][j]!=1: LNBD=abs(img[i][j])
    return contours,parent,border_type

img=np.array(ast.literal_eval(input()))
contours,parent,border_type=raster_scan(img)
print(contours)
print(parent)
print(border_type)
