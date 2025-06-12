import React, { useState, useEffect } from 'react';
import { useSpeechSynthesis, useSpeechRecognition } from 'react-speech-kit';
import { Mic, MicOff, Volume2, ArrowLeft, ArrowRight } from 'lucide-react';
import useVendingStore from '../store/vendingStore';

const VoiceInput = () => {
  const { 
    setPatientData, 
    previousStep, 
    nextStep, 
    isRecording, 
    setIsRecording,
    setTranscribedText 
  } = useVendingStore();

  const [currentSection, setCurrentSection] = useState('symptoms');
  const [voicePrompts, setVoicePrompts] = useState({
    symptoms: '',
    allergies: '',
    underlying_conditions: '',
    current_medications: ''
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [recognitionInstance, setRecognitionInstance] = useState(null);

  const { cancel, speaking } = useSpeechSynthesis();
  const { listening, stop } = useSpeechRecognition({
    onResult: (result) => {
      setTranscribedText(result);
      setVoicePrompts(prev => ({
        ...prev,
        [currentSection]: result
      }));
    },
  });

  // Custom listen function with Vietnamese language support
  const listenInVietnamese = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.lang = 'vi-VN'; // Set Vietnamese language
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        const result = event.results[0][0].transcript;
        setTranscribedText(result);
        setVoicePrompts(prev => ({
          ...prev,
          [currentSection]: result
        }));
        setIsRecording(false);
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setErrorMessage('Lỗi nhận diện giọng nói. Vui lòng thử lại.');
        setIsRecording(false);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognition.start();
      return recognition;
    } else {
      setErrorMessage('Trình duyệt không hỗ trợ nhận diện giọng nói.');
      return null;
    }
  };

  // Voice prompts for each section
  const sectionPrompts = {
    symptoms: "Vui lòng mô tả các triệu chứng bạn đang gặp phải. Ví dụ: đau đầu, sổ mũi, ho, sốt...",
    allergies: "Bạn có bị dị ứng với loại thuốc nào không? Nếu không có, hãy nói 'không có'",
    underlying_conditions: "Bạn có bệnh nền nào không? Ví dụ: cao huyết áp, tiểu đường... Nếu không có, hãy nói 'không có'",
    current_medications: "Bạn hiện đang dùng thuốc gì không? Nếu không có, hãy nói 'không có'"
  };

  const sectionTitles = {
    symptoms: "Triệu chứng",
    allergies: "Dị ứng",
    underlying_conditions: "Bệnh nền",
    current_medications: "Thuốc đang dùng"
  };

  const handleStartListening = () => {
    setIsRecording(true);
    setErrorMessage('');
    setTimeout(() => {
      const recognition = listenInVietnamese();
      setRecognitionInstance(recognition);
    }, 3000);
  };

  const handleStopListening = () => {
    setIsRecording(false);
    if (recognitionInstance) {
      recognitionInstance.stop();
      setRecognitionInstance(null);
    }
    stop();
    cancel();
  };

  const handleNextSection = () => {
    // Clear any previous error message
    setErrorMessage('');
    
    // Validate symptoms section (required)
    if (currentSection === 'symptoms' && (!voicePrompts.symptoms || voicePrompts.symptoms.trim().length === 0)) {
      setErrorMessage('Vui lòng mô tả triệu chứng của bạn trước khi tiếp tục.');
      return;
    }
    
    const sections = ['symptoms', 'allergies', 'underlying_conditions', 'current_medications'];
    const currentIndex = sections.indexOf(currentSection);
    
    if (currentIndex < sections.length - 1) {
      setCurrentSection(sections[currentIndex + 1]);
      setTranscribedText('');
    } else {
      // Save all data and proceed to next step
      saveAllData();
      nextStep();
    }
  };

  const handlePreviousSection = () => {
    const sections = ['symptoms', 'allergies', 'underlying_conditions', 'current_medications'];
    const currentIndex = sections.indexOf(currentSection);
    
    if (currentIndex > 0) {
      setCurrentSection(sections[currentIndex - 1]);
      setTranscribedText(voicePrompts[sections[currentIndex - 1]] || '');
    } else {
      previousStep();
    }
  };

  const saveAllData = () => {
    const processArrayField = (text) => {
      if (!text || text.toLowerCase().includes('không có') || text.toLowerCase().includes('không')) {
        return [];
      }
      return text.split(',').map(item => item.trim()).filter(item => item.length > 0);
    };

    setPatientData({
      symptoms: voicePrompts.symptoms || '',
      allergies: processArrayField(voicePrompts.allergies),
      underlying_conditions: processArrayField(voicePrompts.underlying_conditions),
      current_medications: processArrayField(voicePrompts.current_medications)
    });
  };

  useEffect(() => {
    setIsRecording(listening);
  }, [listening, setIsRecording]);

  const sections = ['symptoms', 'allergies', 'underlying_conditions', 'current_medications'];
  const currentIndex = sections.indexOf(currentSection);
  const isLastSection = currentIndex === sections.length - 1;

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="bg-emerald-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <Mic className="w-8 h-8 text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Nhập Thông Tin Bằng Giọng Nói
          </h1>
          <p className="text-gray-600">
            Bước {currentIndex + 1} / {sections.length}: {sectionTitles[currentSection]}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-xs text-gray-500 mb-2">
            {sections.map((section, index) => (
              <span key={section} className={`${index <= currentIndex ? 'text-emerald-600 font-medium' : ''}`}>
                {sectionTitles[section]}
              </span>
            ))}
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-emerald-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentIndex + 1) / sections.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Current Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            {sectionTitles[currentSection]}
          </h2>
          <p className="text-gray-600 mb-6">
            {sectionPrompts[currentSection]}
          </p>

          {/* Voice Control */}
          <div className="flex justify-center mb-6">
            {!isRecording ? (
              <button
                onClick={handleStartListening}
                className="bg-emerald-600 hover:bg-emerald-700 text-white rounded-full p-6 shadow-lg transition-all transform hover:scale-105"
              >
                <Mic className="w-12 h-12" />
              </button>
            ) : (
              <button
                onClick={handleStopListening}
                className="bg-red-600 hover:bg-red-700 text-white rounded-full p-6 shadow-lg transition-all transform hover:scale-105 animate-pulse"
              >
                <MicOff className="w-12 h-12" />
              </button>
            )}
          </div>

          {/* Status */}
          <div className="text-center mb-6">
            {speaking && (
              <div className="flex items-center justify-center text-emerald-600 mb-2">
                <Volume2 className="w-5 h-5 mr-2" />
                <span>Đang phát âm thanh hướng dẫn...</span>
              </div>
            )}
            {isRecording && (
              <div className="flex items-center justify-center text-emerald-600 mb-2">
                <div className="w-3 h-3 bg-red-500 rounded-full mr-2 animate-pulse"></div>
                <span>Đang ghi âm... Hãy nói vào microphone</span>
              </div>
            )}
          </div>

          {/* Transcribed Text */}
          <div className="bg-gray-50 rounded-lg p-4 min-h-32">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Văn bản đã nhận diện:
            </label>
            <textarea
              value={voicePrompts[currentSection] || ''}
              onChange={(e) => {
                setVoicePrompts(prev => ({
                  ...prev,
                  [currentSection]: e.target.value
                }));
                // Clear error when user starts typing
                if (errorMessage) {
                  setErrorMessage('');
                }
              }}
              className="w-full p-3 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-emerald-500 focus:border-transparent resize-none"
              rows="4"
              placeholder="Văn bản sẽ hiển thị ở đây sau khi bạn nói..."
            />
          </div>

          {/* Error Message */}
          {errorMessage && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm font-medium">{errorMessage}</p>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={handlePreviousSection}
            className="flex items-center px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            {currentIndex === 0 ? 'Quay lại' : 'Phần trước'}
          </button>

          <button
            onClick={handleNextSection}
            className="flex items-center px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
          >
            {isLastSection ? 'Hoàn thành' : 'Phần tiếp theo'}
            <ArrowRight className="w-5 h-5 ml-2" />
          </button>
        </div>

        {/* Summary */}
        {Object.values(voicePrompts).some(text => text && text.trim().length > 0) && (
          <div className="mt-8 bg-emerald-50 rounded-lg p-6">
            <h3 className="font-semibold text-emerald-800 mb-4">Tóm tắt thông tin đã nhập:</h3>
            <div className="space-y-2 text-sm">
              {voicePrompts.symptoms && (
                <div><strong>Triệu chứng:</strong> {voicePrompts.symptoms}</div>
              )}
              {voicePrompts.allergies && (
                <div><strong>Dị ứng:</strong> {voicePrompts.allergies}</div>
              )}
              {voicePrompts.underlying_conditions && (
                <div><strong>Bệnh nền:</strong> {voicePrompts.underlying_conditions}</div>
              )}
              {voicePrompts.current_medications && (
                <div><strong>Thuốc đang dùng:</strong> {voicePrompts.current_medications}</div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceInput; 