import openai
import json

def paraphrase(comment):
    messages=[{"role": "system", "content": "You are a helpful assistant."}]
    #message = input()
    message="Please paraphrase the following comment:" + comment 
    messages.append({"role": "user", "content": message}) 
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response = chat['choices'][0]['message']['content']
    return response

# Load the configuration from the JSON file
try:
    with open('chatgpt-key.json', 'r') as config_file:
        config = json.load(config_file)

except FileNotFoundError:
    print("Configuration file not found. Please create a 'config.json' file.")
    exit(1)

# Access the API key
openai.api_key = config.get("api_key")
