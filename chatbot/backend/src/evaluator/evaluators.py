# ---------------------------------------
# IMPORTACIONES
# ---------------------------------------
from langsmith import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.chatbot.core_initializer import CoreInitializer
from src.config.config_url import DOCS_URL
from src.chatbot.graph_initializer import GraphInitializer
from src.chatbot.chat_initializer import ChatInitializer

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import nltk
import time

nltk.download("punkt")

# ---------------------------------------
# CONFIGURACIÓN DE RUTAS
# ---------------------------------------
DOCS_PATH = "./docs"  # Carpeta local con documentos
WEB_PATHS = DOCS_URL  # URLs de documentos online

# ---------------------------------------
# INICIALIZACIÓN DEL SISTEMA
# ---------------------------------------
core = CoreInitializer(docs_path=DOCS_PATH, web_paths=WEB_PATHS)
core.initialize()

client = Client()  # Cliente de LangSmith

model_manager = core.model_manager
embedding_manager = core.embedding_manager

chatbot_graph = GraphInitializer(
    model_manager=model_manager, embedding_manager=embedding_manager
)
chatbot_graph.build_graph()

config = {"configurable": {"thread_id": "1"}}
chatbot = ChatInitializer(chatbot_graph=chatbot_graph, config=config)

# ---------------------------------------
# CONFIGURACIÓN DEL MODELO LLM PARA EVALUACIÓN
# ---------------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0.0)


# ---------------------------------------
# MODELO DE SALIDA PARA LA EVALUACIÓN
# ---------------------------------------
class Similarity_Score(BaseModel):
    similarity_score: float = Field(
        description="Semantic similarity score between 0 and 1, where 0 means totally different and 1 means identical."
    )


# ---------------------------------------
# FUNCIÓN PRINCIPAL DEL CHATBOT
# ---------------------------------------
def chatbot_app(inputs: dict) -> dict:
    """Toma una pregunta y devuelve la respuesta del chatbot."""
    question = inputs["question"]
    response = chatbot._chatbot_graph.graph.invoke(
        {"question": question}, chatbot._config
    )
    return {"output": response}


# ---------------------------------------
# PROMPTS
# ---------------------------------------
similarity_prompt = """
Evaluate the semantic similarity between the generated response and the reference answer. 
Respond with a decimal number between 0 and 1, where 0 means "completely different" and 1 means "completely identical".
Please be as precise as possible in your evaluation.

Generated response: {respuesta_generada}
Reference answer: {respuesta_referencia}

RESPOND WITH A DECIMAL NUMBER BETWEEN 0 AND 1.
DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATION.
"""

prompt_template = PromptTemplate(
    input_variables=["respuesta_generada", "respuesta_referencia"],
    template=similarity_prompt,
)

cr_prompt = """
Evaluate the Context Relevance (CR) between the generated response and the retrieved documents. 
The relevance should be rated from 0 to 1, where 0 indicates the response is completely irrelevant to the context provided by the documents, and 1 indicates the response is completely relevant.
Please be rigorous in your evaluation, considering both the content and the relationship between the documents and the generated response.

Generated response: {respuesta}

Retrieved documents:
{documentos}

RESPOND WITH A DECIMAL NUMBER BETWEEN 0 AND 1.
DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATION.
"""

cr_prompt_template = PromptTemplate(
    input_variables=["respuesta", "documentos"], template=cr_prompt
)

f_prompt = """
Evaluate the Faithfulness (F) of the generated response in relation to the retrieved documents. 
Respond with a decimal number between 0 and 1, where 0 means the response is completely incorrect or misleading regarding the documents, and 1 means the response is perfectly faithful to the documents.
Be as precise as possible when evaluating how the response reflects or is based on the retrieved documents.

Generated response: {respuesta}

Retrieved documents:
{documentos}

RESPOND WITH A DECIMAL NUMBER BETWEEN 0 AND 1.
DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATION.
"""

f_prompt_template = PromptTemplate(
    input_variables=["respuesta", "documentos"], template=f_prompt
)

ar_prompt = """
Evaluate the Answer Relevance (AR) in relation to the question and the retrieved documents. 
Respond with a decimal number between 0 and 1, where 0 means the response is completely irrelevant to the question and documents, and 1 means the response is perfectly relevant.
Please be as rigorous as possible in assessing the pertinence of the response with respect to the query and the documents.

Generated response: {respuesta}

Retrieved documents:
{documentos}

RESPOND WITH A DECIMAL NUMBER BETWEEN 0 AND 1.
DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATION.
"""

ar_prompt_template = PromptTemplate(
    input_variables=["respuesta", "documentos"], template=ar_prompt
)


# ---------------------------------------
# EVALUADOR: MÉTRICA BLEU
# ---------------------------------------
def evaluar_bleu(outputs: dict, reference_outputs: dict) -> float:
    """Calcula la puntuación BLEU entre la respuesta generada y la referencia."""
    respuesta = outputs["output"]["answer"]
    referencia = reference_outputs["answer"]

    referencia_tokens = [nltk.word_tokenize(referencia)]
    respuesta_tokens = nltk.word_tokenize(respuesta)

    smoothing = SmoothingFunction().method4
    bleu_score = sentence_bleu(
        referencia_tokens, respuesta_tokens, smoothing_function=smoothing
    )

    print(f"BLEU: {bleu_score}")
    return bleu_score


# ---------------------------------------
# EVALUADOR: MÉTRICA ROUGE-L
# ---------------------------------------
def evaluar_rouge(outputs: dict, reference_outputs: dict) -> float:
    """Calcula la puntuación ROUGE-L entre la respuesta generada y la referencia."""
    respuesta = outputs["output"]["answer"]
    referencia = reference_outputs["answer"]

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(referencia, respuesta)

    rouge_l_f1 = scores["rougeL"].fmeasure
    print(f"ROUGE-L F1: {rouge_l_f1}")
    return rouge_l_f1


# ---------------------------------------
# FUNCIÓN PARA SIMILITUD USANDO LLM
# ---------------------------------------
def calcular_similitud_llm(referencia: str, respuesta: str) -> float:
    """Calcula la similitud semántica entre dos textos usando un LLM como juez."""
    prompt = prompt_template.format(
        respuesta_generada=respuesta, respuesta_referencia=referencia
    )
    result = llm.invoke(prompt)
    try:
        result_text = result.content
        return float(result_text)
    except (ValueError, AttributeError):
        print(f"Error: El modelo devolvió un resultado no numérico: {result}")
        return 0.0


# ---------------------------------------
# EVALUADOR: SIMILITUD LLM
# ---------------------------------------
def evaluar_similitud_llm(outputs: dict, reference_outputs: dict) -> float:
    """Evalúa la similitud entre la respuesta generada y la de referencia usando un LLM."""
    respuesta = outputs["output"]
    referencia = reference_outputs["answer"]
    similitud = calcular_similitud_llm(referencia, respuesta["answer"])

    print(f"Similitud (LLM): {similitud}")
    # print("Respuesta generada:", respuesta["answer"])
    # print("Respuesta de referencia:", referencia)

    return similitud


# =======================================
#  FUNCIÓN PARA CONTEXT RELEVANCE (CR) USANDO LLM
# =======================================
def calcular_cr_llm(respuesta: str, documentos: str) -> float:
    """Evalúa la relevancia del contexto (CR) entre la respuesta generada y los documentos recuperados usando un LLM."""
    prompt = cr_prompt_template.format(respuesta=respuesta, documentos=documentos)
    result = llm.invoke(prompt)
    try:
        result_text = result.content
        return float(result_text)
    except (ValueError, AttributeError):
        print(f"Error: El modelo devolvió un resultado no numérico: {result}")
        return 0.0


# =======================================
#  EVALUADOR: CONTEXT RELEVANCE (CR)
# =======================================
def evaluar_cr(outputs: dict, reference_outputs: dict) -> float:
    """Evalúa la relevancia del contexto (CR) entre la respuesta generada y los documentos recuperados usando un LLM."""
    respuesta = outputs["output"]
    documentos = "\n\n".join([str(doc) for doc in respuesta.get("documents", [])])
    cr_score = calcular_cr_llm(respuesta["answer"], documentos)

    print(f"Context Relevance (CR): {cr_score}")
    # print("Respuesta generada:", respuesta["answer"])
    # print("Documentos recuperados:", documentos)

    return cr_score


# =======================================
#  FUNCIÓN PARA FAITHFULNESS (F) USANDO LLM
# =======================================
def calcular_f_llm(respuesta: str, documentos: str) -> float:
    """Evalúa la fidelidad (F) entre la respuesta generada y los documentos recuperados usando un LLM."""
    prompt = f_prompt_template.format(respuesta=respuesta, documentos=documentos)
    result = llm.invoke(prompt)
    try:
        result_text = result.content
        return float(result_text)
    except (ValueError, AttributeError):
        print(f"Error: El modelo devolvió un resultado no numérico: {result}")
        return 0.0


# =======================================
#  EVALUADOR: FAITHFULNESS (F)
# =======================================
def evaluar_f(outputs: dict, reference_outputs: dict) -> float:
    """Evalúa la fidelidad (F) entre la respuesta generada y los documentos recuperados usando un LLM."""
    respuesta = outputs["output"]
    documentos = "\n\n".join([str(doc) for doc in respuesta.get("documents", [])])
    f_score = calcular_f_llm(respuesta["answer"], documentos)

    print(f"Faithfulness (F): {f_score}")
    # print("Respuesta generada:", respuesta["answer"])
    # print("Documentos recuperados:", documentos)

    return f_score


# =======================================
#  FUNCIÓN PARA ANSWER RELEVANCE (AR) USANDO LLM
# =======================================
def calcular_ar_llm(respuesta: str, documentos: str) -> float:
    """Evalúa la relevancia de la respuesta (AR) entre la respuesta generada y los documentos recuperados usando un LLM."""
    prompt = ar_prompt_template.format(respuesta=respuesta, documentos=documentos)
    result = llm.invoke(prompt)
    try:
        result_text = result.content
        return float(result_text)
    except (ValueError, AttributeError):
        print(f"Error: El modelo devolvió un resultado no numérico: {result}")
        return 0.0


# =======================================
#  EVALUADOR: ANSWER RELEVANCE (AR)
# =======================================
def evaluar_ar(outputs: dict, reference_outputs: dict) -> float:
    """Evalúa la relevancia de la respuesta generada comparándola con los documentos recuperados usando AR."""
    respuesta = outputs["output"]
    documentos = "\n\n".join([str(doc) for doc in respuesta.get("documents", [])])
    ar_score = calcular_ar_llm(respuesta=respuesta["answer"], documentos=documentos)

    print(f"Answer Relevance (AR): {ar_score}")
    # print("Respuesta generada:", respuesta["answer"])
    # print("Documentos recuperados:", documentos)

    time.sleep(30)
    return ar_score


# ---------------------------------------
# EJECUCIÓN DE LA EVALUACIÓN
# ---------------------------------------
results = client.evaluate(
    chatbot_app,
    data="preguntas-chatbot",
    evaluators=[
        evaluar_similitud_llm,
        evaluar_bleu,
        evaluar_rouge,
        evaluar_cr,
        evaluar_f,
        evaluar_ar,
    ],
)


# ---------------------------------------
# RESULTADOS
# ---------------------------------------
print(results)
