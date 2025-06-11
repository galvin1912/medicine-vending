import React, { useEffect, useState, useCallback } from 'react';
import { ShoppingCart, AlertCircle, Heart, ArrowLeft, ArrowRight, Loader2, FileText } from 'lucide-react';
import useVendingStore from '../store/vendingStore';
import { confirmPrescription, handleApiError } from '../services/api';

const PrescriptionView = () => {
  const { 
    patientData, 
    recommendation,
    prescription, 
    setPrescription, 
    previousStep, 
    nextStep,
    isLoading,
    setLoading,
    error,
    setError
  } = useVendingStore();

  const [showDetails, setShowDetails] = useState(true);

  const fetchPrescription = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const requestData = { ...patientData, recommendation };
      const response = await confirmPrescription(requestData);
      setPrescription(response);
    } catch (err) {
      const errorInfo = handleApiError(err);
      setError(errorInfo.message);  
    } finally { 
      setLoading(false);
    }
  }, [patientData, recommendation, setPrescription, setLoading, setError]);

  const handleRetry = () => {
    fetchPrescription();
  };

  const handleConfirmPurchase = () => {
    nextStep();
  };

  useEffect(() => {
    if (!prescription) {
      fetchPrescription();
    }
  }, [fetchPrescription, prescription]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'nhẹ': return 'text-green-600 bg-green-100';
      case 'vừa': return 'text-yellow-600 bg-yellow-100';
      case 'nặng': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <Loader2 className="w-16 h-16 text-orange-600 animate-spin mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Đang tạo đơn thuốc...
          </h2>
          <p className="text-gray-600">
            Đang tính toán giá cả và chuẩn bị đơn thuốc cho bạn
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <AlertCircle className="w-16 h-16 text-red-600 mx-auto mb-4" />
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

  if (!prescription) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <AlertCircle className="w-16 h-16 text-yellow-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Chưa có đơn thuốc
          </h2>
          <p className="text-gray-600 mb-6">
            Không có thông tin đơn thuốc. Vui lòng quay lại bước trước.
          </p>
          <button
            onClick={previousStep}
            className="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors"
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
            <FileText className="w-8 h-8 text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Đơn Thuốc Chi Tiết
          </h1>
          <p className="text-gray-600">
            Xác nhận thông tin và thanh toán
          </p>
        </div>

        {/* Prescription Summary */}
        <div className="mb-8 bg-slate-50 rounded-lg p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800 mb-4 flex items-center">
            <FileText className="w-6 h-6 mr-2" />
            Chẩn đoán và tình trạng
          </h2>
          <div className="space-y-3">
            <div>
              <span className="font-medium text-slate-700">Chẩn đoán:</span>
              <span className="ml-2 text-slate-800">{prescription.diagnosis || "Không có chẩn đoán"}</span>
            </div>
            <div className="flex items-center">
              <span className="font-medium text-slate-700">Mức độ nghiêm trọng:</span>
              <span className={`ml-2 px-2 py-1 rounded text-sm font-medium ${getSeverityColor(prescription.severity_level)}`}>
                {prescription.severity_level}
              </span>
            </div>
            {prescription.emergency_status && (
              <div className="bg-red-100 border border-red-300 rounded-lg p-3">
                <span className="text-red-700 font-medium">⚠️ Tình trạng khẩn cấp - Cần gặp bác sĩ ngay lập tức!</span>
              </div>
            )}
          </div>
        </div>

        {/* Items List */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <ShoppingCart className="w-6 h-6 mr-2 text-emerald-600" />
            Danh sách thuốc
          </h2>
          <div className="bg-gray-50 rounded-lg overflow-hidden">
            <div className="grid grid-cols-4 gap-4 p-4 bg-gray-100 font-semibold text-gray-700 text-sm">
              <div>Tên thuốc</div>
              <div className="text-center">Số lượng</div>
              <div className="text-right">Đơn giá</div>
              <div className="text-right">Thành tiền</div>
            </div>
            {prescription.items?.map((item, index) => (
              <div key={index} className="grid grid-cols-4 gap-4 p-4 border-b border-gray-200">
                <div className="font-medium text-gray-800">{item.name}</div>
                <div className="text-center text-gray-600">{item.total_quantity}</div>
                <div className="text-right text-gray-600">
                  {formatCurrency(item.price / item.total_quantity)}
                </div>
                <div className="text-right font-medium text-gray-800">
                  {formatCurrency(item.price)}
                </div>
              </div>
            ))}
            <div className="p-4 bg-emerald-50 border-t-2 border-emerald-200">
              <div className="flex justify-between items-center">
                <span className="text-lg font-semibold text-emerald-800">Tổng cộng:</span>
                <span className="text-2xl font-bold text-emerald-800">
                  {formatCurrency(prescription.total_price)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Heart className="w-6 h-6 mr-2 text-red-600" />
            Hướng dẫn sử dụng
          </h2>
          <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
            <p className="text-emerald-800">{prescription.usage_instructions}</p>
          </div>
        </div>

        {/* Side Effects and Warnings */}
        {prescription.side_effects_warning && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <AlertCircle className="w-6 h-6 mr-2 text-yellow-600" />
              Tác dụng phụ và cảnh báo
            </h2>
            <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
              <p className="text-yellow-800">{prescription.side_effects_warning}</p>
            </div>
          </div>
        )}

        {/* Medical Advice */}
        {prescription.medical_advice && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Lời khuyên y tế
            </h2>
            <div className="bg-teal-50 rounded-lg p-4 border border-teal-200">
              <p className="text-teal-800">{prescription.medical_advice}</p>
              {prescription.should_see_doctor && (
                <div className="mt-3 bg-red-100 border border-red-300 rounded-lg p-3">
                  <span className="text-red-700 font-medium">
                    💊 Khuyến nghị: Nên gặp bác sĩ để được thăm khám và tư vấn chuyên sâu
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Additional Details */}
        <div className="mb-8">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full text-left bg-gray-50 hover:bg-gray-100 rounded-lg p-4 border border-gray-200 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-800 flex items-center justify-between">
              Thông tin bổ sung
              <span className="text-sm text-gray-500">
                {showDetails ? 'Ẩn' : 'Hiển thị'}
              </span>
            </h2>
          </button>
          
          {showDetails && (
            <div className="mt-4 bg-gray-50 rounded-lg p-4 space-y-4">
              <div>
                <h3 className="font-medium text-gray-800 mb-2">Mã đơn thuốc:</h3>
                <p className="text-gray-700 font-mono">#{prescription.prescription_id}</p>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-800 mb-2">Lý do gợi ý:</h3>
                <p className="text-gray-700 text-sm">{prescription.recommendation_reasoning}</p>
              </div>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h3 className="font-medium text-yellow-800 mb-2 flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Tuyên bố từ chối trách nhiệm:
                </h3>
                <p className="text-yellow-700 text-sm">{prescription.disclaimer}</p>
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
            onClick={handleConfirmPurchase}
            className="flex items-center px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors text-lg font-semibold"
          >
            Xác nhận mua - {formatCurrency(prescription.total_price)}
            <ArrowRight className="w-5 h-5 ml-2" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PrescriptionView; 