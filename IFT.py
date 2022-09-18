import tensorflow as tf
import numpy as np
from utils.model import EncDec
from utils import seg_utils
from matplotlib import pyplot as plt
from PIL import Image
import os, cv2
from segmentation import *






def load_img(file,scale=1):
    img = np.asarray(Image.open(file))
    print(img.shape[1],img.shape[0])
    img = np.expand_dims(cv2.resize(img, (int(img.shape[1]*scale) // 8 * 8,int(img.shape[0]*scale) // 8 * 8)), axis=0) / 255
    return img


def iter_kargs(n_iter=[20,20,20,20], lr=[0.001]*4, lamb=[1e4, 2.5e3, 2.5e2, 2.5e1]): 
    return {
            0: {'lr':lr[0], 'lamb':lamb[0], 'n_iter':n_iter[0]},
            1: {'lr':lr[1], 'lamb':lamb[1], 'n_iter':n_iter[1]},
            2: {'lr':lr[2], 'lamb':lamb[2], 'n_iter':n_iter[2]},
            3: {'lr':lr[3], 'lamb':lamb[3], 'n_iter':n_iter[3]}
           }



def original_colors(a1,b1):
    content=Image.open(a1)
    generated=Image.open(b1)
    content_channels = list(content.convert('YCbCr').split())
    generated_channels = list(generated.convert('YCbCr').split())
    content_channels[0] = generated_channels[0]
    return Image.merge('YCbCr', content_channels).convert('RGB')

def initModel():
    enc_dec = EncDec()
    ckpt = tf.train.Checkpoint(net=enc_dec)
    x = load_img('./figures/content/ship.png')
    outputs = enc_dec(x)
    ckpt.restore('./ckpt/ckpt')
    return enc_dec


def settt(a,number_of_areas):
  final = cv2.imread(a)
  final2 = final.copy() 
  for j in range(number_of_areas):
    b='./figures/tmp/mask{}.png'.format(str(j+1))
    c='./figures/tmp/area{}.png'.format(str(j+1))
    mask = cv2.imread(b)
    res=cv2.imread(c)
    #--- Resizing the logo to the shape of room image ---
    mask = cv2.resize(mask, (final.shape[1], final.shape[0]))
    res=cv2.resize(res, (final.shape[1], final.shape[0]))
    #--- Apply Otsu threshold to blue channel of the logo image ---
    ret, logo_mask = cv2.threshold(mask[:,:,0], 0, 255, cv2.THRESH_BINARY)
    final2[np.where(logo_mask !=0)] = res[np.where(logo_mask!= 0)]
  return final2

def setfinal(a,number_of_areas):
  final = cv2.imread(a)
  final2 = final.copy() 
  for j in range(number_of_areas):
    b='./figures/tmp/mask{}.png'.format(str(j))
    c='./figures/tmp/area{}.png'.format(str(j))
    mask = cv2.imread(b)
    res=cv2.imread(c)
    #--- Resizing the logo to the shape of room image ---
    mask = cv2.resize(mask, (final.shape[1], final.shape[0]))
    res=cv2.resize(res, (final.shape[1], final.shape[0]))
    #--- Apply Otsu threshold to blue channel of the logo image ---
    ret, logo_mask = cv2.threshold(mask[:,:,0], 0, 255, cv2.THRESH_BINARY)
    final2[np.where(logo_mask !=0)] = res[np.where(logo_mask!= 0)]
  return final2

def ST(cont_img,style_img,weight,enc_dec):
  for i in range(2):
        if i == 0:
          stylized= enc_dec.stylize(cont_img, style_img,weights=weight,enc_layers={0:'iter', 1:'iter', 2:'iter', 3:'iter'}, dec_layers={0:'iter', 1:'iter', 2:'iter', 3:'iter'},iter_kargs=iter_kargs())
        else:
          stylized= enc_dec.stylize(stylized, style_img,weights=weight,enc_layers={0:'iter', 1:'iter', 2:'iter', 3:'iter'}, dec_layers={0:'iter', 1:'iter', 2:'iter', 3:'iter'},iter_kargs=iter_kargs())
        return stylized

def style_transfer(mode,color,blendormix,number_of_areas,number_of_styles,style_scale):
    enc_dec=initModel()
    cont_img=load_img('./figures/content/content.png')
    style_img=[]
    print(number_of_styles)
    if ',' in style_scale:
      style_scale=style_scale.split(',')
    style_scale=[float(x) for x in style_scale]
    for j in range(number_of_styles):
      style=load_img('./figures/style/style{}.png'.format(str(j+1)),style_scale[j])
      style_img.append(style)
    if mode=="1":
      for i in range(number_of_areas):
        style=blendormix[i][0]
        weight=blendormix[i][1]
        if ',' in style:
          style=style.split(',')
        if ',' in weight:
          weight=weight.split(',')
        style=[int(x) for x in style]
        weight=[int(x) for x in weight]
        print(style,weight)
        print(style,weight)
        styles=[style_img[x-1] for x in style]
        stylized=ST(cont_img,styles,weight,enc_dec)
        plt.imsave('./figures/tmp/area'+str(i+1)+'.png',np.clip(stylized[0], 0, 1))

      result=settt('./figures/content/content.png',number_of_areas)
      cv2.imwrite('./figures/tmp/area0.png',result)
      get()
      result=setfinal('./figures/content/content.png',1)
      cv2.imwrite('./figures/tmp/result.png',result)
    elif mode=="2":
      for i in range(number_of_styles):
        style=blendormix[i]
        if ',' in style:
          style=style.split(',')
        style=[int(x) for x in style]
        result=segment2('./figures/content/content.png',number_of_styles)
        cv2.imwrite('./figures/tmp/area0.png',result)
        result=settt('./figures/content/content.png',1)
        cv2.imwrite('./figures/tmp/result.png',result)
    if color=="1":
      res=original_colors('./figures/content/content.png','./figures/tmp/result.png')
      cv2.imwrite('./figures/tmp/result.png',res)