import { create } from 'zustand';

const useVendingStore = create((set, get) => ({
  // Current step in the workflow
  currentStep: 'patient-info', // 'patient-info' | 'voice-input' | 'recommendation' | 'prescription' | 'receipt'
  
  // Patient information
  patientData: {
    symptoms: '',
    gender: '',
    age: null,
    height: null,
    weight: null,
    allergies: [],
    underlying_conditions: [],
    current_medications: []
  },
  
  // Voice input state
  isRecording: false,
  transcribedText: '',
  
  // API responses
  recommendation: null,
  prescription: null,
  
  // Loading states
  isLoading: false,
  error: null,
  
  // Actions
  setCurrentStep: (step) => set({ currentStep: step }),
  
  setPatientData: (data) => set((state) => ({
    patientData: { ...state.patientData, ...data }
  })),
  
  setIsRecording: (recording) => set({ isRecording: recording }),
  
  setTranscribedText: (text) => set({ transcribedText: text }),
  
  setRecommendation: (recommendation) => set({ recommendation }),
  
  setPrescription: (prescription) => set({ prescription }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),
  
  // Reset all data (for new patient)
  resetAll: () => set({
    currentStep: 'patient-info',
    patientData: {
      symptoms: '',
      gender: '',
      age: null,
      height: null,
      weight: null,
      allergies: [],
      underlying_conditions: [],
      current_medications: []
    },
    isRecording: false,
    transcribedText: '',
    recommendation: null,
    prescription: null,
    isLoading: false,
    error: null
  }),
  
  // Navigate to next step
  nextStep: () => {
    const { currentStep } = get();
    const stepOrder = ['patient-info', 'voice-input', 'recommendation', 'prescription', 'receipt'];
    const currentIndex = stepOrder.indexOf(currentStep);
    if (currentIndex < stepOrder.length - 1) {
      set({ currentStep: stepOrder[currentIndex + 1] });
    }
  },
  
  // Navigate to previous step
  previousStep: () => {
    const { currentStep } = get();
    const stepOrder = ['patient-info', 'voice-input', 'recommendation', 'prescription', 'receipt'];
    const currentIndex = stepOrder.indexOf(currentStep);
    if (currentIndex > 0) {
      set({ currentStep: stepOrder[currentIndex - 1] });
    }
  },
  
  // Update symptoms from voice input
  updateSymptomsFromVoice: (symptoms) => set((state) => ({
    patientData: { ...state.patientData, symptoms }
  })),
  
  // Validation helpers
  isPatientDataValid: () => {
    const { patientData } = get();
    return patientData.gender && 
           patientData.age && 
           patientData.height && 
           patientData.weight;
  },
  
  isSymptomsValid: () => {
    const { patientData } = get();
    return patientData.symptoms && patientData.symptoms.trim().length > 0;
  }
}));

export default useVendingStore; 