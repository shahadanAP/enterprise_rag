from langchain_community.document_loaders import PyPDFDirectoryLoader

loader  = PyPDFDirectoryLoader("docs")

docs = loader.load()

print(f"loaded {len(docs)} page document")
print(docs[0].metadata)