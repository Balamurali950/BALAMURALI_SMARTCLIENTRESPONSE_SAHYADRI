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
   ```bash
   git clone https://github.com/Balamurali950/BALAMURALI_SMARTCLIENTRESPONSE_SAHYADRI.git
   cd RepositoryName
   ```

3. **Create a virtual environment: Run the following command to create a virtual environment**:
   ```bash
    python -m venv venv
   ```

4. **Activate the Virtual Environment:**<br/>
    **On windows**:
   ```bash
   venv\Scripts\activate
   ```
    **On Linux/Mac**:
   ```bash
   source venv/bin/activate
   ```

5. **Install Dependencies: Install all necessary dependencies using pip:**
   ```bash
    pip install -r requirements.txt
   ```

6. **Set Up Your OpenAI API Key:**<br/>
    Create a .env file in the root directory of the project.<br/>
    Inside the .env file, add the following line with your OpenAI API key:
   ```bash
    OPENAI_API_KEY=your_actual_api_key
   ```

7. **Make Sure .env is Added to `.gitignore`:**<br/>
    Add .env to .gitignore to prevent it from being pushed to GitHub:
    ```bash
    .env
    ```
## Running the Application

1. **Run the Streamlit App: After completing the setup, run the following command:**
   ```bash
   streamlit run main.py
   ```
3. **Open the App: Open your web browser and go to http://localhost:8501 to see the app running.**
