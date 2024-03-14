import numpy as np

from src.components.llm import LLM

llm_ = LLM(logits_all=True, logprobs=True)
llm = llm_.load_model()

query = 'What types of dependencies does dependence analysis identify in loop programs?'
response = llm.invoke(query)

outs = llm.client(query, **llm._get_parameters())
ppl = np.exp(-1 * np.mean(outs['choices'][0]['logprobs']['token_logprobs']))
print("Perplexity: {}".format(ppl))
