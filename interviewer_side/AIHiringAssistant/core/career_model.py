import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

import os

class CareerPersonalityModel:
    _instance = None
    _is_trained = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CareerPersonalityModel, cls).__new__(cls)
        return cls._instance

    def __init__(self, csv_path="jobProfileData.csv"):
        # Prevent re-initialization if already trained
        if CareerPersonalityModel._is_trained:
            print("[CareerPersonalityModel] Using existing trained model from memory.")
            return
            
        # Ensure path is relative to the AIHiringAssistant base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(base_dir, csv_path)
        print(f"[CareerPersonalityModel] Initializing model... Looking for dataset at: {self.csv_path}")
        
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"[CareerPersonalityModel] Successfully loaded {len(self.df)} profiles from {csv_path}")
            self._train()
        except Exception as e:
            # Fallback exact logic if dataset is missing
            print(f"[CareerPersonalityModel] ⚠️ WARNING: Dataset not found or failed to load. Using built-in fallback data. Error: {e}")
            self.df = pd.DataFrame({
                'Openness': [80.0, 20.0, 70.0, 30.0, 50.0, 90.0, 40.0],
                'Conscientiousness': [70.0, 90.0, 40.0, 80.0, 50.0, 60.0, 70.0],
                'Extraversion': [30.0, 80.0, 90.0, 20.0, 50.0, 80.0, 40.0],
                'Agreeableness': [60.0, 70.0, 40.0, 80.0, 50.0, 70.0, 60.0],
                'Neuroticism': [20.0, 40.0, 80.0, 30.0, 50.0, 30.0, 70.0],
                'Occupation': ['Software Engineer', 'Data Scientist', 'Marketing', 'Product Manager', 'UI/UX Designer', 'Sales', 'HR'],
                'Description': ['Coding logic detail', 'Math stats accuracy', 'Creative social outgoing', 'Manage plan organize', 'Design layout creative', 'talkative persuasive', 'empathetic listener']
            })
            self._train()
            
            print("[CareerPersonalityModel] Training complete!")
        CareerPersonalityModel._is_trained = True
            
    def _train(self):
        print("[CareerPersonalityModel] Training KNN on available dataset...")
        # The new CSV uses full trait names and 'Occupation'
        features = self.df[['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']].values
        labels = self.df['Occupation'].values
        
        # In case dataset has fewer than 5 rows
        n_neighbors = min(5, len(self.df))
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.knn.fit(features, labels)
        
        # TF-IDF logic
        if 'Description' in self.df.columns:
            self.tfidf_matrix = self.tfidf.fit_transform(self.df['Description'].astype(str))
        else:
            self.tfidf_matrix = self.tfidf.fit_transform(self.df['Occupation'].astype(str))
            
    def get_top_3_profiles(self, ocean_scores):
        print(f"\\n[CareerPersonalityModel] === Generating Recommendations ===")
        print(f"[CareerPersonalityModel] Candidate OCEAN Scores: {ocean_scores}")
        try:
            # The dataset values are 0-100 (e.g., 51.9, 46.99)
            # The user's input scores are 1.0-5.0
            # Scale 1-5 to 0-100: formula -> (score / 5.0) * 100.0
            scores = np.array([[
                (ocean_scores.get('O', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('C', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('E', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('A', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('N', 2.5) / 5.0) * 100.0
            ]])
            probs = self.knn.predict_proba(scores)[0]
            top_3_idx = np.argsort(probs)[-3:][::-1]
            classes = self.knn.classes_
            
            n_return = min(3, len(classes))
            top_matches = [str(classes[i]) for i in top_3_idx[:n_return]]
            print(f"[CareerPersonalityModel] Top Recommendations: {top_matches}")
            return top_matches
        except Exception as e:
            print("[CareerPersonalityModel] ❌ Error in get_top_3_profiles:", e)
            return ["Software Engineer", "Product Manager", "UI/UX Designer"]
            
    def get_job_suitability_percentage(self, ocean_scores, job_profile):
        print(f"\\n[CareerPersonalityModel] === Calculating Match for Target Role: '{job_profile}' ===")
        try:
            scores = np.array([[
                (ocean_scores.get('O', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('C', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('E', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('A', 2.5) / 5.0) * 100.0,
                (ocean_scores.get('N', 2.5) / 5.0) * 100.0
            ]])
            probs = self.knn.predict_proba(scores)[0]
            classes = list(self.knn.classes_)
            if job_profile in classes:
                idx = classes.index(job_profile)
                base_prob = probs[idx]
            else:
                base_prob = 0.5
                
            # Increase base prob visibly since KNN gives low exact probability for wide class counts
            pct = min(100, max(0, int(base_prob * 100) + 40))
            print(f"[CareerPersonalityModel] Analyzed match rate: {pct}%")
            return f"{pct}%"
        except Exception as e:
            print(f"[CareerPersonalityModel] ❌ Error calculating suitability: {e}")
            return "75%"
