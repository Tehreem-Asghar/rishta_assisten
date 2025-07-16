from pydantic import BaseModel
from dotenv import load_dotenv
import os, requests
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, function_tool
from agents.run import RunConfig
from fastapi import FastAPI
import uvicorn

from fastapi.middleware.cors import CORSMiddleware




# 🔒 Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("API_KEY")
ULTRAMSG_URL = os.getenv("Api_Url")
TOKEN = os.getenv("Token")

# ⚠️ Validate env
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is not set")
if not ULTRAMSG_URL or not TOKEN:
    raise ValueError("❌ WhatsApp configuration missing")

app = FastAPI()
# 👇 Add this after `app = FastAPI()`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📋 Profiles data
profiles = [
    # 👩 Female Profiles
    {
        "name": "Ayesha Khan",
        "age": 24,
        "gender": "female",
        "city": "Karachi",
        "education": "BS CS",
        "profession": "Software Engineer",
        "sect": "Sunni",
        "marital_status": "Single",
    },
    {
        "name": "Zainab Noor",
        "age": 26,
        "gender": "female",
        "city": "Islamabad",
        "education": "Masters in Economics",
        "profession": "Lecturer",
        "sect": "Barelvi",
        "marital_status": "Single",
    },
    {
        "name": "Fatima Shah",
        "age": 30,
        "gender": "female",
        "city": "Lahore",
        "education": "BBA",
        "profession": "HR Manager",
        "sect": "Shia",
        "marital_status": "Divorced",
    },
    {
        "name": "Hira Iqbal",
        "age": 27,
        "gender": "female",
        "city": "Multan",
        "education": "MBBS",
        "profession": "Doctor",
        "sect": "Deobandi",
        "marital_status": "Single",
    },
    {
        "name": "Mariam Javed",
        "age": 25,
        "gender": "female",
        "city": "Faisalabad",
        "education": "MSc Mathematics",
        "profession": "Teacher",
        "sect": "Sunni",
        "marital_status": "Divorced",
    },
    {
        "name": "Nimra Saeed",
        "age": 28,
        "gender": "female",
        "city": "Rawalpindi",
        "education": "MBA",
        "profession": "Marketing Executive",
        "sect": "Bohra",
        "marital_status": "Single",
    },
    {
        "name": "Sana Tariq",
        "age": 29,
        "gender": "female",
        "city": "Hyderabad",
        "education": "LLB",
        "profession": "Lawyer",
        "sect": "Ahl-e-Hadith",
        "marital_status": "Divorced",
    },
    {
        "name": "Laiba Hassan",
        "age": 23,
        "gender": "female",
        "city": "Sialkot",
        "education": "BSc Chemistry",
        "profession": "Research Assistant",
        "sect": "Muslim",
        "marital_status": "Single",
    },
    {
        "name": "Kiran Malik",
        "age": 31,
        "gender": "female",
        "city": "Quetta",
        "education": "Masters in English",
        "profession": "Content Writer",
        "sect": "Ismaili",
        "marital_status": "Divorced",
    },
    {
        "name": "Areeba Nisar",
        "age": 22,
        "gender": "female",
        "city": "Peshawar",
        "education": "BS Psychology",
        "profession": "Intern Psychologist",
        "sect": "Shia",
        "marital_status": "Single",
    },
    {
        "name": "Mehwish Zafar",
        "age": 26,
        "gender": "female",
        "city": "Bahawalpur",
        "education": "M.Ed",
        "profession": "School Principal",
        "sect": "Sunni",
        "marital_status": "Single",
    },
    {
        "name": "Iqra Kamal",
        "age": 27,
        "gender": "female",
        "city": "Gujranwala",
        "education": "BS Software Engineering",
        "profession": "UI/UX Designer",
        "sect": "Deobandi",
        "marital_status": "Divorced",
    },
    {
        "name": "Sadia Rauf",
        "age": 29,
        "gender": "female",
        "city": "Sargodha",
        "education": "MPhil Physics",
        "profession": "Lecturer",
        "sect": "Barelvi",
        "marital_status": "Single",
    },

    # 👨 Male Profiles
    {
        "name": "Ali Raza",
        "age": 28,
        "gender": "male",
        "city": "Lahore",
        "education": "MBA",
        "profession": "Banker",
        "sect": "Shia",
        "marital_status": "Single",
    },
    {
        "name": "Usman Tariq",
        "age": 30,
        "gender": "male",
        "city": "Karachi",
        "education": "BS CS",
        "profession": "Software Engineer",
        "sect": "Sunni",
        "marital_status": "Divorced",
    },
    {
        "name": "Ahmed Nawaz",
        "age": 32,
        "gender": "male",
        "city": "Rawalpindi",
        "education": "MS Data Science",
        "profession": "Data Analyst",
        "sect": "Deobandi",
        "marital_status": "Single",
    },
    {
        "name": "Hassan Qureshi",
        "age": 29,
        "gender": "male",
        "city": "Multan",
        "education": "LLB",
        "profession": "Lawyer",
        "sect": "Ahl-e-Hadith",
        "marital_status": "Single",
    },
    {
        "name": "Bilal Khan",
        "age": 27,
        "gender": "male",
        "city": "Peshawar",
        "education": "BBA",
        "profession": "Marketing Manager",
        "sect": "Barelvi",
        "marital_status": "Divorced",
    },
    {
        "name": "Fahad Ali",
        "age": 31,
        "gender": "male",
        "city": "Islamabad",
        "education": "MSc Physics",
        "profession": "Lecturer",
        "sect": "Sunni",
        "marital_status": "Single",
    },
    {
        "name": "Saad Mehmood",
        "age": 33,
        "gender": "male",
        "city": "Faisalabad",
        "education": "MBBS",
        "profession": "Doctor",
        "sect": "Shia",
        "marital_status": "Divorced",
    },
    {
        "name": "Imran Baig",
        "age": 34,
        "gender": "male",
        "city": "Hyderabad",
        "education": "B.Com",
        "profession": "Accountant",
        "sect": "Ismaili",
        "marital_status": "Single",
    },
    {
        "name": "Zeeshan Ashraf",
        "age": 28,
        "gender": "male",
        "city": "Sialkot",
        "education": "BS Electrical Engineering",
        "profession": "Engineer",
        "sect": "Muslim",
        "marital_status": "Single",
    },
    {
        "name": "Kashif Iqbal",
        "age": 29,
        "gender": "male",
        "city": "Bahawalpur",
        "education": "Masters in Finance",
        "profession": "Investment Analyst",
        "sect": "Bohra",
        "marital_status": "Divorced",
    },
    {
        "name": "Adnan Sheikh",
        "age": 35,
        "gender": "male",
        "city": "Gujranwala",
        "education": "MPhil Islamic Studies",
        "profession": "Research Scholar",
        "sect": "Deobandi",
        "marital_status": "Single",
    },
    {
        "name": "Waqas Ahmed",
        "age": 30,
        "gender": "male",
        "city": "Quetta",
        "education": "BS Media Studies",
        "profession": "TV Producer",
        "sect": "Barelvi",
        "marital_status": "Divorced",
    },
]

# 📥 User Input Schema
class UserInput(BaseModel):
    gender: str
    age_range: list[int]
    city: str = ""
    education: str = ""
    profession: str = ""
    sect: str = ""
    marital_status: str = "Single"
    phone: str


# 📤 WhatsApp Message Format
class WhatsAppRequest(BaseModel):
    phone: str
    message: str


# 🧠 Tool: Match Rishtas
@function_tool
def match_rishtas(data: UserInput):
    """
    🔍 Finds rishta matches based on preferences.
    """
    results = [
        p for p in profiles
        if p["gender"].lower() == data.gender.lower()
        and data.age_range[0] <= p["age"] <= data.age_range[1]
        and (data.city.lower() in p["city"].lower() if data.city else True)
        and (data.education.lower() in p["education"].lower() if data.education else True)
        and (data.profession.lower() in p["profession"].lower() if data.profession else True)
        and (data.sect.lower() == p["sect"].lower() if data.sect else True)
        and p["marital_status"].lower() == data.marital_status.lower()
    ]
    return {"matches": results}


# 📲 Tool: Send WhatsApp Message
@function_tool
def send_whatsapp(data: WhatsAppRequest):
    """
    📤 Sends rishta details to given WhatsApp number.
    """
    url = f"{ULTRAMSG_URL}messages/chat"
    payload = f"token={TOKEN}&to={data.phone}&body={data.message}"
    headers = {"content-type": "application/x-www-form-urlencoded"}

    try:
        res = requests.post(
            url,
            data=payload.encode("utf8").decode("iso-8859-1"),
            headers=headers
        )
        if res.status_code == 200:
            return {"status": "✅ WhatsApp message sent!"}
        return {"status": f"❌ Failed: {res.text}"}
    except Exception as e:
        return {"status": f"❌ Error: {str(e)}"}


# 🔗 Set up Gemini-compatible client
external_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🤖 Agent
agent = Agent(
    name="Rishta Assistant",
   instructions=(
    "You are a professional Rishta Assistant. "
    "Your task is to help users find suitable rishtas based on gender, age, city, education, profession, sect, and marital status. "
    "Use the `match_rishtas` tool to filter matches. "
    "Once a match is found, immediately format the result in this format:\n\n"
    "Hy  \n \n I am your Rishta Assistant.\n Based on your preferences, here is a suggested match:\n\n Name: {name}\n Education: {education}\n Profession: {profession}\n City: {city}\n Sect: {sect}\n Marital Status: {marital_status}\n Do you like this proposal ?\n\n"
    "Then use the `send_whatsapp` tool to send it to the user's phone number without asking for confirmation."

    " If no match is found, send this message via WhatsApp instead:\n\n"
    "\"Hy  I'm your Rishta Assistant. Unfortunately, there is no suitable match based on your preferences at this moment. "
    "But don't worry! We are always adding new profiles and will reach out to you as soon as we find a suitable match."
    "Thank you for trusting us! 💖\""
),
    model=model,
    tools=[match_rishtas, send_whatsapp],
)


# 🚀 FastAPI Endpoint
@app.post("/")
async def get_rishta(details: UserInput):
    user_input = f"""
I'm looking for a rishta. These are my preferences:
Gender: {details.gender}  
Age Range: {details.age_range}  
City: {details.city}
Education: {details.education}  
Profession: {details.profession}  
Sect: {details.sect}  
Marital Status: {details.marital_status}

My WhatsApp number is {details.phone}. Once a match is found, send it directly to my WhatsApp without asking for confirmation.
"""

    result = await Runner.run(agent, user_input, run_config=config)
    return {"response": result.final_output}