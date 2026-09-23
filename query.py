from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv # to read the env file


load_dotenv() #reads env file


embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2", 
model_kwargs ={"device": "cpu"}, encode_kwargs = {"normalize_embeddings": True})

chormaChunks = Chroma(persist_directory = "chroma_db", embedding_function = embeddings)

query = "What must happen before an automated decision system goes into production?"

results = chormaChunks.similarity_search_with_score(query, k=5)

context_parts = []

for doc, score in results:
    print(f"Score = {score}")
    print(f"Source = {doc.metadata["source"]}")
    print(f"Page Lable = {doc.metadata["page_label"]}")

    # label each chunk with where it came from, then its text
    context_parts.append(
        f"[Source: {doc.metadata['source']}, page {doc.metadata['page_label']}]\n{doc.page_content}"
    )

context = "\n\n".join(context_parts) 

#print(f"page contents from start up to 200 charecter{doc.page_content[:200]}")



# defining the llm model
llm = ChatGroq(model = "openai/gpt-oss-20b")


prompt = f"""Answer the question using only the context below. Cite the source file for and page for every you use.
If you cannot fidn the answer in the context, jst say "I dont know"

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)  # send the prompt to the LLM
print("\nANSWER:\n", response.content)

