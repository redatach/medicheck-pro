# api/ml_service.py

import torch
from transformers import pipeline
from PIL import Image
import google.generativeai as genai
import os

class MedicalDiagnosticAI:
    def __init__(self):
        # 1. Modèle NLP pour le texte (symptômes)
        self.nlp_model = pipeline(
            "text-classification", 
            model="medical-bert",  # À remplacer par un vrai modèle médical
            device=0 if torch.cuda.is_available() else -1
        )
        
        # 2. Modèle Vision pour les photos
        # Option A: Google Gemini Vision
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        
        # Option B: Custom CNN médical
        # self.cnn_model = torch.load('models/skin_cnn.pth')
        
        # 3. Dataset médical
        self.disease_db = self.load_disease_database()
    
    def analyze_text(self, text_description, age, gender):
        """Analyse le texte des symptômes"""
        # Extraction des symptômes clés
        symptoms = self.extract_symptoms(text_description)
        
        # Recherche dans la base
        possible_diseases = self.match_symptoms_to_diseases(symptoms, age, gender)
        
        return {
            'extracted_symptoms': symptoms,
            'possible_diseases': possible_diseases
        }
    
    def analyze_image(self, image_path):
        """Analyse une photo médicale"""
        image = Image.open(image_path)
        
        # Option A: Gemini Vision
        prompt = """
        Analyse cette photo médicale. Décris:
        1. Ce qui est visible (éruption, rougeur, gonflement, etc.)
        2. Éventuelle pathologie visible
        3. Niveau d'urgence (1-4)
        
        Réponds en format JSON.
        """
        
        response = self.vision_model.generate_content([prompt, image])
        
        # Option B: CNN custom
        # predictions = self.cnn_model.predict(image)
        
        return self.parse_vision_response(response.text)
    
    def full_diagnostic(self, text_description, image_path=None, age=None, gender=None):
        """Analyse combinée texte + image"""
        text_results = self.analyze_text(text_description, age, gender)
        
        image_results = None
        if image_path and os.path.exists(image_path):
            image_results = self.analyze_image(image_path)
        
        # Fusion des résultats
        final_diagnosis = self.fuse_results(text_results, image_results)
        
        return final_diagnosis