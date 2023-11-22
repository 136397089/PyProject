from torchvision import models

dir(moudels)

alexnet=models.AlexNet()
resnet=models.resnet101(pretrained=True)


from torchvision import transforms
preprocess=transforms.Compose([transforms.Resize(256),
                              transforms.CenterCrop(224),
                              transforms.ToTensor(),
                              transforms.Normalize(
                                  mean=[0.485,0.456,0.406],
                                  std=[0.229,0.224,0.225]
                              )])


from PIL import Image
img = Image.open("E:\\__GitCodeData\\9_PyProject\\机器学习\\pytorch\\Demo\\wKgAFFUvWymAJUHFAATzeWkJ5kw259.jpg")
# img.show()
img_t=preprocess(img)
import torch
batch_t=torch.unsqueeze(img_t,0)

resnet.eval()
out=resnet(batch_t)

with open('E:\\__GitCodeData\\9_PyProject\\机器学习\\pytorch\\Demo\\imagenet_classes.txt') as f:
    labels=[line.strip() for line in f.readlines()]

_,index = torch.max(out,1)
percentage=torch.nn.functional.softmax(out, dim=1)[0]*100
labels[index[0]],percentage[index[0]].item()

_,indices=torch.sort(out,descending=True)
a = [(labels[idx], percentage[idx].item()) for idx in indices[0][:5]]

