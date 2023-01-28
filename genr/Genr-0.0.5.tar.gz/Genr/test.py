import genr


#With default parameters

api_key = "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"
openai = genr.OpenAI(api_key)
text = "OpenAI is an artificial intelligence research laboratory consisting of the for-profit OpenAI LP and its parent company, the non-profit OpenAI Inc. The company is dedicated to promoting and developing friendly AI in a way that benefits humanity as a whole."
summary = openai.summarize(text, model="text-davinci-003", temperature=1)
print(summary)

#With additional parameters

# api_key = "<API-KEY>"
# openai = OpenAIWrapper(api_key)
# text = "OpenAI is an artificial intelligence research laboratory consisting of the for-profit OpenAI LP and its parent company, the non-profit OpenAI Inc. The company is dedicated to promoting and developing friendly AI in a way that benefits humanity as a whole."
# summary = openai.get_summary(text, temperature=0.7, max_tokens=120, model="text-davinci-003")
# print(text)