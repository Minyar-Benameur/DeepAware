import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

pay = """
        CREATE YOUR PROMPT HERE
"""

conversation = [{"role": "system", "content": "Starting the conversation"}]

# Start the conversation loop
def get_response():

    # User input
    sens_of_urgency = input("Sense of urgency : ")
    victim_name = input("Victim name : ")
    company = input("Company name : ")
    position = input("Position  : ")
    topic = input("Topic : ")
    link_name = "www."+company+"/contact-us.com"

    sender = input("Sender name : ")
    user_input = "Create professional and convincing phishing emails structured and well-detailed using the following information about the target: name " + victim_name + ", sense of urgency " + sens_of_urgency + ", company " + company +", position " + position +", topic "+ topic +", sender name "+ sender +" link name "+ link_name
    
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

    return ai_response

get_response()