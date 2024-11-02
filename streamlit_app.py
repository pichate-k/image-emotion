import openai
import streamlit as st
from PIL import Image

# Show title and description.
st.title("🖼️ Image Emotion Prediction")
st.write(
    "Upload an image below and describe it – GPT will predict the emotion based on your description! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the OpenAI API key
    openai.api_key = openai_api_key

    # Let the user upload an image file via `st.file_uploader`.
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # If an image is uploaded, display it.
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Ask the user to describe the image.
        description = st.text_area(
            "Describe the image (for example, what the person is doing, their expressions, etc.):",
            placeholder="The person is sitting on a bench with a sad expression...",
        )

        if description:
            # Process the description to predict emotion
            messages = [
                {
                    "role": "system",
                    "content": "You are an assistant that predicts emotions based on descriptions of images.",
                },
                {
                    "role": "user",
                    "content": f"Here's an image description: {description}. What emotion do you infer from this?",
                },
            ]

            # Generate an emotion prediction using the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
            )

            # Extract and display the response
            emotion_prediction = response['choices'][0]['message']['content']
            st.write("Predicted Emotion:")
            st.write(emotion_prediction)
        else:
            st.write("Please provide a description of the image for emotion analysis.")
