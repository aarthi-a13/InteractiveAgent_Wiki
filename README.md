<div align="center">

# 🚀 Interactive AI Agent <span style="font-size: 0.8em;">v1.0</span>

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Agent playground powered by Phidata**  

</div>

## 🌟 Features
- Interactive AI Agents
- Multi Agent workflows
- Wikipedia knowledge integration
- Web search integration
- Visualization dashboard
- Chat memory access

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/aarthi-a13/ThinkGen.git
cd ThinkGen

# Create & activate virtual environment
python -m venv myenv
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔑 API Key Generation
### 1. Phidata Connection
**Required for local agent integration**  
🔗 [Phidata Dashboard](https://www.phidata.app/)
1. Sign up/login to the dashboard using github
2. Navigate to "API Key" section and create one

### 2. Akash API Keys
**For chat and embedding models**  
🔗Refer [API Documentation](https://chatapi.akash.network/documentation) and,
1. Choose the chat model (Example: Meta-Llama-3-3-70B-Instruct)
2. Choose the embedding model (Example: BAAI-bge-large-en-v1-5)
3. Create API key by providing the name from [Akash Console](https://chatapi.akash.network/)

### 3. Timescale Database
**PostgreSQL cloud setup**  
🔗 [Cloud Console](https://console.cloud.timescale.com/)
1. Create free account and setup Postgresql service
2. The DB usrl must be in the below format to be replaced in playground.py
```bash
postgresql+psycopg://<PGUSER>:<PGPASSWORD>@<PGHOST>:<PGPORT>/<PGDATABASE>
```

## 🔐 Authentication
```bash
# Connect to Phidata Dashboard
phi auth
```
➡️ When prompted, login with your GitHub account

## 🚦 Usage
```bash
# Start the app playground
python playground.py
```

After starting the server, access the interactive playground:  
https://www.phidata.app/playground/chat


## 📂 Project Structure
```
ThinkGen/
├── playground.py        # Main application logic
├── requirements.txt     # Dependency specifications
├── .env                 # Environment configurations
└── Output/              # Chat screenshots
```

<div align="center" style="margin-top: 20px;">
  <hr style="border: 1px solid #eee;">
  <p>Made with Intelligence 🧠 by Agent Ninjas</p>
</div>
