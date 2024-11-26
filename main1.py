import os
from dotenv import load_dotenv
import openai
import streamlit as st
import json

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize feedback log file if it doesn't exist
def initialize_feedback_log():
    if not os.path.exists("feedback_log.json"):
        with open("feedback_log.json", "w") as f:
            json.dump([], f)  # Create an empty list in the file

# Analyze feedback trends
def analyze_feedback():
    try:
        with open("feedback_log.json", "r") as f:
            feedback_entries = json.load(f)
        issues = {"budget": 0, "tone": 0, "clarity": 0}
        for entry in feedback_entries:
            feedback_text = entry["feedback"].lower()
            if "budget" in feedback_text:
                issues["budget"] += 1
            if "tone" in feedback_text:
                issues["tone"] += 1
            if "clarity" in feedback_text:
                issues["clarity"] += 1
        return issues
    except FileNotFoundError:
        return {}

# Adjust the system prompt dynamically based on feedback trends
def adjust_prompt_based_on_feedback(feedback_analysis):
    adjustments = []
    if feedback_analysis.get("budget", 0) > 5:
        adjustments.append("Ensure the budget details are clearly addressed.")
    if feedback_analysis.get("tone", 0) > 5:
        adjustments.append("Adjust the tone to be more formal and professional.")
    if feedback_analysis.get("clarity", 0) > 5:
        adjustments.append("Focus on improving clarity and conciseness.")
    return " ".join(adjustments)

# Generate a response using OpenAI Chat API
def generate_response(client_details):
    feedback_analysis = analyze_feedback()
    feedback_adjustment = adjust_prompt_based_on_feedback(feedback_analysis)

    from_name = ""
    for line in client_details.split("\n"):
        if "From Name:" in line:
            from_name = line.split(":")[1].strip()
            break
    from_name = from_name if from_name else "Your Name"

    messages = [
        {"role": "system", "content": 
         f"You are a professional project manager drafting email responses to clients. Your responses should be context-aware, professional, and flexible. Avoid rigid templates. Tailor each response to the client's unique details. {feedback_adjustment}"},
        {"role": "user", "content": f"""
        Based on the following client details, craft a professional and context-aware email response:

        {client_details}

        Remember to:
        - Use a friendly and professional tone.
        - Address the client's unique requirements and ensure the response is specific to their project details.
        - Avoid overused phrases like 'I hope this email finds you well.'
        - Provide clear next steps and, if applicable, discuss aligning the project requirements with their budget.
        """}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",  
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    final_response = response["choices"][0]["message"]["content"].strip()

    # Clean up any existing signature lines
    final_response_lines = final_response.split("\n")
    cleaned_response_lines = []
    for line in final_response_lines:
        if any(placeholder in line.lower() for placeholder in ["[your name]", "[your position]", "[your contact information]"]):
            continue
        if "best regards" in line.lower() or from_name.lower() in line.lower():
            continue
        if not line.strip():
            continue
        cleaned_response_lines.append(line.strip())

    cleaned_response = "\n\n".join(cleaned_response_lines).strip()
    cleaned_response += f"\n\nBest regards,\n{from_name}"

    return cleaned_response

# Prepare fine-tuning data
def prepare_fine_tuning_data():
    try:
        with open("feedback_log.json", "r") as f:
            feedback_entries = json.load(f)
        fine_tuning_data = []
        for entry in feedback_entries:
            fine_tuning_data.append({
                "prompt": entry["client_details"],
                "completion": entry["generated_response"]
            })
        with open("fine_tuning_data.jsonl", "w") as f:
            for item in fine_tuning_data:
                f.write(json.dumps(item) + "\n")
        return "Fine-tuning data prepared successfully!"
    except Exception as e:
        return f"Error while preparing fine-tuning data: {e}"

# Fine-tune the OpenAI model
def fine_tune_model():
    try:
        prepare_fine_tuning_data()
        openai.FineTune.create(
            training_file="fine_tuning_data.jsonl",
            model="gpt-4",
            n_epochs=1
        )
        return "Fine-tuning triggered successfully!"
    except Exception as e:
        return f"Error while fine-tuning the model: {e}"

# Log feedback to file
def log_feedback(client_details, generated_response, feedback, mistakes="", suggestions=""):
    feedback_entry = {
        "client_details": client_details,
        "generated_response": generated_response,
        "feedback": feedback,
        "mistakes": mistakes,
        "suggestions": suggestions
    }

    try:
        with open("feedback_log.json", "r+") as f:
            data = json.load(f)
            data.append(feedback_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
        return "Feedback logged successfully!"
    except Exception as e:
        return f"Error while logging feedback: {e}"

# Streamlit UI for client details input
def main():
    st.title("Smart Client Response Generator")
    st.markdown("Generate a professional email response and provide feedback for future improvements.")

    from_name = st.text_input("From Name", "Jesna")
    client_first_name = st.text_input("Client First Name", "Geminas")
    client_last_name = st.text_input("Client Last Name", "Ket")
    client_email = st.text_input("Client Email", "GeminasKet@gmail.com")
    client_country = st.text_input("Client Country", "Romania")
    client_location = st.text_input("Client Location (if provided)", "Romania")
    client_language = st.text_input("Client Language", "English")
    project_type = st.text_input("Project Type", "Content with Databases")
    service_category = st.text_input("Service Category", "Web Development")
    client_website = st.text_input("Client Website (if any)", "No")
    additional_info = st.text_area(
        "Additional Information (if any)", 
        "I need 4 dynamic pages for a real estate Web-application: one each for apartments, houses, business centres, and land. I need 2 filters for 'for sale' and 'for rent,' and they should be connected. Don't bother with the design; I'll handle that. I just need the functionality. The budget should be $100000. Thank you!"
    )

    client_details = f"""
    From Name: {from_name}
    Client First Name: {client_first_name}
    Client Last Name: {client_last_name}
    Client Email: {client_email}
    Client Country: {client_country}
    Client Location: {client_location}
    Client Language: {client_language}
    Project Type: {project_type}
    Service Category: {service_category}
    Client Website: {client_website}
    Additional Information: {additional_info}
    """

    if st.button("Generate Response"):
        with st.spinner("Generating response..."):
            try:
                response = generate_response(client_details)
                st.subheader("Generated Email:")
                st.text_area("Email Response", response, height=300)
                st.session_state.generated_response = response
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if "generated_response" in st.session_state:
        st.subheader("Was this response helpful?")
        feedback = st.text_area("Provide feedback or suggest improvements for the response:", key="feedback")
        mistakes = st.text_area("What mistakes did you notice in the response?", key="mistakes")
        suggestions = st.text_area("How would you improve the communication?", key="suggestions")

        if st.button("Submit Feedback"):
            if not feedback.strip() and not mistakes.strip() and not suggestions.strip():
                st.warning("Feedback, mistakes, and suggestions cannot all be empty. Please provide input.")
            else:
                result = log_feedback(client_details, st.session_state.generated_response, feedback, mistakes, suggestions)
                st.success(result)

if __name__ == "__main__":
    initialize_feedback_log()
    main()
