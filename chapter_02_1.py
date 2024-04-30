# pip install tiktoken

import tiktoken

encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

text = "This is a test for tiktoken."
tokens = encoding.encode(text)

print(text)
print(tokens)
print(encoding.decode(tokens))
