import torch
import os
import logging
import numpy as np
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from tqdm import tqdm
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import torchvision.transforms as T
from model.SRNet_CBAM import Model
from utils.terminal import MetricMonitor

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = Model().to(device)
pre_trained_srnet_path = 'D:\File\Graduation Design\Code\steganalysis_backend\model\pretrained_model\models.pt'

# Load pretrained model
if pre_trained_srnet_path is not None:
    model.load_state_dict(torch.load(pre_trained_srnet_path))
else:
    print('No pre-trained model path provided.')
    exit()

transform_val_or_test = T.Compose([
    T.ToTensor(),
])


def get_test_loader(data_dir, batch_size):
    test_sets = ImageFolder(root=data_dir, transform=transform_val_or_test)
    test_loader = DataLoader(test_sets, batch_size=batch_size, shuffle=False, num_workers=2, drop_last=False)
    return test_loader


def test_model(test_path):
    test_loader = get_test_loader(test_path, 4)
    all_preds = []
    all_labels = []

    model.eval()
    metric_monitor = MetricMonitor(float_precision=4)
    stream = tqdm(test_loader)

    with torch.no_grad():
        for batch_idx, (inputs, labels) in enumerate(stream):
            inputs = inputs.to(device, dtype=torch.float)
            labels = labels.to(device, dtype=torch.long)

            outputs = model(inputs)
            prediction = outputs.data.max(1)[1]

            all_preds.extend(prediction.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

            accuracy = (prediction.eq(labels.data).sum() * 100.0 / labels.size()[0])
            metric_monitor.update("ACC", accuracy)

    precision, recall, f1_score, _ = precision_recall_fscore_support(all_labels, all_preds, average='macro')

    # 计算混淆矩阵
    conf_matrix = confusion_matrix(all_labels, all_preds)
    TP = conf_matrix[1, 1]
    TN = conf_matrix[0, 0]
    FP = conf_matrix[0, 1]
    FN = conf_matrix[1, 0]
    accuracy = (TP + TN) / (TP + TN + FP + FN)

    # 将数据保留到小数点后两位
    precision = round(precision, 2)
    recall = round(recall, 2)
    f1_score = round(f1_score, 2)
    accuracy = round(accuracy, 2)

    return precision, recall, f1_score, accuracy
