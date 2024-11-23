import os
from dotenv import load_dotenv
import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
# Generate a response using the OpenAI Chat API
def generate_response(client_details):
    # Refined prompt for generating the exact email format
    messages = [
        {"role": "system", "content": "You are a professional project manager drafting email responses to clients."},
        {"role": "user", "content": f"""
        Create an email response based on the following details:

        {client_details}

        Format:
        Subject: [Subject based on project type and details]
        Dear [Client First Name] [Client Last Name],
        [Use a friendly and professional tone while avoiding overused formalities like 'I hope this email finds you well.']
        [Polite opening, acknowledging the client and introducing yourself by the 'From Name'.]
        [Description of how their requirements will be addressed, including dynamic pages and filters.]
        [Mention the budget and offer to discuss further if needed.]
        [the response must be professional, polished, and crafted as though written manually, with adjustments based on the client’s project details, budget, and other specific information provided]
        [Closing with a friendly tone.]

        Example Output:
        Subject: Real Estate Web application Development with Dynamic Pages
        Dear Geminas Ket,
        Thank you for reaching out!
        I'm Jesna, and I’d be happy to assist with the functionality setup for your real estate website. Based on your requirements, we’ll create four dynamic pages: one each for apartments, houses, business centres, and land, with two connected filters for sale and rent. This will ensure a functional and streamlined user experience.
        Given the budget constraints, please let me know if you’d like to discuss further to align the requirements with your budget of $100000.
        Looking forward to your response.
        Best regards,
        Jesna
        """}
    ]

    # Call OpenAI's Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace with "gpt-3.5-turbo" if needed
        messages=messages,
        max_tokens=500,  # Allow room for the full response
        temperature=0.7
    )

    # Return the generated response
    return response["choices"][0]["message"]["content"].strip()

# Streamlit UI for client details input
def main():
    st.title("Email Response Generator")
    st.markdown(
        "Enter client details below to generate a professional and tailored email response."
    )

    # Input fields for client information
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

    # Combine inputs into a formatted string for OpenAI
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

    # Generate response on button click
    if st.button("Generate Response"):
        with st.spinner("Generating response..."):
            try:
                response = generate_response(client_details)
                st.subheader("Generated Email:")
                st.text_area("Email Response", response, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
