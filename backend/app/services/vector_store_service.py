"""
Vector Store Service for medical knowledge retrieval.
This service handles embedding generation and semantic search for medications and symptoms.
"""

import pickle
from typing import List, Dict, Optional
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.models.medication import Medication
from app.models.symptom import Symptom


class MedicalVectorStore:
    """Vector store for medical knowledge using FAISS and SentenceTransformers."""
    
    def __init__(self, embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", vector_store_path: str = "data/vector_stores"):
        """
        Initialize the medical vector store.
        
        Args:
            embedding_model_name: Pre-trained embedding model name for multilingual support
            vector_store_path: Path to store vector indices
        """
        self.embedding_model_name = embedding_model_name
        self.vector_store_path = Path(vector_store_path)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={'device': 'cpu'}
        )
        
        # Vector store instances
        self.medication_store: Optional[FAISS] = None
        self.symptom_store: Optional[FAISS] = None
        self.knowledge_store: Optional[FAISS] = None
        
        # Metadata storage
        self.medication_metadata: Dict[int, Dict] = {}
        self.symptom_metadata: Dict[int, Dict] = {}
        
        print(f"Initialized MedicalVectorStore with model: {embedding_model_name}")
    
    def create_medication_embeddings(self, medications: List[Medication]) -> None:
        """
        Create vector embeddings for medications.
        
        Args:
            medications: List of medication objects from database
        """
        if not medications:
            print("No medications provided for embedding creation")
            return
        
        documents = []
        metadata_list = []
        
        for idx, med in enumerate(medications):
            # Create comprehensive text representation for each medication
            med_text = self._create_medication_text(med)
            
            # Create document
            doc = Document(
                page_content=med_text,
                metadata={
                    "id": med.id,
                    "name": med.name,
                    "active_ingredient": med.active_ingredient,
                    "treatment_class": med.treatment_class,
                    "is_supporting": med.is_supporting,
                    "stock": med.stock,
                    "type": "medication"
                }
            )
            
            documents.append(doc)
            metadata_list.append(doc.metadata)
            
            # Store detailed metadata
            self.medication_metadata[idx] = {
                "id": med.id,
                "name": med.name,
                "active_ingredient": med.active_ingredient,
                "form": med.form,
                "unit_type": med.unit_type,
                "unit_price": med.unit_price,
                "stock": med.stock,
                "side_effects": med.side_effects,
                "max_per_day": med.max_per_day,
                "is_supporting": med.is_supporting,
                "treatment_class": med.treatment_class,
                "contraindications": med.contraindications,
                "allergy_tags": med.allergy_tags or []
            }
        
        # Create FAISS vector store
        self.medication_store = FAISS.from_documents(documents, self.embeddings)
        
        # Save to disk
        self._save_medication_store()
        
        print(f"Created medication embeddings for {len(medications)} medications")
    
    def create_symptom_embeddings(self, symptoms: List[Symptom]) -> None:
        """
        Create vector embeddings for symptoms.
        
        Args:
            symptoms: List of symptom objects from database
        """
        if not symptoms:
            print("No symptoms provided for embedding creation")
            return
        
        documents = []
        
        for idx, symptom in enumerate(symptoms):
            # Create text representation for symptom
            symptom_text = f"Triệu chứng: {symptom.name}"
            
            doc = Document(
                page_content=symptom_text,
                metadata={
                    "id": symptom.id,
                    "name": symptom.name,
                    "type": "symptom"
                }
            )
            
            documents.append(doc)
            self.symptom_metadata[idx] = {
                "id": symptom.id,
                "name": symptom.name
            }
        
        # Create FAISS vector store
        self.symptom_store = FAISS.from_documents(documents, self.embeddings)
        
        # Save to disk
        self._save_symptom_store()
        
        print(f"Created symptom embeddings for {len(symptoms)} symptoms")
    
    def _create_medication_text(self, med: Medication) -> str:
        """Create comprehensive text representation for medication."""
        text_parts = [
            f"Tên thuốc: {med.name}",
            f"Hoạt chất: {med.active_ingredient}",
            f"Nhóm điều trị: {med.treatment_class}",
            f"Dạng bào chế: {med.form}",
        ]
        
        if med.side_effects:
            text_parts.append(f"Tác dụng phụ: {med.side_effects}")
        
        if med.contraindications:
            text_parts.append(f"Chống chỉ định: {med.contraindications}")
        
        if med.allergy_tags:
            text_parts.append(f"Thành phần dị ứng: {', '.join(med.allergy_tags)}")
        
        text_parts.append(f"Loại thuốc: {'hỗ trợ' if med.is_supporting else 'chính'}")
        
        return " | ".join(text_parts)
    
    def search_relevant_medications(self, symptoms: str, k: int = 10, filter_in_stock: bool = True, exclude_allergies: List[str] = None) -> List[Dict]:
        """
        Search for relevant medications based on symptoms.
        
        Args:
            symptoms: Patient symptoms string
            k: Number of top results to return
            filter_in_stock: Only return medications in stock
            exclude_allergies: List of allergic substances to exclude
            
        Returns:
            List of relevant medication metadata
        """
        if not self.medication_store:
            print("Medication store not initialized")
            return []
        
        exclude_allergies = exclude_allergies or []
        
        try:
            # Perform semantic search
            search_results = self.medication_store.similarity_search_with_score(
                query=f"Điều trị triệu chứng: {symptoms}",
                k=k * 2  # Get more results for filtering
            )
            
            relevant_meds = []
            for doc, score in search_results:
                med_id = doc.metadata["id"]
                
                # Find metadata by medication ID
                med_metadata = None
                for metadata in self.medication_metadata.values():
                    if metadata["id"] == med_id:
                        med_metadata = metadata.copy()
                        med_metadata["relevance_score"] = float(1 - score)  # Convert distance to similarity
                        break
                
                if not med_metadata:
                    continue
                
                # Apply filters
                if filter_in_stock and med_metadata["stock"] <= 0:
                    continue
                
                # Check allergies
                if exclude_allergies and med_metadata.get("allergy_tags"):
                    if any(allergy.lower() in [tag.lower() for tag in med_metadata["allergy_tags"]] 
                           for allergy in exclude_allergies):
                        continue
                
                relevant_meds.append(med_metadata)
                
                if len(relevant_meds) >= k:
                    break
            
            return relevant_meds
            
        except Exception as e:
            print(f"Error in medication search: {e}")
            return []
    
    def search_similar_symptoms(self, symptoms: str, k: int = 5) -> List[Dict]:
        """
        Search for similar symptoms in the database.
        
        Args:
            symptoms: Input symptoms string
            k: Number of similar symptoms to return
            
        Returns:
            List of similar symptom metadata
        """
        if not self.symptom_store:
            print("Symptom store not initialized")
            return []
        
        try:
            search_results = self.symptom_store.similarity_search_with_score(
                query=symptoms,
                k=k
            )
            
            similar_symptoms = []
            for doc, score in search_results:
                symptom_data = {
                    "id": doc.metadata["id"],
                    "name": doc.metadata["name"],
                    "similarity_score": float(1 - score)
                }
                similar_symptoms.append(symptom_data)
            
            return similar_symptoms
            
        except Exception as e:
            print(f"Error in symptom search: {e}")
            return []
    
    def load_existing_stores(self) -> bool:
        """
        Load existing vector stores from disk.
        
        Returns:
            True if stores loaded successfully, False otherwise
        """
        try:
            # Load medication store
            med_store_path = self.vector_store_path / "medication_store"
            med_metadata_path = self.vector_store_path / "medication_metadata.pkl"
            
            if med_store_path.exists() and med_metadata_path.exists():
                self.medication_store = FAISS.load_local(
                    str(med_store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                with open(med_metadata_path, 'rb') as f:
                    self.medication_metadata = pickle.load(f)
                
                print("Loaded existing medication vector store")
            
            # Load symptom store
            symptom_store_path = self.vector_store_path / "symptom_store"
            symptom_metadata_path = self.vector_store_path / "symptom_metadata.pkl"
            
            if symptom_store_path.exists() and symptom_metadata_path.exists():
                self.symptom_store = FAISS.load_local(
                    str(symptom_store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                with open(symptom_metadata_path, 'rb') as f:
                    self.symptom_metadata = pickle.load(f)
                
                print("Loaded existing symptom vector store")
            
            return True
            
        except Exception as e:
            print(f"Error loading existing stores: {e}")
            return False
    
    def _save_medication_store(self) -> None:
        """Save medication vector store to disk."""
        if self.medication_store:
            med_store_path = self.vector_store_path / "medication_store"
            self.medication_store.save_local(str(med_store_path))
            
            # Save metadata
            med_metadata_path = self.vector_store_path / "medication_metadata.pkl"
            with open(med_metadata_path, 'wb') as f:
                pickle.dump(self.medication_metadata, f)
    
    def _save_symptom_store(self) -> None:
        """Save symptom vector store to disk."""
        if self.symptom_store:
            symptom_store_path = self.vector_store_path / "symptom_store"
            self.symptom_store.save_local(str(symptom_store_path))
            
            # Save metadata
            symptom_metadata_path = self.vector_store_path / "symptom_metadata.pkl"
            with open(symptom_metadata_path, 'wb') as f:
                pickle.dump(self.symptom_metadata, f)
    
    def get_treatment_context(self, symptoms: str, patient_allergies: List[str] = None) -> str:
        """
        Get treatment context based on symptoms using vector search.
        
        Args:
            symptoms: Patient symptoms
            patient_allergies: Patient allergies to exclude
            
        Returns:
            Formatted context string for AI prompt
        """
        relevant_meds = self.search_relevant_medications(
            symptoms=symptoms,
            k=8,
            filter_in_stock=True,
            exclude_allergies=patient_allergies or []
        )
        
        if not relevant_meds:
            return ""
        
        context_parts = ["\n--- Thuốc được khuyến nghị dựa trên vector search ---"]
        
        for med in relevant_meds:
            context_parts.append(
                f"• {med['name']} - "
                f"{med['treatment_class']} - "
                f"Độ liên quan: {med['relevance_score']:.2f}"
            )
        
        return "\n".join(context_parts)


# Global vector store instance
medical_vector_store = MedicalVectorStore() 