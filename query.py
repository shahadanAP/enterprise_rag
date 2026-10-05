from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv # to read the env file
import psycopg2
import time


load_dotenv() #reads env file


embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2", 
model_kwargs ={"device": "cpu"}, encode_kwargs = {"normalize_embeddings": True})

chormaChunks = Chroma(persist_directory = "chroma_db", embedding_function = embeddings)

query = "Who is the president of usa"


#start the timer for latency mesuremnt
startTime = time.perf_counter()

results = chormaChunks.similarity_search_with_score(query, k=5)

context_parts = []
sourceList = []

for doc, score in results:
    print(f"Score = {score}")
    print(f"Source = {doc.metadata['source']}")
    print(f"Page Lable = {doc.metadata['page_label']}")

    # label each chunk with where it came from, then its text
    context_parts.append(
        f"[Source: {doc.metadata['source']}, page {doc.metadata['page_label']}]\n{doc.page_content}"
    )
    sourceList.append( f"Source: {doc.metadata['source']}, page:{doc.metadata['page_label']}")

context = "\n\n".join(context_parts) 

#print(f"page contents from start up to 200 charecter{doc.page_content[:200]}")



# defining the llm model
llm = ChatGroq(model = "openai/gpt-oss-20b", temperature=0)

prompt = f"""Answer the question using only the context below. Cite the source file and page for every fact you use.
If you cannot find the answer in the context, reply with exactly: I don't know


Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)  # send the prompt to the LLM
print("\nANSWER:\n", response.content)



endTime = time.perf_counter()
#finding the elapsed time in milli seconds
latency_ms =  round((endTime - startTime)*1000)
print(latency_ms)


trimmedAiAnswer = response.content.strip()
confidence = ""
if trimmedAiAnswer == "I don't know":
    confidence = "low"
else:
    confidence = "high"
print(confidence)




#print(f"source{sourceList}")
#connecting to pstgresql server
sources = "; ".join(sourceList)
print(sources)



try:

    connection = psycopg2.connect(
        database = "enterprise_rag"
    )

    #cursor object to excute sql command
    cursor = connection.cursor()

    cursor.execute("INSERT INTO query_log (question, answer, confidence, sources, latency_ms ) VALUES (%s,%s,%s,%s,%s);", (query, trimmedAiAnswer, confidence, sources , latency_ms))
    connection.commit()

except Exception as error:
        print(f"Error getting the answer form llm {error}")

finally:
    if "cursor" in locals() and cursor:
        cursor.close()

    if "connection" in locals() and connection:
        connection.close()
        print("Databse connection closed")

