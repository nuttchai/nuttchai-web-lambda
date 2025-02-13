import os
import json
import urllib3

http = urllib3.PoolManager()

def generate_instruction_answer_prompt():
    NUTT_PROFILE = """
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
    Software Engineer with 3+ years of experience in web and backend development, cloud computing, and machine learning.
    Proven ability to deliver scalable solutions for over 3 million users.
    Seeking a full-time role across the software development lifecycle with a strong focus on adopting new technologies.
    
    **Experience**
    Software Engineer, Machine Learning at KASIKORN Business-Technology Group (Nov 2023 - Present, Bangkok, TH)
    - Improved chatbot efficiency by doubling release frequency with change-free PROD deployments, reclaiming 20% sprint capacity.
    - Streamlined 3,600+ banking inquiries/month by developing the open-source RAG system, Athena, integrated with MS Teams.
    - Optimized LLM performance, reducing batch response time by 3.37s and increasing TPS by 2.21x using gRPC streaming.
    - Automated sentiment analysis for YouTube videos via K8s CronJobs.
    - Reduced memory leaks by 84.7%, optimizing TensorFlow batch processing.
    Software Engineer at RentSpree (Jun 2022 - Oct 2023, Bangkok, TH)
    - Boosted user input speed by 43% and Tenant Screening conversions by 4% via address auto-complete integration.
    - Implemented a monorepo strategy for React hooks to enhance component reusability.
    - Accelerated agent service response by 5.71x via database indexing.
    - Led the transition from JavaScript to TypeScript, improving maintainability.
    Software Engineer Intern at CMKL University (Dec 2021 - May 2022, Bangkok, TH)
    - Designed, implemented, and deployed a system enabling 100+ students to track learning progress via mobile.
    Software Engineer Intern at ExxonMobil (Jun 2021 - Nov 2021, Bangkok, TH)
    - Automated SAP-to-MRMA compliance reports, reducing reporting time.
    - Accelerated report extraction by 3x through template optimization and indexing.
    Software Engineer Intern, Infrastructure at CMKL University (Jan 2021 - Mar 2021, Bangkok, TH)
    - Enhanced APEX SSH security by replacing fingerprint checks with time-bound SSH certificates via Google SSO.
    
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
    - Warehouse Cost Reporter: LINE chatbot for summarizing 100,000+ data records (JavaScript + Dialogflow).
    
    **Extracurriculars**
    - Instructor for Python ML Training (50+ participants in KMITL's BootCamp).
    - Lecturer for Software Testing (JMeter + Grafana + Prometheus).
    - Facilitated a clean coding workshop (60+ employees at RentSpree).
    - Teaching Assistant for Programming, Physics, and Statistics at KMITL.
    - Led CIE Open House (500+ high school students), handling budget and logistics.
    
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
