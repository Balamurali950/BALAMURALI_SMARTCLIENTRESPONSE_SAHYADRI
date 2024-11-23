# BALAMURALI_SMARTCLIENTRESPONSE_SAHYADRI

# Smart Client Response

This project generates professional, human-like email responses based on client details using OpenAI's GPT model. The application uses **Streamlit** for the user interface and loads the OpenAI API key securely from a `.env` file.

## Getting Started

These instructions will help you set up the project and run it locally.

### Prerequisites

1. **Python 3.7 or higher** is required. You can download it from [python.org](https://www.python.org/downloads/).
2. **OpenAI API Key**: You'll need an API key from OpenAI. You can create one at [OpenAI](https://platform.openai.com/account/api-keys).

### Installation Steps

Follow these steps to get the project up and running:

1. **Clone the Repository**:
   git clone https://github.com/YourGitHubUsername/RepositoryName.git
   cd RepositoryName

2. **Create a virtual environment: Run the following command to create a virtual environment**:
    python -m venv venv

3. **Activate the Virtual Environment:**
    **On windows**:
       venv\Scripts\activate
    **On Linux/Mac**:
        source venv/bin/activate

4. **Install Dependencies: Install all necessary dependencies using pip:**
    pip install -r requirements.txt

5. **Set Up Your OpenAI API Key:**
    **Create a .env file in the root directory of the project.**
    **Inside the .env file, add the following line with your OpenAI API key:**
        OPENAI_API_KEY=your_actual_api_key

6. **Make Sure .env is Added to `.gitignore:**
    **Add .env to .gitignore to prevent it from being pushed to GitHub:**
        .env

## Running the Application

1. **Run the Streamlit App: After completing the setup, run the following command:**
    streamlit run main.py

2. **Open the App: Open your web browser and go to http://localhost:8501 to see the app running.**
