import React from 'react';
import useVendingStore from './store/vendingStore';
import PatientInfoForm from './components/PatientInfoForm';
import VoiceInput from './components/VoiceInput';
import RecommendationView from './components/RecommendationView';
import PrescriptionView from './components/PrescriptionView';
import ReceiptView from './components/ReceiptView';
import './App.css';

function App() {
  const { currentStep } = useVendingStore();

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 'patient-info':
        return <PatientInfoForm />;
      case 'voice-input':
        return <VoiceInput />;
      case 'recommendation':
        return <RecommendationView />;
      case 'prescription':
        return <PrescriptionView />;
      case 'receipt':
        return <ReceiptView />;
      default:
        return <PatientInfoForm />;
    }
  };

  return (
    <div className="App">
      {renderCurrentStep()}
    </div>
  );
}

export default App;
