import React, { useState } from 'react';
import { CheckCircle, Printer, RotateCcw, Download, Clock, User } from 'lucide-react';
import useVendingStore from '../store/vendingStore';

const ReceiptView = () => {
  const { prescription, patientData, resetAll } = useVendingStore();
  const [showPrintOptions, setShowPrintOptions] = useState(false);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const getCurrentDateTime = () => {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date());
  };

  const handleStartOver = () => {
    resetAll();
  };

  const handlePrintReceipt = () => {
    window.print();
  };

  const handleDownloadReceipt = () => {
    // Create receipt content for download
    const receiptContent = generateReceiptContent();
    const blob = new Blob([receiptContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `don-thuoc-${prescription?.prescription_id || 'receipt'}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const generateReceiptContent = () => {
    return `
      ====================================
          MÁY BÁN THUỐC TỰ ĐỘNG AI
      ====================================

      Ngày: ${getCurrentDateTime()}
      Mã đơn: #${prescription?.prescription_id || 'N/A'}

      ------------------------------------
      THÔNG TIN KHÁCH HÀNG:
      ------------------------------------
      Giới tính: ${patientData.gender === 'male' ? 'Nam' : 'Nữ'}
      Tuổi: ${patientData.age}
      Chiều cao: ${patientData.height} cm
      Cân nặng: ${patientData.weight} kg

      ------------------------------------
      CHẨN ĐOÁN:
      ------------------------------------
      ${prescription?.diagnosis || 'N/A'}
      Mức độ: ${prescription?.severity_level || 'N/A'}

      ------------------------------------
      DANH SÁCH THUỐC:
      ------------------------------------
      ${prescription?.items?.map(item => 
        `${item.name} x${item.total_quantity} - ${formatCurrency(item.price)}`
      ).join('\n') || 'Không có thông tin'}

      ------------------------------------
      TỔNG TIỀN: ${formatCurrency(prescription?.total_price || 0)}
      ------------------------------------

      HƯỚNG DẪN SỬ DỤNG:
      ${prescription?.usage_instructions || 'N/A'}

      LƯU Ý: ${prescription?.disclaimer || 'N/A'}

      Cảm ơn quý khách đã sử dụng dịch vụ!
      ====================================
    `;
  };

  if (!prescription) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-white flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
          <div className="text-gray-400 mb-4">
            <Clock className="w-16 h-16 mx-auto" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Không có thông tin đơn thuốc
          </h2>
          <p className="text-gray-600 mb-6">
            Vui lòng thực hiện quy trình mua thuốc để xem hóa đơn.
          </p>
          <button
            onClick={handleStartOver}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
          >
            Bắt đầu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-4xl print:shadow-none print:max-w-none">
        
        {/* Header - Success Message */}
        <div className="text-center p-8 bg-emerald-50 rounded-t-2xl print:bg-white">
          <div className="bg-emerald-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-12 h-12 text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold text-emerald-800 mb-2">
            Thanh toán thành công!
          </h1>
          <p className="text-emerald-600 text-lg">
            Thuốc của bạn đang được chuẩn bị. Vui lòng chờ trong giây lát.
          </p>
        </div>

        {/* Receipt Content */}
        <div className="p-8 space-y-8">
          
          {/* Receipt Header */}
          <div className="text-center border-b border-gray-200 pb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              HÓA ĐƠN MUA THUỐC
            </h2>
            <div className="text-gray-600 space-y-1">
              <p>Ngày: {getCurrentDateTime()}</p>
              <p>Mã đơn: #{prescription.prescription_id}</p>
            </div>
          </div>

          {/* Customer Info */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <User className="w-5 h-5 mr-2" />
              Thông tin khách hàng
            </h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-700">Giới tính:</span>
                <span className="ml-2">{patientData.gender === 'male' ? 'Nam' : 'Nữ'}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Tuổi:</span>
                <span className="ml-2">{patientData.age}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Chiều cao:</span>
                <span className="ml-2">{patientData.height} cm</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Cân nặng:</span>
                <span className="ml-2">{patientData.weight} kg</span>
              </div>
            </div>
          </div>

          {/* Diagnosis */}
          <div className="bg-slate-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-3">Chẩn đoán</h3>
            <p className="text-slate-700 mb-2">{prescription.diagnosis}</p>
            <span className="inline-block bg-slate-200 text-slate-800 px-3 py-1 rounded text-sm">
              Mức độ: {prescription.severity_level}
            </span>
          </div>

          {/* Items Table */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Chi tiết thuốc</h3>
            <div className="bg-gray-50 rounded-lg overflow-hidden">
              <div className="grid grid-cols-4 gap-4 p-4 bg-gray-100 font-semibold text-gray-700 text-sm">
                <div>Tên thuốc</div>
                <div className="text-center">Số lượng</div>
                <div className="text-right">Đơn giá</div>
                <div className="text-right">Thành tiền</div>
              </div>
              {prescription.items?.map((item, index) => (
                <div key={index} className="grid grid-cols-4 gap-4 p-4 border-b border-gray-200">
                  <div className="font-medium">{item.name}</div>
                  <div className="text-center">{item.total_quantity}</div>
                  <div className="text-right">
                    {formatCurrency(item.price / item.total_quantity)}
                  </div>
                  <div className="text-right font-medium">
                    {formatCurrency(item.price)}
                  </div>
                </div>
              ))}
              <div className="p-4 bg-emerald-100 border-t-2 border-emerald-300">
                 <div className="flex justify-between items-center">
                   <span className="text-lg font-bold text-emerald-800">TỔNG CỘNG:</span>
                   <span className="text-2xl font-bold text-emerald-800">
                     {formatCurrency(prescription.total_price)}
                   </span>
                 </div>
               </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-emerald-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-emerald-800 mb-3">Hướng dẫn sử dụng</h3>
            <p className="text-emerald-700">{prescription.usage_instructions}</p>
          </div>

          {/* Important Notes */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-yellow-800 mb-3">Lưu ý quan trọng</h3>
            <div className="space-y-2 text-yellow-700">
              {prescription.side_effects_warning && (
                <p><strong>Tác dụng phụ:</strong> {prescription.side_effects_warning}</p>
              )}
              {prescription.medical_advice && (
                <p><strong>Lời khuyên:</strong> {prescription.medical_advice}</p>
              )}
              {prescription.should_see_doctor && (
                <p className="text-red-700 font-medium">
                  ⚠️ Khuyến nghị gặp bác sĩ để được tư vấn thêm
                </p>
              )}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="bg-gray-100 rounded-lg p-4 border-l-4 border-gray-400">
            <p className="text-gray-600 text-sm italic">
              {prescription.disclaimer}
            </p>
          </div>
        </div>

        {/* Actions - Hide on print */}
        <div className="p-8 bg-gray-50 rounded-b-2xl print:hidden">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            
            {/* Print Options */}
            <div className="relative">
              <button
                onClick={() => setShowPrintOptions(!showPrintOptions)}
                className="flex items-center px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors"
              >
                <Printer className="w-5 h-5 mr-2" />
                Xuất hóa đơn
              </button>
              
              {showPrintOptions && (
                <div className="absolute bottom-full mb-2 left-0 bg-white rounded-lg shadow-lg border border-gray-200 min-w-48">
                  <button
                    onClick={handlePrintReceipt}
                    className="w-full text-left px-4 py-3 hover:bg-gray-50 flex items-center"
                  >
                    <Printer className="w-4 h-4 mr-2" />
                    In hóa đơn
                  </button>
                  <button
                    onClick={handleDownloadReceipt}
                    className="w-full text-left px-4 py-3 hover:bg-gray-50 flex items-center border-t border-gray-100"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Tải về file
                  </button>
                </div>
              )}
            </div>

            {/* Start Over */}
            <button
              onClick={handleStartOver}
              className="flex items-center px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white rounded-lg transition-colors"
            >
              <RotateCcw className="w-5 h-5 mr-2" />
              Khách hàng mới
            </button>
          </div>

          <div className="text-center mt-6 text-gray-600">
            <p className="text-lg font-medium">Cảm ơn bạn đã sử dụng dịch vụ!</p>
            <p className="text-sm">Thuốc sẽ được chuẩn bị trong vòng 2-3 phút</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReceiptView; 