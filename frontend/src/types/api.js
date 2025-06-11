// API Request/Response Types based on PRD specifications

// POST /analyze_input request
export const createAnalyzeInputRequest = (data) => ({
  symptoms: data.symptoms,
  gender: data.gender,
  age: data.age,
  height: data.height,
  weight: data.weight,
  allergies: data.allergies || [],
  underlying_conditions: data.underlying_conditions || [],
  current_medications: data.current_medications || []
});

// POST /analyze_input response structure
export const analyzeInputResponseSchema = {
  main_medicines: [
    {
      name: "string",
      quantity_per_dose: "number",
      reason: "string"
    }
  ],
  supporting_medicines: [
    {
      name: "string",
      quantity_per_day: "number", // or quantity for items like masks
      quantity: "number", // optional for non-daily items
      reason: "string"
    }
  ],
  doses_per_day: "number",
  total_days: "number",
  recommendation_reasoning: "string",
  disclaimer: "string"
};

// POST /confirm_prescription request (based on backend ConfirmPrescriptionRequest schema)
export const createConfirmPrescriptionRequest = (data) => ({
  patient_data: {
    gender: data.gender,
    age: data.age,
    height: data.height,
    weight: data.weight
  },
  main_medicines: data.recommendation?.main_medicines || [],
  supporting_medicines: data.recommendation?.supporting_medicines?.map(med => ({
    name: med.name,
    quantity_total: med.quantity_per_day || med.quantity || 1
  })) || [],
  doses_per_day: data.recommendation?.doses_per_day || 3,
  total_days: data.recommendation?.total_days || 3,
  ai_recommendation: data.recommendation?.recommendation_reasoning || "",
  diagnosis: data.recommendation?.diagnosis || "",
  severity_level: data.recommendation?.severity_level || "",
  side_effects_warning: data.recommendation?.side_effects_warning || "",
  medical_advice: data.recommendation?.medical_advice || "",
  emergency_status: data.recommendation?.emergency_status || false,
  should_see_doctor: data.recommendation?.should_see_doctor || false,
  disclaimer: data.recommendation?.disclaimer || ""
});

// POST /confirm_prescription response structure
export const confirmPrescriptionResponseSchema = {
  prescription_id: "number",
  total_price: "number",
  diagnosis: "string",
  usage_instructions: "string",
  side_effects_warning: "string",
  medical_advice: "string",
  recommendation_reasoning: "string",
  severity_level: "string",
  emergency_status: "boolean",
  should_see_doctor: "boolean",
  disclaimer: "string",
  items: [
    {
      name: "string",
      total_quantity: "number",
      price: "number"
    }
  ]
};

// POST /patients request
export const createPatientRequest = (data) => ({
  gender: data.gender,
  age: data.age,
  weight: data.weight,
  height: data.height
});

// GET /medications response structure
export const medicationsResponseSchema = [
  {
    id: "number",
    name: "string",
    active_ingredient: "string",
    form: "string",
    unit_type: "string",
    unit_price: "number",
    stock: "number",
    side_effects: "string",
    max_per_day: "number",
    is_supporting: "boolean",
    treatment_class: "string",
    contraindications: "string",
    allergy_tags: ["string"]
  }
]; 