def get_disease(symptoms):

    if "fever" in symptoms:
        return {
            "disease": "Fever Disease",
            "advice": "Consult vet"
        }

    return {
        "disease": "Unknown",
        "advice": "Monitor animal"
    }