import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple

class MoodAnalyzer:
    def __init__(self):
        self.mood_vectors = {
            'happy': [0.8, 0.9, 0.7],
            'sad': [-0.6, -0.4, -0.8],
            'energetic': [0.9, 0.8, 0.9],
            'calm': [0.2, -0.3, -0.1],
            'anxious': [-0.4, 0.7, -0.5]
        }
        
        self.music_features = {
            'tempo': (0, 200),  # BPM
            'energy': (0, 1),
            'valence': (0, 1)   # Musical positiveness
        }
    
    def analyze_mood_entry(self, text: str, intensity: float) -> Dict[str, float]:
        """Analyze mood entry text and return mood vector."""
        # Initialize mood scores
        mood_scores = {mood: 0.0 for mood in self.mood_vectors.keys()}
        
        # Simple keyword matching (could be enhanced with NLP)
        keywords = text.lower().split()
        for word in keywords:
            for mood, vector in self.mood_vectors.items():
                if word in self._get_mood_keywords(mood):
                    mood_scores[mood] += intensity
        
        # Normalize scores
        total = sum(score for score in mood_scores.values() if score > 0)
        if total > 0:
            mood_scores = {k: v/total for k, v in mood_scores.items()}
            
        return mood_scores
    
    def get_music_recommendations(self, mood_scores: Dict[str, float]) -> List[Dict[str, float]]:
        """Generate music recommendations based on mood analysis."""
        # Calculate target musical features
        target_tempo = self._calculate_target_tempo(mood_scores)
        target_energy = self._calculate_target_energy(mood_scores)
        target_valence = self._calculate_target_valence(mood_scores)
        
        return [{
            'tempo': target_tempo,
            'energy': target_energy,
            'valence': target_valence,
            'confidence': self._calculate_confidence(mood_scores)
        }]
    
    def _calculate_target_tempo(self, mood_scores: Dict[str, float]) -> float:
        base_tempo = 120  # Default tempo
        tempo_modifiers = {
            'happy': 15,
            'sad': -20,
            'energetic': 30,
            'calm': -30,
            'anxious': 10
        }
        
        for mood, score in mood_scores.items():
            base_tempo += tempo_modifiers.get(mood, 0) * score
        
        return max(60, min(180, base_tempo))  # Clamp between 60-180 BPM
    
    def _calculate_target_energy(self, mood_scores: Dict[str, float]) -> float:
        energy = sum(score * self.mood_vectors[mood][1] for mood, score in mood_scores.items())
        return max(0, min(1, (energy + 1) / 2))  # Normalize to 0-1
    
    def _calculate_target_valence(self, mood_scores: Dict[str, float]) -> float:
        valence = sum(score * self.mood_vectors[mood][2] for mood, score in mood_scores.items())
        return max(0, min(1, (valence + 1) / 2))  # Normalize to 0-1
    
    def _calculate_confidence(self, mood_scores: Dict[str, float]) -> float:
        # Higher confidence if we have strong mood indicators
        strongest_mood = max(mood_scores.values())
        return min(1.0, strongest_mood * 1.5)
    
    def _get_mood_keywords(self, mood: str) -> List[str]:
        """Return keywords associated with each mood."""
        keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful'],
            'sad': ['sad', 'down', 'blue', 'depressed', 'unhappy'],
            'energetic': ['energetic', 'active', 'pumped', 'motivated'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed']
        }
        return keywords.get(mood, [])

    def get_mood_trends(self, mood_history: List[Tuple[datetime, Dict[str, float]]]) 
        -> Dict[str, List[float]]:
        """Analyze mood trends over time."""
        trends = {mood: [] for mood in self.mood_vectors.keys()}
        
        for _, mood_scores in mood_history:
            for mood, score in mood_scores.items():
                trends[mood].append(score)
        
        return trends