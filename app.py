import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load model
model = load_model(r"E:\DOCUMENT\defect_detection\notebook\defect_detection_model.keras")
  # or .h5 if you saved it that way

# Load class names from training generator
class_names = ['Crazing', 'Inclusion', 'Patches', 'Rolled-in scale', 'Scratches', 'Other']  # Update if needed

def predict_defect(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    class_name = class_names[class_index]
    confidence = prediction[0][class_index]

    return class_name, confidence

# Streamlit UI
st.title("🧠 Defect Detection App")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    label, confidence = predict_defect("temp.jpg")
    st.success(f"Predicted: **{label}** with confidence **{confidence:.2f}**")