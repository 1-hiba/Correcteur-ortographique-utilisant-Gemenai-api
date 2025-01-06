import gradio as gr
import google.generativeai as genai
import json

# Configuration de Gemini
API_KEY = "AIzaSyCQ0s9dMKCyRJThcGUCS1prpIwtN9hBlMA" # Remplacez par votre clé API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Fonction pour analyser et corriger le texte
def corriger_texte(texte):
    prompt = f"""
    Vous êtes un assistant qui aide à améliorer les textes en fournissant des corrections grammaticales, des suggestions de style, des ajustements de ton, et des suggestions générales. Voici quelques exemples de corrections et suggestions :

    1. Correction grammaticale:
       Texte: "Il va au marché pour acheter des pomme."
       Correction: {{"corrections": [{{"erreur": "pomme", "correction": "pommes", "type": "orthographe"}}]}}

    2. Suggestion de style (lisibilité):
       Texte: "Le rapport était long et difficile à comprendre."
       Suggestion: {{"suggestions": [{{"original": "long et difficile à comprendre", "suggestion": "complexe et peu clair", "type": "lisibilité"}}]}}

    3. Ajustement de ton:
       Texte: "Je pense que vous avez tort."
       Ajustement: {{"ajustements": [{{"original": "vous avez tort", "ajustement": "il semble y avoir une erreur", "type": "ton"}}]}}

    4. Suggestion générale:
       Texte: "Le projet est bien mais pourrait être amélioré."
       Suggestion: {{"suggestions": [{{"original": "pourrait être amélioré", "suggestion": "pourrait bénéficier de quelques améliorations", "type": "général"}}]}}

    Analyse le texte suivant et retourne les corrections et suggestions en JSON:
    "{texte}"

    Format: {{
        "corrections": [
            {{"erreur": "mot_incorrect", 
              "correction": "suggestion",
              "type": "orthographe/grammaire"}}
        ],
        "suggestions": [
            {{"original": "texte_original", 
              "suggestion": "suggestion_améliorée",
              "type": "lisibilité/consistance"}}
        ],
        "ajustements": [
            {{"original": "texte_original", 
              "ajustement": "texte_ajusté",
              "type": "ton"}}
        ],
        "suggestions_generales": [
            {{"original": "texte_original", 
              "suggestion": "suggestion_améliorée",
              "type": "général"}}
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        return formater_resultat(result)
    except Exception as e:
        return f"Erreur : {str(e)}"


# Fonction pour formater le résultat en texte lisible
def formater_resultat(result):
    formatted_text = ""

    if "corrections" in result:
        formatted_text += "**Corrections grammaticales:**\n"
        for corr in result["corrections"]:
            formatted_text += f"- Erreur: {corr['erreur']}\n"
            formatted_text += f"  Correction: {corr['correction']}\n"
            formatted_text += f"  Type: {corr['type']}\n\n"

    if "suggestions" in result:
        formatted_text += "**Suggestions de style:**\n"
        for sugg in result["suggestions"]:
            formatted_text += f"- Original: {sugg['original']}\n"
            formatted_text += f"  Suggestion: {sugg['suggestion']}\n"
            formatted_text += f"  Type: {sugg['type']}\n\n"

    if "ajustements" in result:
        formatted_text += "**Ajustements de ton:**\n"
        for adj in result["ajustements"]:
            formatted_text += f"- Original: {adj['original']}\n"
            formatted_text += f"  Ajustement: {adj['ajustement']}\n"
            formatted_text += f"  Type: {adj['type']}\n\n"

    if "suggestions_generales" in result:
        formatted_text += "**Suggestions générales:**\n"
        for sugg in result["suggestions_generales"]:
            formatted_text += f"- Original: {sugg['original']}\n"
            formatted_text += f"  Suggestion: {sugg['suggestion']}\n"
            formatted_text += f"  Type: {sugg['type']}\n\n"

    return formatted_text if formatted_text else "Aucune correction ou suggestion trouvée."


# Interface Gradio
interface = gr.Interface(
    fn=corriger_texte,  # Fonction à appeler
    inputs="text",  # Champ de saisie de texte
    outputs="text",  # Champ de sortie de texte
    title="Correcteur de Texte avec Gemini",
    description="Entrez un texte pour obtenir des corrections grammaticales, des suggestions de style, des ajustements de ton, et des suggestions générales."
)

# Lancement de l'interface
interface.launch()