import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from PIL import Image
import docx
import fitz
import pytesseract

# Linux Tesseract Path for Render (NO WINDOWS PATHS!)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load env variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq Model
chat = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.4,
)

# Chat history
chat_history = [SystemMessage(content="You are a helpful HR chatbot assistant.")]
file_knowledge = ""

# ---------------------------------------------
# EMPLOYEE DATA
# ---------------------------------------------
employees = [
    {"emp_id": 101, "emp_name": "Ravi",    "emp_dob": "15-01-1990", "emp_email":"ravi123@gmail.com", "phone":9865432157, "emp_address": "No:77 Mayors Street, Coimbatore"},
    {"emp_id": 102, "emp_name": "Guru",    "emp_dob": "14-07-2005", "emp_email":"guru147@gmail.com", "phone":8964332156, "emp_address": "No:14 Gandhi Street, Chennai"},
    {"emp_id": 103, "emp_name": "Ram",     "emp_dob": "12-08-1992", "emp_email":"ram132@gmail.com", "phone":7685432167, "emp_address": "No:8 Bakers Street, Bangalore"},
    {"emp_id": 104, "emp_name": "Raja",    "emp_dob": "11-10-1999", "emp_email":"raja234@gmail.com", "phone":9665433187, "emp_address": "No:10 J.P Nagar, Trichy"},
    {"emp_id": 105, "emp_name": "Amirtha", "emp_dob": "05-09-1992", "emp_email":"amirtha987@gmail.com", "phone":9855544217, "emp_address": "No:6 Nehru Street, Hyderabad"}
]

# OCR Helpers
def extract_text_from_pdf(upload_path):
    doc = fitz.open(upload_path)
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(upload_path):
    document = docx.Document(upload_path)
    return "\n".join([p.text for p in document.paragraphs])

def extract_text_from_image(upload_path):
    try:
        image = Image.open(upload_path)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "[No visible text detected]"
    except Exception as e:
        return f"[Image processing failed: {e}]"

# Main Chat Response
def get_chat_response(user_msg):
    global chat_history, file_knowledge

    chat_history.append(HumanMessage(content=user_msg))
    lower_msg = user_msg.lower()

    # Employee list
    if any(k in lower_msg for k in ["list employees", "employees list", "employee names", "all employees"]):
        emp_names = [emp["emp_name"] for emp in employees]
        reply = "Here are the names of all employees:\n\n- " + "\n- ".join(emp_names)
        chat_history.append(AIMessage(content=reply))
        return reply

    # Specific employee
    for emp in employees:
        if emp["emp_name"].lower() in lower_msg:
            reply = (
                f"Here are the details of **{emp['emp_name']}**:\n\n"
                f"- Employee ID: {emp['emp_id']}\n"
                f"- Date of Birth: {emp['emp_dob']}\n"
                f"- Email: {emp['emp_email']}\n"
                f"- Mobile: {emp['phone']}\n"
                f"- Address: {emp['emp_address']}"
            )
            chat_history.append(AIMessage(content=reply))
            return reply

    # File content context
    file_text = file_knowledge.strip()
    if len(file_text) > 3000:
        file_text = file_text[:3000] + "\n...[Content Truncated]..."

    context = ""
    if file_text:
        context = "Here is reference content from uploaded file:\n" + file_text + "\n\n"

    final_prompt = context + f"User Question: {user_msg}"

    ai_answer = chat.invoke([HumanMessage(content=final_prompt)])
    bot_reply = ai_answer.content
    chat_history.append(AIMessage(content=bot_reply))

    return bot_reply

