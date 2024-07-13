from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-kHGp5": {},
  "Prompt-YeOlW": {},
  "ChatOutput-vavIB": {},
  "GroqModel-7lXUs": {}
}

result = run_flow_from_json(flow="jsonfiles/Basic_Prompting.json",
                            input_value="hello",
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)

print(result)