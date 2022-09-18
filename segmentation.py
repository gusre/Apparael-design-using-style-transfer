from pylab import imshow
import numpy as np
import cv2
import torch
import albumentations as albu
from matplotlib import pyplot as plt


from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image

from collections import namedtuple
from torch import nn
from torch.utils import model_zoo
from iglovikov_helper_functions.dl.pytorch.utils import rename_layers

from segmentation_models_pytorch import Unet

model = namedtuple("model", ["url", "model"])

models = {
    "Unet_2020-10-30": model(
        url="https://github.com/gusre/segmentation/releases/download/v.0.1.0/weights.zip",
        model=Unet(encoder_name="timm-efficientnet-b3", classes=1, encoder_weights=None),
    )
}


def create_model(model_name: str) -> nn.Module:
    model = models[model_name].model
    state_dict = model_zoo.load_url(models[model_name].url, progress=True, map_location="cpu")["state_dict"]
    state_dict = rename_layers(state_dict, {"model.": ""})
    model.load_state_dict(state_dict)
    return model

def getModel():
    model = create_model("Unet_2020-10-30")
    model.eval()
    return model


def get(model=getModel()):
  image = load_rgb("./figures/content/content.png")
  transform = albu.Compose([albu.Normalize(p=1)], p=1)
  padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)
  x = transform(image=padded_image)["image"]
  x = torch.unsqueeze(tensor_from_rgb_image(x), 0)
  with torch.no_grad():
    prediction = model(x)[0][0]
  mask = (prediction > 0).cpu().numpy().astype(np.uint8)
  mask = unpad(mask, pads)
  mask=cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) * 255
  plt.imsave('./figures/tmp/mask0.png',mask)




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



  
def segment2(a,mix):
  final = cv2.imread(a)
  final2 = final.copy() 
  for j in range(len(mix)):
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