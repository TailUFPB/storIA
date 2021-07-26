import requests

API_URL = "https://api-inference.huggingface.co/models/Felipehonorato/storIA"
headers = {"Authorization": "Bearer api_CwzaLVoNBMVQhviuBtnxxdVoXvQgjuTEmW"}

def remove_token(text):
  return " ".join(text.split()[1:])

def check_token(input):
  token = '<|startoftext|> '
  if input.split()[0] != token:
    return token + input
  else:
    return input

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

input = 'it was a dark night' # TEXTO DO USUÁRIO
input_len = len(input.split())
size = 50 # DEFINIDO PELO USUÁRIO DEFAULT 50
input = check_token(input)
output = query({"inputs": input,
                "parameters": {"max_length": 50, 'repetition_penalty': float(1.2), 'num_beams':5,
                               'no_repeat_ngram_size':3, 'max_length':input_len + size}})