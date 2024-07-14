from langflow.load import run_flow_from_json
TWEAKS = {
  "Prompt-LjR1d": {},
  "ChatOutput-iyAtB": {},
  "OpenAIModel-FtYGt": {},
  "ChatInput-49meU": {}
}

result = run_flow_from_json(flow="AnalyseImage.json",
                            input_value="https://i.postimg.cc/j53cf6fM/pizza.jpg",
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)



print(result[0].outputs[0].results['message'].text)