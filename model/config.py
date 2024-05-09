mode = 'train'  # train or test
epochs = 50
lr = 2e-4
weight_decay = 1e-5
gamma = 0.5
weight_decay_step = 15

train_batch_size = 16
val_batch_size = 16
test_batch_size = 4
save_freq = 2
val_freq = 2
start_save_epoch = 2
stego_img_height = 256  # stego_img_height == stego_img_width 长宽
stego_img_channel = 3  # 彩色3 灰色1