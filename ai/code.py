import torch
import torchvision.transforms as transforms
import cv2
import matplotlib.pyplot as plt
from app.aws.bucket import *

# from .network.Transformer import Transformer



# from celery import Celery
# from celery.result import AsyncResult
# from celery.states import state, PENDING, SUCCESS

from .network.Transformer import Transformer
from pathlib import Path
from fastapi.responses import FileResponse
import io
import os



def picture(image):
    # currentpath=os.getcwd()
    # print(currentpath)
    # print("ai함수 진입 성공 ")
    buf = io.BytesIO()
    model=Transformer()
    model.load_state_dict(torch.load('./ai/pretrained_model/Paprika_net_G_float.pth'))
    model.eval()
    
    print('Model loaded!')
    img_size=450
    img_path=image
    img=cv2.imread(img_path)

    T=transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(img_size,),
        transforms.ToTensor()
    ])

    img_input=T(img).unsqueeze(0)
    img_input=-1+2*img_input

    # plt.figure(figsize=(16,10))
    # plt.imshow(img[:,:,::-1])

    img_output=model(img_input)
    img_output=(img_output.squeeze().detach().numpy()+1.)/2.
    img_output=img_output.transpose([1,2,0])
    plt.figure(figsize=(16,10))
    # plt.axis('off')
    
    ax = plt.gca()

#hide x-axis
    ax.get_xaxis().set_visible(False)

#hide y-axis 
    ax.get_yaxis().set_visible(False)
    # plt.alt.get_xaxis().set_visible(False)
    # plt.axes.get_yaxis().set_visible(False)
    ax.grid(False)
    
    plt.imshow(img_output[:,:,::-1])

    plt.savefig('savefig_default.png',bbox_inches='tight',pad_inches=0,transparent=True)
    
    #plt.savefig('savefig_default.png')  

    # plt.savefig('savefig_default.png',transparent=True) 

    return img_output