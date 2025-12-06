# parsing record & sort probabilitas

# processor.py
from typing import Tuple, Dict, List

def sort_probabilities(probabilities: Dict[str, float]) -> List[tuple]:
    """
    Urutkan probabilitas dari tinggi ke rendah.
    """
    return sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

def prepare_recommendation_payload(record: Dict) -> Tuple[str, str, Dict, List[str], Dict]:
    """
    Mengambil element penting dari record:
    - model_name, prediction, probabilities, sorted_labels, inputs
    """
    model_name = record.get("Model", "unknown")
    prediction = record.get("Prediction", "")
    probabilities = record.get("Probabilities", {})
    inputs = record.get("Inputs", {})
    sorted_probs = sort_probabilities(probabilities)
    sorted_labels = [label for label, _ in sorted_probs]
    return model_name, prediction, probabilities, sorted_labels, inputs

