import torch
import torchvision.transforms as transforms
import cv2
import matplotlib.pyplot as plt
from app.aws.bucket import *

from .network.Transformer import Transformer



from celery import Celery
from celery.result import AsyncResult
from celery.states import state, PENDING, SUCCESS


celery = Celery('backend',broker='amqp://guest@localhost:5672',backend ='redis://127.0.0.1:6379/0')
#'redis://localhost:6379/0'


@celery.task(ignore_result=False, task_ignore_result =False)
def ai(file):

    # model=Transformer()
    # model.load_state_dict(torch.load("C:/Users/syeon/Desktop/docker2/docker/backend/ai/pretrained_model/Paprika_net_G_float.pth"))
    # model.eval()
    print('Model loaded!')
    img_size=450

    img_path=file
    origin=file
    # img=cv2.imread(img_path)

    # T=transforms.Compose([
    #     transforms.ToPILImage(),
    #     transforms.Resize(img_size,2),
    #     transforms.ToTensor()
    # ])

    # img_input=T(img).unsqueeze(0)
    # img_input=-1+2*img_input

    # plt.figure(figsize=(16,10))
    # plt.imshow(img[:,:,::-1])

    # img_output=model(img_input)
    # img_output=(img_output.squeeze().detach().numpy()+1.)/2.
    # img_output=img_output.transpose([1,2,0])

    # plt.figure(figsize=(16,10))
    # plt.axis('off')
    # plt.imshow(img_output[:,:,::-1])


    # photo=models.UploadedPhoto(user_id=user,photo_name=filename,update_type=type, result_name=filename)
    # plt.savefig('savefig_default.png')
    
    #사진 db에 저장

    return "hi"