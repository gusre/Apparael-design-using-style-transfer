import numpy as np
import pandas as pd
import matplotlib,sklearn
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans
from PIL import ImageColor,Image

def get_colors(num_colors,style_num):
    img=cv2.imread('C:/Users/gunas/Music/Flask/figures/tmp/color.png')
    if(img is not None):
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(img.shape[1],img.shape[0])
    a,b=img.shape[0],img.shape[1]
    img=img.reshape((img.shape[1]*img.shape[0],3))
    kmeans=KMeans(n_clusters=int(num_colors))
    s=kmeans.fit(img)
    labels=kmeans.labels_
    print(labels,len(labels))
   
    labels=list(labels)
    centroid=kmeans.cluster_centers_
    colors=[]
    for color in centroid:
        color1=[int(x) for x in color]
        colors.append(color1)
    print(colors)
    for i in range(img.shape[0]):
        img[i][0]=colors[labels[i]][0]
        img[i][1]=colors[labels[i]][1]
        img[i][2]=colors[labels[i]][2]
    img=img.reshape(a,b,3)
    img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite('C:/Users/gunas/Music/Flask/figures/colored/style'+str(style_num)+'.png',img)
    return colors



def swap_colors(data):
    i=0
    print(data)
    for row in data:
        i+=1
        stylenum=row[0]
        colorchange={}
        for j in range(len(row[1])):
            if row[1][j]!=row[2][j]:
                colorchange[ImageColor.getcolor(row[1][j], "RGB")]=ImageColor.getcolor(row[2][j], "RGB")

        im1 = Image.open('./figures/colored/style'+str(stylenum)+'.png', 'r')
        im2= Image.open('./figures/style/file'+str(stylenum)+'.png', 'r')
        width, height = im1.size
        for y in range(0, height): #each pixel has coordinates
            for x in range(0, width):
                RGB = im1.getpixel((x,y))
                RGB1=colorchange.get(RGB)
                if RGB1 is not None: 
                    im2.putpixel((x,y),RGB1)
        im2.save('./figures/style/style'+str(stylenum)+'.png')


    return ''


