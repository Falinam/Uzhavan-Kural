import faiss
from sentence_transformers import SentenceTransformer
import requests
import os
import logging
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TamilFarmingAssistant:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.load_knowledge_base()
        self.load_model()
        self.load_faiss_index()
    
    def load_knowledge_base(self):
        """Load agricultural knowledge base"""
        try:
            file_path = os.path.join(self.base_dir, "agri_knowledge.txt")
            with open(file_path, encoding="utf-8") as f:
                self.docs = f.read().split("\n")
            logger.info(f"Loaded {len(self.docs)} knowledge documents")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            self.docs = []
    
    def load_model(self):
        """Load sentence transformer model"""
        try:
            self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def load_faiss_index(self):
        """Load FAISS index"""
        try:
            index_path = os.path.join(self.base_dir, "agri_index.faiss")
            self.index = faiss.read_index(index_path)
            logger.info("FAISS index loaded successfully")
        except Exception as e:
            logger.error(f"Error loading FAISS index: {e}")
            # Create new index if doesn't exist
            self.create_new_index()
    
    def create_new_index(self):
        """Create new FAISS index from documents"""
        if self.docs:
            logger.info("Creating new FAISS index...")
            embeddings = self.embed_model.encode(self.docs)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings)
            
            # Save the index
            index_path = os.path.join(self.base_dir, "agri_index.faiss")
            faiss.write_index(self.index, index_path)
            logger.info("New FAISS index created and saved")
    
    def generate_with_ollama(self, prompt: str) -> str:
        """Generate response using Ollama"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 150
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return "Error generating response. Please try again."
                
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama. Make sure it's running.")
            return "Ollama service is not available. Please start Ollama."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Error generating response."
    
    def query(self, question: str, top_k: int = 5) -> Dict:
        """Main query function"""
        try:
            # 1️⃣ Retrieve relevant documents
            q_embed = self.embed_model.encode([question])
            D, I = self.index.search(q_embed, min(top_k, len(self.docs)))
            
            retrieved_docs = [self.docs[i] for i in I[0] if i < len(self.docs)]
            context = "\n\n".join(retrieved_docs)
            
            # 2️⃣ Agricultural prompt in Tamil context
            prompt = f"""You are an agricultural assistant helping Tamil farmers. 
Use the context to answer the question in simple language.

Rules:
- Give maximum 3 short sentences
- Use simple, practical language
- Focus on actionable solutions
- Include specific quantities if mentioned in context
- No bullet points or formatting

Context:
{context}

Question:
{question}

Answer:"""
            
            # 3️⃣ Generate answer
            answer = self.generate_with_ollama(prompt)
            
            return {
                "success": True,
                "answer": answer,
                "context": retrieved_docs,
                "confidence": float(1 - D[0][0] / 100) if D[0][0] else 0
            }
            
        except Exception as e:
            logger.error(f"Error in query: {e}")
            return {
                "success": False,
                "answer": "Sorry, I couldn't process your question. Please try again.",
                "error": str(e)
            }

# Global instance
assistant = TamilFarmingAssistant()

def query_rag(question: str) -> str:
    """Legacy function for compatibility"""
    result = assistant.query(question)
    return result["answer"]
