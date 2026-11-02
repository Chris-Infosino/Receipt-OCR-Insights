import streamlit as st

from interactions import select_random_receipt, use_uploaded_receipt

# Build user interface
st.set_page_config(
    page_title ="Receipt OCR and Insights", 
    layout ="centered"
    )

st.title("Receipt OCR and Insights")
st.markdown("The purpose of this project is to highlight important information from any receipt.")
st.markdown("**Easy OCR** is used to extract text.")
st.markdown("That text is then analyzed to create a JSON file containing important information from the receipt, which you will see annotated on the image.")

processing_progress = st.progress(0, text=None)
text_feedback_area = st.status(label="Awaiting file selection", type="step")

image_display_area = st.empty()

success_area = st.empty()

with st.sidebar:
    st.header("Select the receipt you want to analyze")
    st.write("You can upload a receipt of your own or use one from the dataset.")
       
    with st.form("Receipt file selection", clear_on_submit=True):
        st.markdown("**Select a receipt for me**")  
        if st.form_submit_button(
            "Click here to use a random receipt", 
            key ='RandomImage',
            ):
            select_random_receipt(image_display_area, text_feedback_area, processing_progress, success_area)

        st.space("small")

        st.markdown("**I want to upload my own receipt**")
        file_types = [".jpg", ".png"]
        uploaded_file = st.file_uploader(
            "Choose image to upload",
            type = file_types,
            )
        if st.form_submit_button(
            "Process selected receipt",
            key = "uploaded_file",
            ):
            use_uploaded_receipt(image_display_area, text_feedback_area, processing_progress, success_area, uploaded_file)
