import logging
import numpy as np
import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer
from args import args






def test_bert(text, model_path):
	device = 'cuda' if args.use_gpu and torch.cuda.is_available else 'cpu'
	device = 'cpu'
	device = torch.device(device)

	#prepare the text for bert
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
	encoded_article = tokenizer.encode_plus(text, add_special_tokens=True, max_length=args.MAX_LEN,
                                                pad_to_max_length=True,
                                                return_attention_mask=True, return_tensors='pt')
	text_ids = torch.tensor(encoded_article['input_ids'])
	text_att_mask = torch.tensor(encoded_article['attention_mask'])

    #prepare the model
	model = load_model(model_path)
	text_ids.to(device)
	text_att_mask.to(device)
	model.to(device)
	model.eval()

    # forward pass
	with torch.no_grad():
		logits = model(text_ids, token_type_ids=None, attention_mask=text_att_mask)
	pred = logits[0].cpu().data.numpy()
	pred_class = np.argmax(pred, axis=1)#description=0 quality=1, planning=2, currentInfo=3, generalInfo=4
	return pred_class






def load_model(checkpoint_path):
	model = BertForSequenceClassification.from_pretrained(checkpoint_path, num_labels=args.num_label,
                                                          output_attentions=False, output_hidden_states=False)
	return model


