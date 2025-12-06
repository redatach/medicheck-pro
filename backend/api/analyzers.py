"""
Logique d'analyse médicale SIMPLE
"""

class SimpleMedicalAnalyzer:
    """
    Analyseur simple pour symptômes + photos
    """
    
    def analyze(self, symptoms_text, pain_level, photo_data=None):
        """
        Analyse les symptômes et retourne un résultat simple
        """
        # 1. Analyser le texte des symptômes
        text_analysis = self._analyze_text(symptoms_text)
        
        # 2. Analyser la photo si fournie
        photo_analysis = self._analyze_photo(photo_data) if photo_data else {}
        
        # 3. Calculer le niveau d'urgence
        emergency_score = self._calculate_score(text_analysis, pain_level, photo_analysis)
        
        # 4. Générer les recommandations
        recommendations = self._get_recommendations(emergency_score)
        
        return {
            'emergency_score': emergency_score,
            'level': self._get_level(emergency_score),
            'reasons': text_analysis['detected_symptoms'],
            'recommendations': recommendations,
            'photo_analysis': photo_analysis
        }
    
    def _analyze_text(self, text):
        """Analyse simple du texte des symptômes"""
        text_lower = text.lower()
        
        # Détection de symptômes critiques
        critical_symptoms = []
        if any(word in text_lower for word in ['douleur thoracique', 'poitrine']):
            critical_symptoms.append('Douleur thoracique')
        if any(word in text_lower for word in ['difficulté respiratoire', 'essoufflement']):
            critical_symptoms.append('Problème respiratoire')
        if 'fièvre' in text_lower:
            critical_symptoms.append('Fièvre')
        if 'tête' in text_lower:
            critical_symptoms.append('Céphalée')
        
        return {
            'detected_symptoms': critical_symptoms,
            'symptom_count': len(critical_symptoms)
        }
    
    def _analyze_photo(self, photo_data):
        """Analyse simple d'une photo (simulation)"""
        # En production, utiliser un modèle ML ici
        return {
            'has_photo': True,
            'analysis': 'Photo reçue pour analyse visuelle',
            'confidence': 0.7,
            'detected': ['Rougeur possible', 'Gonflement détecté']  # Simulation
        }
    
    def _calculate_score(self, text_analysis, pain_level, photo_analysis):
        """Calcule un score d'urgence simple (0-10)"""
        score = 0
        
        # Points pour symptômes critiques
        score += len(text_analysis['detected_symptoms']) * 2
        
        # Points pour douleur
        score += pain_level * 0.5
        
        # Points pour photo (si anomalie détectée)
        if photo_analysis.get('detected'):
            score += 1
        
        return min(score, 10)
    
    def _get_level(self, score):
        """Détermine le niveau d'urgence"""
        if score >= 8:
            return 'CRITIQUE'
        elif score >= 5:
            return 'ÉLEVÉ'
        elif score >= 3:
            return 'MODÉRÉ'
        else:
            return 'FAIBLE'
    
    def _get_recommendations(self, score):
        """Retourne des recommandations basées sur le score"""
        if score >= 8:
            return [
                "Appelez immédiatement le 15 (SAMU)",
                "Ne conduisez pas vous-même",
                "Allongez-vous en attendant les secours"
            ]
        elif score >= 5:
            return [
                "Consultez un médecin dans les 24h",
                "Surveillez vos symptômes",
                "Évitez l'auto-médication"
            ]
        else:
            return [
                "Reposez-vous et hydratez-vous",
                "Surveillez l'évolution",
                "Consultez si aggravé"
            ]

# Instance globale
analyzer = SimpleMedicalAnalyzer()