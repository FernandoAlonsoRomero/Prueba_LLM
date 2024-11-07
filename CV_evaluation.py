import os
import json
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from huggingface_hub import login

login(token="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")



def evaluar_cv(oferta_trabajo, cv_candidato):
    
    prompt_template = """
    Necesito que evalúes la experiencia de candidatos para un puesto de trabajo concreto a partir de su CV.
    Instrucciones:
    1. Genera una puntuación de 0 a 100 basada en la experiencia laboral relevante del candidato para la oferta de trabajo.
    2. Lista las experiencias relevantes en formato JSON, incluyendo 'puesto', 'empresa' y 'duracion' de cada experiencia relevante.
    3. Proporciona una breve explicación de la puntuación, justificando por qué cada experiencia es relevante.
    Salida:
    Devuelve la respuesta en JSON con los siguientes campos:
    {{
      "puntuacion": int,
      "experiencias_relacionadas": [{{"puesto": str, "empresa": str, "duracion": str}}],
      "descripcion": str
    }}
    Oferta de trabajo: {oferta_trabajo}
    CV del candidato:
    {cv}
    """

    prompt = PromptTemplate(input_variables=["oferta_trabajo", "cv"], template=prompt_template)

    prompt_text = prompt.format(oferta_trabajo=oferta_trabajo, cv=cv_candidato)

    #PARA GPT-3.5 DE PAGO
    os.environ["OPENAI_API_KEY"] = "tu_api_key_aqui"
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5)
    print(prompt_text)
    response = llm(prompt_text)
    
    try:
        resultado_json = json.loads(response)
        return resultado_json

    except json.JSONDecodeError:
        print("Error al decodificar la respuesta en JSON")
        return None


if __name__=="__main__":

    # Ejemplo de uso
    oferta_trabajo = "Cajero supermercado Dia"
    cv_candidato = "CV.pdf"

    reader = PdfReader(cv_candidato)
    cv = ""
    for page in reader.pages:
        cv += page.extract_text()

    resultado = evaluar_cv(oferta_trabajo, cv)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

