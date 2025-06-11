"""
Vector Store Manager for initializing and managing medical vector stores.
This service handles the lifecycle of vector stores and database synchronization.
"""

from typing import List
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.medication import Medication
from app.models.symptom import Symptom
from app.services.vector_store_service import medical_vector_store


class VectorStoreManager:
    """Manager for medical vector store operations."""
    
    def __init__(self):
        """Initialize the vector store manager."""
        self.vector_store = medical_vector_store
        self.initialized = False
    
    async def initialize(self, db: Session = None) -> bool:
        """
        Initialize vector stores from database.
        
        Args:
            db: Database session, if not provided will create one
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Try loading existing stores first
            if self.vector_store.load_existing_stores():
                print("Vector stores loaded from existing files")
                self.initialized = True
                return True
            
            # Create new stores from database
            if db is None:
                # Get a database session
                db_gen = get_db()
                db = next(db_gen)
                try:
                    success = await self._create_stores_from_db(db)
                finally:
                    db.close()
            else:
                success = await self._create_stores_from_db(db)
            
            if success:
                self.initialized = True
                print("Vector stores initialized successfully")
            else:
                print("Failed to initialize vector stores")
            
            return success
            
        except Exception as e:
            print(f"Error initializing vector stores: {e}")
            return False
    
    async def _create_stores_from_db(self, db: Session) -> bool:
        """Create vector stores from database data."""
        try:
            # Get all medications from database
            medications = db.query(Medication).all()
            if medications:
                self.vector_store.create_medication_embeddings(medications)
                print(f"Created embeddings for {len(medications)} medications")
            else:
                print("No medications found in database")
            
            # Get all symptoms from database
            symptoms = db.query(Symptom).all()
            if symptoms:
                self.vector_store.create_symptom_embeddings(symptoms)
                print(f"Created embeddings for {len(symptoms)} symptoms")
            else:
                print("No symptoms found in database")
            
            return len(medications) > 0 or len(symptoms) > 0
            
        except Exception as e:
            print(f"Error creating stores from database: {e}")
            return False
    
    async def rebuild_stores(self, db: Session = None) -> bool:
        """
        Rebuild vector stores from scratch using current database data.
        
        Args:
            db: Database session
            
        Returns:
            True if rebuild successful, False otherwise
        """
        try:
            print("Rebuilding vector stores from database...")
            
            if db is None:
                db_gen = get_db()
                db = next(db_gen)
                try:
                    success = await self._create_stores_from_db(db)
                finally:
                    db.close()
            else:
                success = await self._create_stores_from_db(db)
            
            if success:
                self.initialized = True
                print("Vector stores rebuilt successfully")
            
            return success
            
        except Exception as e:
            print(f"Error rebuilding vector stores: {e}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if vector stores are initialized."""
        return self.initialized and (
            self.vector_store.medication_store is not None or 
            self.vector_store.symptom_store is not None
        )
    
    def get_medication_recommendations(self, symptoms: str, allergies: List[str] = None, k: int = 10) -> List[dict]:
        """
        Get medication recommendations using vector search.
        
        Args:
            symptoms: Patient symptoms
            allergies: Patient allergies to exclude
            k: Number of recommendations to return
            
        Returns:
            List of medication recommendations
        """
        if not self.is_initialized():
            print("Vector stores not initialized")
            return []
        
        return self.vector_store.search_relevant_medications(
            symptoms=symptoms,
            k=k,
            filter_in_stock=True,
            exclude_allergies=allergies or []
        )
    
    def get_vector_context_for_prompt(self, symptoms: str, allergies: List[str] = None) -> str:
        """
        Get vector search context for AI prompt enhancement.
        
        Args:
            symptoms: Patient symptoms
            allergies: Patient allergies
            
        Returns:
            Formatted context string for AI prompt
        """
        if not self.is_initialized():
            return ""
        
        return self.vector_store.get_treatment_context(
            symptoms=symptoms,
            patient_allergies=allergies or []
        )
    
    async def update_medication_embeddings(self, medications: List[Medication]) -> bool:
        """
        Update vector store with new/modified medications.
        
        Args:
            medications: List of medications to add/update
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            if not medications:
                return True
            
            self.vector_store.create_medication_embeddings(medications)
            return True
            
        except Exception as e:
            print(f"Error updating medication embeddings: {e}")
            return False
    
    def get_store_stats(self) -> dict:
        """
        Get statistics about the vector stores.
        
        Returns:
            Dictionary with store statistics
        """
        stats = {
            "initialized": self.initialized,
            "medication_store_exists": self.vector_store.medication_store is not None,
            "symptom_store_exists": self.vector_store.symptom_store is not None,
            "medication_count": len(self.vector_store.medication_metadata),
            "symptom_count": len(self.vector_store.symptom_metadata)
        }
        
        return stats


# Global vector store manager instance
vector_store_manager = VectorStoreManager() 