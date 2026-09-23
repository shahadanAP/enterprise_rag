from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

loader  = PyPDFDirectoryLoader("docs")

docs = loader.load()

#print(f"loaded {len(docs)} page document")
#print(docs[0].metadata)



splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
chunks = splitter.split_documents(docs)
#print(len(chunks))
#print(chunks[10].page_content)


embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2", 
model_kwargs ={"device": "cpu"}, encode_kwargs = {"normalize_embeddings": True})

chormaChunks = Chroma.from_documents(documents = chunks, embedding = embeddings, 
persist_directory = "chroma_db")

storedItems = chormaChunks._collection.count()
print(storedItems)