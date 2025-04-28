import os
import json
import urllib3
from datetime import datetime

http = urllib3.PoolManager()


def year_diff(start: str, end: str) -> int:
    """
    Calculate the difference in full years between two Year-Month strings.

    Args:
        start: A string in "YYYY-MM" format representing the earlier date.
        end:   A string in "YYYY-MM" format representing the later date.

    Returns:
        The number of complete years between start and end (rounded down).
    """
    y1, m1 = map(int, start.split('-'))
    y2, m2 = map(int, end.split('-'))
    total_months = (y2 - y1) * 12 + (m2 - m1)
    return total_months // 12


def get_years_of_working_experience() -> int:
    START_WORKING_YEARS_MONTHS = "2022-06"
    CURRENT_WORKING_YEARS_MONTHS = datetime.today().strftime('%Y-%m')
    return year_diff(START_WORKING_YEARS_MONTHS, CURRENT_WORKING_YEARS_MONTHS)


def generate_instruction_answer_prompt():
    YEARS_WORKING_EXPERIENCES = get_years_of_working_experience()    
    NUTT_PROFILE = f"""
     **Personal Information**
    - Name: Nutt Chairatana
    - Location: Bangkok, Thailand
    - Contact: nuttc@nuttchai.com, +66 86-392-2658
    - Birthday: 13th December 1999
    - LinkedIn: linkedin.com/in/nuttchai
    - Portfolio: nuttchai.com
    - GitHub: github.com/nuttchai
    - Girlfriend: Pemika Kongsinthu (Oom)
    
    **Objective**
    Software Engineer with {YEARS_WORKING_EXPERIENCES}+ years of experience in web and backend development, cloud computing, and machine learning.
    Proven ability to deliver scalable solutions for over 3 million users.
    Seeking a full-time role across the software development lifecycle with a strong focus on adopting new technologies.
    
    **Experience**
    Software Engineer, Machine Learning at KASIKORN Business-Technology Group (Nov 2023 - {datetime.today().strftime('%m %Y')}, Bangkok, TH)
    - Automated NLP training and release, saving $20.2k annually (reclaiming 20% sprint capacity), by using K8s Jobs and AWS EFS for shared model access in cluster
    - Streamlined 3,600+ monthly banking inquiries by developing the open-source RAG system, Athena, integrated with MS Teams
    - Initiated a high-throughput inference LLM pipeline utilizing gRPC server streaming with a leaky bucket rate limiter and asynchronous log to improve service latency by 3.37s and capacity by 2.21× over traditional REST, as confirmed by k6
    - Automated YouTube video cues reviewing (saving 1.5 MD/week) using sentiment analysis triggered by K8s CronJob
    - Reduced NLP memory leaks by 84.7% and response time by 31ms (88.8%), tracked via Python Profiler and k6, by revamping TensorFlow to process inputs as single batches to eliminate cache from input splitting
    FYI, In KASIKORN Business-Technology Group, 1 MD costs 16k Baht
    Software Engineer at RentSpree (Jun 2022 - Oct 2023, Bangkok, TH)
    - Boosted input speed by 43% and Tenant Screening conversions by 4%, verified by Amplitude, by adding address auto-complete
    - Streamlined web component reusability across projects by promoting a mono repository for React hooks
    - Accelerated agent service response by 5.71x, as measured by k6, by implementing database indexing
    - Led the transition of JavaScript projects to TypeScript to enhance codebase quality and maintainability
    Software Engineer Intern at CMKL University (Dec 2021 - May 2022, Bangkok, TH)
    - Led the design, development, and deployment of a mobile learning platform utilized by 100+ CMKL students
    Software Engineer Intern at ExxonMobil (Jun 2021 - Nov 2021, Bangkok, TH)
    - Reduced compliance reporting time by automating SAP-to-MRMA data synchronization with Azure Durable Functions
    - Accelerated calibration report extraction by 3x, verified by Azure App Insights, by refining templates and indexing queries
    Junior Software Developer, Infrastructure at CMKL University (Jan 2021 - Mar 2021, Bangkok, TH)
    - Strengthened APEX SSH security by replacing host fingerprint checks with time-bound SSH certificates via Google SSO
    
    **Education**
    Master's in Robotics and Artificial Intelligence Engineering, King Mongkut's Institute of Technology Ladkrabang (2022 - 2024)
    - Award: First-Class Honors Graduate Scholarship
    - Thesis: Software System Performance Prediction and Health Assessment in Cloud Environments (Grade: Outstanding)
    Bachelor's in Computer Engineering, King Mongkut's Institute of Technology Ladkrabang (2018 - 2022)
    - Award: First-Class Honors & Top Academic Performer Scholarship
    
    **Skills**
    - Programming Languages: C#, Go, JavaScript, Python, TypeScript
    - Technologies: ASP.NET, AWS, Docker, GCP, gRPC, Kafka, Kubernetes, MongoDB, NestJS, OTel, PostgreSQL, React
    
    **Achievements**
    - 4th Place in Cloud Ace Hackathon TH (GenAI ad solution based on preferences) (Jun 2024)
    - Finalist in HUAWEI CLOUD Developer Hackathon (Cloud-based traffic prediction solution) (Nov 2020)
    
    **Projects**
    - Auto Attendance System: Python facial recognition for 30+ students in a single frame.
    - Hungry Hub: Food-ordering app using NodeJS & React, AWS EKS, and Jenkins automation.
    - Patient Monitoring System: Real-time weight tracking with 99.9% uptime (React + Arduino).
    - Smart Garden: 24/7 IoT plant care using Raspberry Pi & WebSocket.
    - Game Sale Predictor: A game sales prediction model in Python. Employed a variety of predictive algorithms, including linear regression, random forest, and gradient boosting.
    - Warehouse Cost Reporter: LINE chatbot for summarizing 100,000+ data records (JavaScript + Dialogflow).
    
    **Extracurriculars**
    - Instructor for Python ML Training (50+ participants in KMITL's BootCamp).
    - Lecturer for Software Testing (JMeter + Grafana + Prometheus).
    - Facilitated a company-wide session for 60+ RentSpree engineers.
    - Teaching Assistant for Programming, Physics, and Statistics at KMITL.
    - Led CIE Open House (500+ high school students), handling budget and logistics.
    - Event Coordinator of CIE Arduino Workshop (50+ high school students).
    
    **Publications**
    - IEEE Access (2024): Stateless System Performance Prediction and Health Assessment in Cloud Environments.
    - iSAI-NLP (2023): Cloud Stateless Server Failover Prediction Using ML on System Metrics.
    
    **Certifications**
    AWS Certified Solution Architect - Associate (Jan 2023)
    """

    SYSTEM_PROMPT = f"""
    Task: 
    Retrieve relevant details from the knowledge base and generate accurate responses based on Nutt Chairatana's experience, skills, education, and projects to answer the latest user question.

    Response Format:
    - Provide clear, factual, structured responses. 
    - Use concise summaries, including key details.
    - If the requested information is unavailable, politely mention it.
    
    Context Document (Profile Information):
    {NUTT_PROFILE} 
    
    Additional Information:
    - Today Date: {datetime.today().strftime('%Y-%m-%d')}
    """

    return SYSTEM_PROMPT

def generate_instruction_format_prompt(message):
    SYSTEM_PROMPT = f"""
        Task: 
        Add new line ("\\n") on every bullet appeared of message below. Otherwise, keep the same.
        
        Response Format: 
        - Provide clear, factual, structured responses.
        
        Message:
        {message}
        """

    return SYSTEM_PROMPT

def send_api_llm_request(model, messages):
    # Prepare OpenAI API request payload
    payload = json.dumps({
        "model": model,
        "messages": messages
    })
    print("Payload:", payload)
    
    # ✅ Make request to OpenAI API using urllib3
    response = http.request(
        "POST",
        "https://api.openai.com/v1/chat/completions",
        body=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv("OPENAI_API_KEY")}",
        },
        retries=False
    )
    return response

def lambda_handler(event, context):
    try:
        print("Event:", event)
        MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

        # ✅ Ensure body is parsed properly
        body = json.loads(event.get("body", "{}"))
        print("Request Body:", body)
        chat_history = body.get("chatHistory", [])
        used_messages = chat_history[-10:]  # Keep only last 10 messages
        print("Used Messages:", used_messages)

        # Add system prompt
        instruction_prompt = generate_instruction_answer_prompt()
        used_messages.insert(0, {"role": "system", "content": instruction_prompt})

        # Send Request to LLM (Answer Response)
        response = send_api_llm_request(MODEL, used_messages)

        # Parse response data
        data = json.loads(response.data.decode("utf-8"))
        message = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        
        """ TODO: Fix the prompt to format the response message
        # Format the response message
        instruction_prompt = generate_instruction_format_prompt(message)
        
        # Send Request to LLM (Format Response)
        response = send_api_llm_request(MODEL, [{"role": "user", "content": instruction_prompt}])

        # Parse response data
        data = json.loads(response.data.decode("utf-8"))
        message = data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        """

        return {
            "statusCode": 200,
            "body": json.dumps({"reply": message})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server Error"})
        }
