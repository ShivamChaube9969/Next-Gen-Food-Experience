import openai
# For the UI
from flask import Flask, render_template, request


# Create a new Flask app
app = Flask(__name__)


openai.api_key = open("C:/Users/Shivam/PythonVSCode/Next-Gen-Food-Experience/key.txt","r").read().strip("\n")

def chat(inp, message_history, role="user"):

    # Append the input message to the message history
    message_history.append({"role": role, "content": f"{inp}"})

    # Generate a chat response using the OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature = 0
    )

    # Grab just the text from the API completion response
    reply_content = completion.choices[0].message

    # Append the generated response to the message history
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # Return the generated response and the updated message history
    return reply_content, message_history


# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():

    # Setting the context
    message_history = [{"role": "user", "content": """
    You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collects the order, \
    You will provide list of 20 random ingredients to the user, \
    
    
    """}]


# """You are a friendly food assistant chatbot that interacts with customers to take their food orders but not in a conventional way. You will provide list of 20 random ingredients from which the customer will pick 5 top ingredients. Wait for the If you understand, say, OK, and begin when I say "begin." """
#Then you will ask the customer how many recipes he wants you to generate based on the given response you will generate those many recipes and make sure these recipes includes the ingedrients mentioned by the customer earlier.
# ,{"role": "assistant", "content": f"""OK, I understand. Begin when you're ready."""}

    # Generate a chat response with an initial message ("Begin")
    reply_content, message_history = chat("Begin", message_history)

    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    reply_content, message_history = chat(message, message_history)
    
    if reply_content!=None:
        return reply_content

    else :
        return 'Failed to Generate response!'
    

if __name__=='__main__':
    app.run()