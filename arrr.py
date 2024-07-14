import time
from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-zGbmw": {},
  "Prompt-OepaV": {},
  "ChatOutput-xHfKI": {},
  "PythonFunction-dLZXz": {}
}

result = run_flow_from_json(flow="AIMLChatBot.json",
                            input_value="hello",
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)




print(result)