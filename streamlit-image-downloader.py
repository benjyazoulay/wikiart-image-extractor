import streamlit as st
import os
import zipfile
import random
from PIL import Image
import io
import tempfile
from collections import defaultdict

def is_image(filename):
    try:
        with Image.open(filename) as img:
            return True
    except:
        return False

def get_all_images(folder_path):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file_path):
                image_files.append(file_path)
    return image_files

def create_zip(images, extract_dir):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        folder_counters = defaultdict(int)
        for img in images:
            relative_path = os.path.relpath(img, extract_dir)
            folder_name = os.path.dirname(relative_path)
            if folder_name == '':
                folder_name = 'root'
            folder_counters[folder_name] += 1
            new_name = f"{folder_name}_{folder_counters[folder_name]}{os.path.splitext(img)[1]}"
            zipf.write(img, new_name)
    return zip_buffer

st.title("Wikiart images extractor")

uploaded_folder = st.file_uploader("Choisissez un dossier", type="zip", accept_multiple_files=False)

if uploaded_folder is not None:
    with tempfile.TemporaryDirectory() as extract_dir:
        with zipfile.ZipFile(uploaded_folder, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        all_images = get_all_images(extract_dir)
        
        st.write(f"Nombre total d'images trouvées : {len(all_images)}")
        
        if st.button("Télécharger toutes les images"):
            zip_buffer = create_zip(all_images, extract_dir)
            
            st.download_button(
                label="Télécharger le fichier ZIP",
                data=zip_buffer.getvalue(),
                file_name="toutes_les_images.zip",
                mime="application/zip"
            )
        
        num_images = st.number_input("Nombre d'images à télécharger", min_value=1, max_value=len(all_images), value=1)
        
        if st.button(f"Télécharger {num_images} image(s) aléatoire(s)"):
            selected_images = random.sample(all_images, num_images)
            zip_buffer = create_zip(selected_images, extract_dir)
            
            st.download_button(
                label="Télécharger le fichier ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"{num_images}_images_aleatoires.zip",
                mime="application/zip"
            )