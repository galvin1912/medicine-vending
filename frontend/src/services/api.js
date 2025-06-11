import axios from 'axios';
import {
  createAnalyzeInputRequest,
  createConfirmPrescriptionRequest,
  createPatientRequest
} from '../types/api.js';

// Base URL configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Services matching PRD specifications exactly

/**
 * POST /analyze_input
 * Analyze symptoms and patient info, get medicine recommendations
 */
export const analyzeInput = async (patientData) => {
  const requestBody = createAnalyzeInputRequest(patientData);
  const response = await apiClient.post('/analyze_input', requestBody);
  return response.data;
};

/**
 * POST /confirm_prescription  
 * Confirm prescription and get final pricing and details
 */
export const confirmPrescription = async (patientData) => {
  const requestBody = createConfirmPrescriptionRequest(patientData);
  const response = await apiClient.post('/confirm_prescription', requestBody);
  return response.data;
};

/**
 * GET /medications
 * Get all available medications in stock
 */
export const getMedications = async () => {
  const response = await apiClient.get('/medications');
  return response.data;
};

/**
 * POST /patients
 * Create patient record with basic info
 */
export const createPatient = async (patientData) => {
  const requestBody = createPatientRequest(patientData);
  const response = await apiClient.post('/patients', requestBody);
  return response.data;
};

// Error handling wrapper
export const handleApiError = (error) => {
  if (error.response) {
    // Backend returned error response
    console.error('API Error:', error.response.data);
    return {
      message: error.response.data.detail || 'Đã xảy ra lỗi từ hệ thống',
      status: error.response.status
    };
  } else if (error.request) {
    // Network error
    console.error('Network Error:', error.request);
    return {
      message: 'Không thể kết nối đến hệ thống. Vui lòng thử lại.',
      status: 0
    };
  } else {
    // Other error
    console.error('Error:', error.message);
    return {
      message: 'Đã xảy ra lỗi không xác định',
      status: -1
    };
  }
}; 