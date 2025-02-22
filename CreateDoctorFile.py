MEDICAL_DOCS_DIR = "medical_documents"
PRESCRIPTION_TEMPLATE = """PRESCRIPTION

Patient Name: {name}
Date: {date}

Medications:
{medications}

Instructions:
{instructions}

Doctor's Signature: AI Medical Assistant
(This is a simulated prescription for educational purposes only)"""

NOTE_TEMPLATE = """DOCTOR'S NOTE

Patient Name: {name}
Date: {date}

{content}

Recommendations:
{recommendations}
"""



def createPrescriptionFile(file_path, prescription, instructions):
    curFileTemplate = PRESCRIPTION_TEMPLATE.replace("{medications}", prescription)
    curFileTemplate = curFileTemplate.replace("{instructions}", instructions)
    with open(file_path, "a") as f:
        f.write(curFileTemplate)
        f.flush()
        f.close()

def createDocNoteFile(file_path, content, recommendations):
    curFileTemplate = NOTE_TEMPLATE.replace("{content}", content)
    curFileTemplate = curFileTemplate.replace("{recommendations}", recommendations)
    with open(file_path, "a") as f:
        f.write(curFileTemplate)
        f.flush()
        f.close()