import numpy as np
import torch

class EarlyStopping:
    """早停法来防止过拟合"""
    def __init__(self, patience=7, verbose=False, delta=0):
        """
        Args:
            patience (int): 性能没有改善后等待的轮次数，之后训练将会被停止。
            verbose (bool): 如果为True，则打印一条信息每当检测到性能的提升。
            delta (float): 最小的改变量，被认为是性能提升。
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model):
        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'早停法计数: {self.counter}/{self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        '''保存模型当验证损失减少时'''
        if self.verbose:
            print(f'验证损失减少 ({self.val_loss_min:.6f} --> {val_loss:.6f}).  保存模型...')
        torch.save(model.state_dict(), 'checkpoint.pt')
        self.val_loss_min = val_loss
