import React, { useEffect, useState, useCallback } from 'react';
import { Pill, Clock, AlertTriangle, ArrowLeft, ArrowRight, Loader2 } from 'lucide-react';
import useVendingStore from '../store/vendingStore';
import { analyzeInput, handleApiError } from '../services/api';

const RecommendationView = () => {
  const { 
    patientData, 
    recommendation, 
    setRecommendation, 
    previousStep, 
    nextStep,
    isLoading,
    setLoading,
    error,
    setError
  } = useVendingStore();

  const [showDetails, setShowDetails] = useState(true);

  const fetchRecommendation = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await analyzeInput(patientData);
      setRecommendation(response);
    } catch (err) {
      const errorInfo = handleApiError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  }, [patientData, setRecommendation, setLoading, setError]);



  const handleRetry = () => {
    fetchRecommendation();
  };

  const handleProceed = () => {
    nextStep();
  };

  useEffect(() => {
    if (!recommendation && patientData.symptoms) {
      fetchRecommendation();
    }
  }, [fetchRecommendation, patientData.symptoms, recommendation]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <Loader2 className="w-16 h-16 text-purple-600 animate-spin mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Đang phân tích triệu chứng...
          </h2>
          <p className="text-gray-600">
            AI đang xem xét thông tin của bạn để đưa ra gợi ý thuốc phù hợp
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <AlertTriangle className="w-16 h-16 text-red-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Đã xảy ra lỗi
          </h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <div className="flex justify-center gap-4">
            <button
              onClick={previousStep}
              className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
            >
              Quay lại
            </button>
            <button
              onClick={handleRetry}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            >
              Thử lại
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!recommendation) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <AlertTriangle className="w-16 h-16 text-yellow-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Chưa có dữ liệu
          </h2>
          <p className="text-gray-600 mb-6">
            Không có thông tin gợi ý thuốc. Vui lòng quay lại và nhập đầy đủ thông tin.
          </p>
          <button
            onClick={previousStep}
            className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
          >
            Quay lại
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="bg-emerald-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <Pill className="w-8 h-8 text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Gợi Ý Thuốc Từ AI
          </h1>
          <p className="text-gray-600">
            Dựa trên triệu chứng và thông tin của bạn
          </p>
        </div>

        {/* Main Medicines */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Pill className="w-6 h-6 mr-2 text-emerald-600" />
            Liều thuốc chính
          </h2>
          <div className="space-y-4">
            {recommendation.main_medicines?.map((medicine, index) => (
              <div key={index} className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-emerald-800">{medicine.name}</h3>
                  <span className="bg-emerald-200 text-emerald-800 px-2 py-1 rounded text-sm">
                    {medicine.quantity_per_dose} đơn vị/lần
                  </span>
                </div>
                <p className="text-gray-700 text-sm">{medicine.reason}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Supporting Medicines */}
        {recommendation.supporting_medicines && recommendation.supporting_medicines.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Pill className="w-6 h-6 mr-2 text-teal-600" />
              Thuốc hỗ trợ
            </h2>
            <div className="space-y-4">
              {recommendation.supporting_medicines.map((medicine, index) => (
                <div key={index} className="bg-teal-50 rounded-lg p-4 border border-teal-200">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-teal-800">{medicine.name}</h3>
                    <span className="bg-teal-200 text-teal-800 px-2 py-1 rounded text-sm">
                      {medicine.quantity_per_day ? `${medicine.quantity_per_day} đơn vị/ngày` : `${medicine.quantity} đơn vị`}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm">{medicine.reason}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Dosage Schedule */}
        <div className="mb-8 bg-slate-50 rounded-lg p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800 mb-4 flex items-center">
            <Clock className="w-6 h-6 mr-2" />
            Lịch uống thuốc
          </h2>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <span className="text-slate-700 font-medium">Số liều/ngày:</span>
              <span className="ml-2 text-slate-800">{recommendation.doses_per_day} liều</span>
            </div>
            <div>
              <span className="text-slate-700 font-medium">Tổng số ngày:</span>
              <span className="ml-2 text-slate-800">{recommendation.total_days} ngày</span>
            </div>
          </div>
        </div>

        {/* AI Reasoning */}
        <div className="mb-8">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full text-left bg-gray-50 hover:bg-gray-100 rounded-lg p-4 border border-gray-200 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-800 flex items-center justify-between">
              Giải thích từ AI
              <span className="text-sm text-gray-500">
                {showDetails ? 'Ẩn' : 'Hiển thị'}
              </span>
            </h2>
          </button>
          
          {showDetails && (
            <div className="mt-4 bg-gray-50 rounded-lg p-4 space-y-4">
              <div>
                <h3 className="font-medium text-gray-800 mb-2">Lý do gợi ý:</h3>
                <p className="text-gray-700 text-sm">{recommendation.recommendation_reasoning}</p>
              </div>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 className="font-medium text-yellow-800 mb-2 flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  Lưu ý quan trọng:
                </h3>
                <p className="text-yellow-700 text-sm">{recommendation.disclaimer}</p>
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={previousStep}
            className="flex items-center px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Quay lại
          </button>

          <button
            onClick={handleProceed}
            className="flex items-center px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
          >
            Xác nhận và tiếp tục
            <ArrowRight className="w-5 h-5 ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecommendationView; 