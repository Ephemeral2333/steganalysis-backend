import torch
from model.SRNet_CBAM import Model
from torchvision import transforms

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = Model().to(device)
pre_trained_srnet_path = 'D:\File\Graduation Design\Code\steganalysis_backend\model\pretrained_model\models.pt'

# Load pretrained model
if pre_trained_srnet_path is not None:
    model.load_state_dict(torch.load(pre_trained_srnet_path))
else:
    print('No pre-trained model path provided.')
    exit()

# Define transform
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
])


def predict(image):
    image = transform(image).unsqueeze(0).to(device)
    # Predict
    model.eval()
    with torch.no_grad():
        outputs = model(image)
        prediction = outputs.data.max(1)[1]

    return prediction.item()


if __name__ == '__main__':
    print(torch.cuda.is_available())
