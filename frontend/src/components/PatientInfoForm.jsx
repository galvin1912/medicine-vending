import React from 'react';
import { useForm } from 'react-hook-form';
import { User, Scale, Ruler, Calendar } from 'lucide-react';
import useVendingStore from '../store/vendingStore';

const PatientInfoForm = () => {
  const { patientData, setPatientData, nextStep } = useVendingStore();
  
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: {
      gender: patientData.gender || '',
      age: patientData.age || '',
      height: patientData.height || '',
      weight: patientData.weight || ''
    }
  });

  const onSubmit = (data) => {
    setPatientData({
      gender: data.gender,
      age: parseInt(data.age),
      height: parseInt(data.height),
      weight: parseInt(data.weight)
    });
    nextStep();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-white flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="bg-emerald-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <User className="w-8 h-8 text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Máy Bán Thuốc Tự Động
          </h1>
          <p className="text-gray-600">
            Vui lòng cung cấp thông tin cá nhân để được tư vấn thuốc phù hợp
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Gender Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Giới tính
            </label>
            <div className="grid grid-cols-2 gap-4">
              <label className="relative">
                <input
                  type="radio"
                  value="male"
                  {...register('gender', { required: 'Vui lòng chọn giới tính' })}
                  className="sr-only"
                />
                <div className={`
                  border-2 rounded-lg p-4 text-center cursor-pointer transition-all
                  ${watch('gender') === 'male' 
                    ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
                    : 'border-gray-200 hover:border-gray-300 text-gray-700'}
                `}> 
                  <User className="w-6 h-6 mx-auto mb-2" />
                  <span className="font-medium">Nam</span>
                </div>
              </label>
              <label className="relative">
                <input
                  type="radio"
                  value="female"
                  {...register('gender', { required: 'Vui lòng chọn giới tính' })}
                  className="sr-only"
                />
                <div className={`
                  border-2 rounded-lg p-4 text-center cursor-pointer transition-all
                  ${watch('gender') === 'female' 
                    ? 'border-emerald-500 bg-emerald-50 text-emerald-700' 
                    : 'border-gray-200 hover:border-gray-300 text-gray-700'}
                `}>
                  <User className="w-6 h-6 mx-auto mb-2" />
                  <span className="font-medium">Nữ</span>
                </div>
              </label>
            </div>
            {errors.gender && (
              <p className="text-red-500 text-sm mt-1">{errors.gender.message}</p>
            )}
          </div>

          {/* Age Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tuổi
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="number"
                min="1"
                max="120"
                {...register('age', { 
                  required: 'Vui lòng nhập tuổi',
                  min: { value: 1, message: 'Tuổi phải lớn hơn 0' },
                  max: { value: 120, message: 'Tuổi phải nhỏ hơn 120' }
                })}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-lg"
                placeholder="Nhập tuổi của bạn"
              />
            </div>
            {errors.age && (
              <p className="text-red-500 text-sm mt-1">{errors.age.message}</p>
            )}
          </div>

          {/* Height Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Chiều cao (cm)
            </label>
            <div className="relative">
              <Ruler className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="number"
                min="50"
                max="250"
                {...register('height', { 
                  required: 'Vui lòng nhập chiều cao',
                  min: { value: 50, message: 'Chiều cao phải lớn hơn 50cm' },
                  max: { value: 250, message: 'Chiều cao phải nhỏ hơn 250cm' }
                })}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-lg"
                placeholder="Nhập chiều cao (cm)"
              />
            </div>
            {errors.height && (
              <p className="text-red-500 text-sm mt-1">{errors.height.message}</p>
            )}
          </div>

          {/* Weight Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cân nặng (kg)
            </label>
            <div className="relative">
              <Scale className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="number"
                min="10"
                max="200"
                {...register('weight', { 
                  required: 'Vui lòng nhập cân nặng',
                  min: { value: 10, message: 'Cân nặng phải lớn hơn 10kg' },
                  max: { value: 200, message: 'Cân nặng phải nhỏ hơn 200kg' }
                })}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-lg"
                placeholder="Nhập cân nặng (kg)"
              />
            </div>
            {errors.weight && (
              <p className="text-red-500 text-sm mt-1">{errors.weight.message}</p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-4 px-6 rounded-lg transition-colors text-lg"
          >
            Tiếp tục
          </button>
        </form>
      </div>
    </div>
  );
};

export default PatientInfoForm; 