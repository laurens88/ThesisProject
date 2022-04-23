import tensorflow as tf
from transformers import BertTokenizer, BertModel

MAX_LEN = 256
TRAIN_BATCH_SIZE = 32
VALID_BATCH_SIZE = 32
EPOCHS = 2
LEARNING_RATE = 1e-05

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")





