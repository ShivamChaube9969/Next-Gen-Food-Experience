import openai
# For the UI
from flask import Flask, render_template, request, session


# Create a new Flask app
app = Flask(__name__)
app.secret_key = "mysecretkey"


openai.api_key = open("C:/Users/Shivam/PythonVSCode/key.txt","r").read().strip("\n")

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

    # Setting the context
    session['message_history'] = [{"role": "user", "content": """
    You are OrderBot, an automated service to collect orders for a restaurant. You will provide a list of 20 ingredients that the user will choose from.
    When you present the ingredients, present the ingredients with a greeting message and start immediately with the ingredients, no further commentary, and then ingredients like "1:" "2:" ...etc. If you understand, say, OK, and begin when I say "begin." """},{"role": "assistant", "content": """
    OK, I understand. Begin when you're ready."""}]

    # Retrieve the message history from the session
    message_history = session['message_history']

    # Generate a chat response with an initial message ("Begin")
    reply_content, message_history = chat("Begin", message_history)
    print(reply_content.content)

    # Render the index.html file and pass in the message history
    return render_template("index.html", message=reply_content.content)


# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")

    # Retrieve the message history and button messages from the session
    message_history = session['message_history']

    # Send the message to OpenAI's API and receive the response
    reply_content, message_history = chat(message, message_history)
    
    if reply_content!=None:
        return reply_content

    else :
        return 'Failed to Generate response!'
    

if __name__=='__main__':
    app.run()