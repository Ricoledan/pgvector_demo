import getpass
import os
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

loader = TextLoader("documents/example.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db = PGVector.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name="kendrick_lamar_lyric_test",
    connection_string=PGVector.connection_string_from_db_params(
        driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
        host=os.environ.get("PGVECTOR_HOST", "localhost"),
        port=int(os.environ.get("PGVECTOR_PORT", "5432")),
        database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
        user=os.environ.get("PGVECTOR_USER", "user"),
        password=os.environ.get("PGVECTOR_PASSWORD", "pwd"),
    ),
)

query = ""
docs_with_score = db.similarity_search_with_score(query)

for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
