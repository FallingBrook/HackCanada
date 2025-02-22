from cgi import print_environ_usage

import requests
import os
import CreateDoctorFile

API_KEY = "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"
url = "https://api.perplexity.ai/chat/completions"

# Configuration constants
HISTORY_FILE = "therapy_history.txt"
DOCTOR_HISTORY_FILE = "doctor_history.txt"
MAX_HISTORY_LENGTH = 5
CRISIS_KEYWORDS = {"suicide", "kill", "harm", "abuse", "emergency"}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# System prompts
THERAPIST_SYSTEM_PROMPT = """You are a compassionate therapist using evidence-based techniques. Follow these guidelines:

1. Validate emotions: "I hear that [emotion] is coming up strongly"
2. Ask open questions: "What's underneath that feeling?"
3. Reframe perspectives: "How might this look differently?"
4. Never diagnose - encourage professional care

Conversation history:
{history}

New patient message:"""

DOCTOR_SYSTEM_PROMPT = """You are an AI medical assistant providing general health information. Follow these guidelines:

1. Suggest medecines and prescriptions if applicable
2. Make sure the medecines and prescriptions are well research and widely known
2. Suggest consulting a healthcare professional only in severe cases
3. Provide evidence-based information
4. Flag emergencies: "This sounds serious - please seek immediate care"
5. Dont include citations
6. If a prescription is applicable end your message with: "P: (medicine name)" Only suggest one medicine
7. If a doctors note is applicable end your message with: "N: (injury)" Only say one injury
8. Before you write the prescription or doctors note write: "***". Have no space between prescription and medicine

Medical conversation history:
{history}

New health query:"""


def load_history(file_path):
    """Load conversation history from specified file"""
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        lines = f.readlines()

    history = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            role = "Therapist" if "therapy" in file_path else "Doctor"
            history.append({
                "user": lines[i].strip().replace("User: ", ""),
                "response": lines[i + 1].strip().replace(f"{role}: ", "")
            })
    return history[-MAX_HISTORY_LENGTH:]


def save_interaction(file_path, user_input, response):
    """Save interaction to specified history file"""
    with open(file_path, "a") as f:
        f.write(f"User: {user_input}\n")
        role = "Therapist" if "therapy" in file_path else "Doctor"
        f.write(f"{role}: {response}\n")

def checkCreateFile(text):
    medicine = ""
    injury = ""
    print(text)
    if(len(text) <= 1):
        return None
    res = text.splitlines(False)
    res.remove("")

    print(res)

    if len(res) == 2:
        res[0] = res[0][3:]
        medicine = res[0]

        res[1] = res[1][3:]
        injury = res[1]
    elif(len(res) == 1):
        if(res[0][:2] == "P:"):
            res[0] = res[0][3:]
            medicine = res[0]
        elif(res[1][:2] == "N:"):
            res[1] = res[1][3:]
            injury = res[1]



    print(medicine + "sdasd")
    print(injury + "sdad")
    if medicine != "":
        createPrescription(medicine)
        print("MEDIDID")
    if injury != "":
        createDocNote(injury)
        print("DOCODOCDOC/")



def GetAiTherapistResp(question):
    # Crisis response
    if any(keyword in question.lower() for keyword in CRISIS_KEYWORDS):
        crisis_response = "Your safety matters. Immediate support: National Crisis Hotline 1-800-273-8255"
        save_interaction(HISTORY_FILE, question, crisis_response)
        return crisis_response

    # Load and format history
    history = load_history(HISTORY_FILE)
    history_context = "\n".join(
        [f"Patient: {h['user']}\nTherapist: {h['response']}"
         for h in history]
    )

    # API call
    messages = [
        {"role": "system", "content": THERAPIST_SYSTEM_PROMPT.format(history=history_context)},
        {"role": "user", "content": question}
    ]

    response = requests.post(url, json={
        "model": "sonar-pro",
        "messages": messages,
        "temperature": 0.7
    }, headers=headers)

    if response.status_code == 200:
        therapist_response = response.json()["choices"][0]["message"]["content"]
        save_interaction(HISTORY_FILE, question, therapist_response)
        return therapist_response
    else:
        print(f"Therapist Error: {response.status_code}")
        return None


def GetAiDoctorResp(question):
    # Medical emergency check
    if any(keyword in question.lower() for keyword in CRISIS_KEYWORDS):
        crisis_response = "This sounds urgent. Please seek immediate medical care or call 911."
        save_interaction(DOCTOR_HISTORY_FILE, question, crisis_response)
        return crisis_response

    # Load and format history
    history = load_history(DOCTOR_HISTORY_FILE)
    history_context = "\n".join(
        [f"Patient: {h['user']}\nDoctor: {h['response']}"
         for h in history]
    )

    # API call
    messages = [
        {"role": "system", "content": DOCTOR_SYSTEM_PROMPT.format(history=history_context)},
        {"role": "user", "content": question}
    ]

    response = requests.post(url, json={
        "model": "sonar-pro",
        "messages": messages,
        "temperature": 0.7
    }, headers=headers)

    if response.status_code == 200:
        text = response.json()["choices"][0]["message"]["content"]
        save_interaction(DOCTOR_HISTORY_FILE, question, text)
        doctor_response = text.split("***")
        checkCreateFile(doctor_response[1])
        return doctor_response[0]
    else:
        print(f"Doctor Error: {response.status_code}")
        return None



def createPrescription(prescription):

    prompt = "Create instructions for the following prescription: " + prescription

    response = requests.post(url, json={
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }, headers=headers)

    if response.status_code == 200:
        doctor_response = response.json()["choices"][0]["message"]["content"]
        CreateDoctorFile.createPrescriptionFile(prescription + "-prescription.txt", prescription, doctor_response)
    else:
        print(f"Doctor Error: {response.status_code}")
        return None

def createDocNote(injury):

    contentPrompt = ("Create the content of a doctors letter for the following injury."
                     "Ensure its only the main body text and does not include date or anything."
                     "Ensure it does not include recommendations") + injury

    recPrompt = ("Your writing a doctors note and you are outlining the recommendations"
                 "of how to deal with the following inury."
                 "Ensure the output only includes recommendations and no other part of the letter") + injury
    content = ""
    recommendations = ""

    response = requests.post(url, json={
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": contentPrompt}],
        "temperature": 0.7
    }, headers=headers)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Doctor Error: {response.status_code}")
        return None

    response = requests.post(url, json={
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": recPrompt}],
        "temperature": 0.7
    }, headers=headers)

    if response.status_code == 200:
        recommendations = response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Doctor Error: {response.status_code}")
        return None

    CreateDoctorFile.createDocNoteFile(injury.replace(" ", "-") + "-doc-note.txt", content, recommendations)
def main_loop():
    print("""\nAI Assistant System
---------------------------------
- Type your message for emotional support
- Start messages with '/doctor' for medical questions
- Type 'quit' to exit
---------------------------------""")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ('quit', 'exit'):
                print("\nThank you for using our service. Take care!")
                break

            if user_input.lower().startswith('/doctor'):
                question = user_input[7:].strip()
                if not question:
                    print("Please enter a medical question after '/doctor'")
                    continue
                response = GetAiDoctorResp(question)
            else:
                response = GetAiTherapistResp(user_input)

            if response:
                print(f"\nAssistant: {response}")
            else:
                print("Error generating response. Please try again.")

        except KeyboardInterrupt:
            print("\n\nSession ended unexpectedly. Your history has been saved.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main_loop()