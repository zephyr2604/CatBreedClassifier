import torch, torchvision, io
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

#Dictionary
Dict = {0: 'Abyssinian', 1: 'Bengal', 2: 'Birman', 3: 'Bombay', 4: 'British Shorthair', 5: 'Egyptian Mau', 
        6: 'Maine Coon', 7: 'Persian', 8: 'Ragdoll', 9: 'Russian Blue', 10: 'Siamese', 11: 'Sphynx'}


#load model
class Model(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, n_classes):
        super().__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu2 = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(hidden_dim // 2, n_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

model = torchvision.models.resnet50(pretrained=True)
model.fc = Model(2048, 1024, 12)

PATH="best_checkpoint.pth"
model.load_state_dict(torch.load(PATH))
model.eval()


#image -> tensor
def transform_image(image_bytes):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize(256),
        torchvision.transforms.CenterCrop(224),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)


#predict
def get_prediction(image_tensor):
    images = image_tensor
    #labels = valid_labels.to(device)
    with torch.no_grad():
        outputs = model(images)
    _,predicted = torch.max(outputs.data, 1)
    print(Dict[predicted.item()])
    return Dict[predicted.item()]