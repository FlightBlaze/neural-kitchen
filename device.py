import torch
import config
import os


os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

device = torch.device(config.TORCH_DEVICE_NAME)
