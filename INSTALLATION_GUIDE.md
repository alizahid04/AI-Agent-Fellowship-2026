\# Installation Guide



\## Prerequisites



Before running the project, make sure the following software is installed:



\* Python 3.10 or later

\* Git

\* Streamlit

\* A Gemini API Key

\* (Optional) A Hugging Face API Key for Hugging Face models



\---



\# Step 1: Clone the Repository



```bash

git clone https://github.com/alizahid04/AI-Agent-Fellowship-2026.git

cd AI-Agent-Fellowship-2026

```



\---



\# Step 2: Create a Virtual Environment



\### Windows



```bash

python -m venv Generative\_Ai

Generative\_Ai\\Scripts\\activate

```



\### macOS / Linux



```bash

python3 -m venv Generative\_Ai

source Generative\_Ai/bin/activate

```



\---



\# Step 3: Install Required Packages



Install all dependencies listed in `requirements.txt`.



```bash

pip install -r requirements.txt

```



\---



\# Step 4: Configure API Keys



Create a file named `.env` in the project root directory.



Add your API keys as shown below:



```env

GEMINI\_API\_KEY=your\_gemini\_api\_key

HF\_API\_KEY=your\_huggingface\_api\_key

```



Replace the placeholder values with your own API keys.



\---



\# Step 5: Launch the Application



Run the following command:



```bash

streamlit run app.py

```



After a few seconds, Streamlit will start the application.



Open your browser and navigate to:



```text

http://localhost:8501

```



\---



\# Project Structure



```text

Generative\_Ai/

│

├── app.py

├── config.py

├── requirements.txt

├── .env

├── services/

├── utils/

├── notebook/

├── reports/

└── exports/

```



\---



\# Troubleshooting



\### Missing Module Error



Install the required packages again:



```bash

pip install -r requirements.txt

```



\---



\### Invalid API Key



Ensure that:



\* The `.env` file exists in the project root.

\* The API keys are valid.

\* There are no extra spaces around the key values.



\---



\### Streamlit Command Not Found



Install Streamlit manually:



```bash

pip install streamlit

```



Then run:



```bash

streamlit run app.py

```



\---



\# Successful Installation



If all steps are completed successfully, the Streamlit application will launch in your web browser. You can now interact with the application, switch between supported AI models, manage chat sessions, export conversations, and experiment with different prompting techniques.



