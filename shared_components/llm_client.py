from litellm import completion
import os
from dotenv import load_dotenv
## set ENV variables
load_dotenv()

os.environ['DEEPSEEK_API_KEY'] 
deepseek_model = completion(
    model="deepseek/deepseek-chat", 
)

openai_model = completion(
  model="openai/gpt-4o",
)

claude_model = completion(
  model="anthropic/claude-3-sonnet-20240229",
)

