import os
import qdrant_client
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant


class qdrant():

    def __init__(self, collection_name, qdrant_url, qdrant_api_key):
        self.collection_name = collection_name
        try:
            client = qdrant_client.QdrantClient(
                qdrant_url, api_key=qdrant_api_key)

            #　創造 collection

            vectors_config = qdrant_client.http.models.VectorParams(
                size=1536,  # 這裡的 size 是 for OpenAI
                distance=qdrant_client.http.models.Distance.COSINE)

            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=vectors_config,
            )
            print(f'Collection: {collection_name} created.')
        except:
            print(f'Collection: {collection_name} is exists.')

    # 將聊天歷史紀錄加入向量庫前的準備(切割文字區塊)
    def getChunks(
        self,
        text,
    ):
        text_splitter = CharacterTextSplitter(separator="\n",
                                              chunk_size=500,
                                              chunk_overlap=50,
                                              length_function=len)
        chunks = text_splitter.split_text(text)
        return chunks

    def setVectorStore(self, openai_api_key):

        client = qdrant_client.QdrantClient(
            os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

        self.vector_store = Qdrant(
            client=client,
            collection_name=self.collection_name,
            embeddings=embeddings,
        )
