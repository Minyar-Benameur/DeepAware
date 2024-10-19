import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

pay = """
    CREATE YOUR PROMPT HERE
"""

# Define an initial message

conversation = [{"role": "system", "content": f"\n\n {pay}"}]

# Start the conversation loop

# User input
full_name = input("Full name: ")
email = input("Email address: ")
age = input("Age: ")
company = input("Company name: ")
position = input("Position: ")
topic = input("Topic: ")

user_input = "Create phishing scenarios based on social engineering using this information about the target: Full name " + full_name +"Email address " + email +"Age" + age +" Company name " + company +"Position " +position +"Topic " +topic
    
# Add user input to the conversation
conversation.append({"role": "user", "content": user_input})
    
# Call the chat endpoint with the conversation so far
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Specify a valid model
    messages=conversation
)
    
# AI's response
ai_response = response['choices'][0]['message']['content'].strip()
print("HackerGPT:", ai_response)
    
# Add AI's response to the conversation
conversation.append({"role": "assistant", "content": ai_response})
