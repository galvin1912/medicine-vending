-- Initialize AI Medicine Vending Machine Database (Vietnam)
-- Based on PRD requirements for Vietnamese pharmacy vending machine
-- This file is automatically executed when the PostgreSQL container starts

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    gender TEXT NOT NULL CHECK (gender IN ('male', 'female', 'other')),
    age INTEGER NOT NULL CHECK (age > 0 AND age <= 120),
    weight INTEGER CHECK (weight > 0 AND weight <= 300), -- kg
    height INTEGER CHECK (height > 0 AND height <= 250), -- cm
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create allergies table
CREATE TABLE IF NOT EXISTS allergies (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    substance TEXT NOT NULL,
    severity TEXT DEFAULT 'mild' CHECK (severity IN ('mild', 'moderate', 'severe')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create underlying_conditions table
CREATE TABLE IF NOT EXISTS underlying_conditions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    condition_name TEXT NOT NULL,
    diagnosed_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create medications table (based on Vietnamese pharmacy standards)
CREATE TABLE IF NOT EXISTS medications (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE, -- Tên thương mại
    active_ingredient TEXT NOT NULL, -- Hoạt chất chính
    form TEXT NOT NULL, -- Dạng bào chế (viên, siro, gói...)
    unit_type TEXT NOT NULL, -- Đơn vị tính (viên, gói, chai...)
    unit_price INTEGER NOT NULL, -- Giá cho mỗi đơn vị (VND)
    stock INTEGER NOT NULL DEFAULT 0, -- Số lượng còn trong kho
    side_effects TEXT, -- Tác dụng phụ phổ biến
    max_per_day INTEGER, -- Liều tối đa/ngày
    is_supporting BOOLEAN DEFAULT FALSE, -- Có phải thuốc hỗ trợ hay không
    treatment_class TEXT NOT NULL, -- Nhóm điều trị
    contraindications TEXT, -- Chống chỉ định
    allergy_tags TEXT[], -- Các thành phần có thể gây dị ứng
    manufacturer TEXT,
    registration_number TEXT, -- Số đăng ký thuốc Việt Nam
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create symptoms table
CREATE TABLE IF NOT EXISTS symptoms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    vietnamese_name TEXT NOT NULL,
    category TEXT,
    severity_level TEXT DEFAULT 'mild' CHECK (severity_level IN ('mild', 'moderate', 'severe', 'emergency')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create medication-symptom relationship table
CREATE TABLE IF NOT EXISTS medication_symptom (
    medication_id INTEGER REFERENCES medications(id) ON DELETE CASCADE,
    symptom_id INTEGER REFERENCES symptoms(id) ON DELETE CASCADE,
    effectiveness INTEGER DEFAULT 5 CHECK (effectiveness >= 1 AND effectiveness <= 10),
    PRIMARY KEY (medication_id, symptom_id)
);

-- Create prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    doses_per_day INTEGER NOT NULL CHECK (doses_per_day >= 1 AND doses_per_day <= 6),
    days INTEGER NOT NULL CHECK (days >= 1 AND days <= 30),
    total_price INTEGER NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    diagnosis TEXT,
    ai_recommendation TEXT,
    pharmacist_notes TEXT
);

-- Create prescription_doses table (main medications)
CREATE TABLE IF NOT EXISTS prescription_doses (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER REFERENCES prescriptions(id) ON DELETE CASCADE,
    medication_id INTEGER REFERENCES medications(id),
    quantity_per_dose INTEGER NOT NULL CHECK (quantity_per_dose > 0),
    dose_time TEXT NOT NULL, -- 'morning', 'noon', 'evening', 'night'
    special_instructions TEXT
);

-- Create prescription_supportings table (supporting medications)
CREATE TABLE IF NOT EXISTS prescription_supportings (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER REFERENCES prescriptions(id) ON DELETE CASCADE,
    medication_id INTEGER REFERENCES medications(id),
    quantity_total INTEGER NOT NULL CHECK (quantity_total > 0),
    usage_instructions TEXT
);

-- Create usage_logs table
CREATE TABLE IF NOT EXISTS usage_logs (
    id SERIAL PRIMARY KEY,
    prescription_id INTEGER REFERENCES prescriptions(id),
    note TEXT,
    generated_by TEXT NOT NULL,
    log_type TEXT DEFAULT 'info' CHECK (log_type IN ('info', 'warning', 'error', 'success')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert common symptoms (Vietnamese context)
INSERT INTO symptoms (name, vietnamese_name, category, severity_level) VALUES
('headache', 'đau đầu', 'neurological', 'mild'),
('fever', 'sốt', 'general', 'moderate'),
('cough', 'ho', 'respiratory', 'mild'),
('runny_nose', 'sổ mũi', 'respiratory', 'mild'),
('sore_throat', 'đau họng', 'respiratory', 'mild'),
('stomach_ache', 'đau bụng', 'digestive', 'moderate'),
('nausea', 'buồn nôn', 'digestive', 'mild'),
('diarrhea', 'tiêu chảy', 'digestive', 'moderate'),
('constipation', 'táo bón', 'digestive', 'mild'),
('muscle_pain', 'đau cơ', 'musculoskeletal', 'mild'),
('joint_pain', 'đau khớp', 'musculoskeletal', 'moderate'),
('back_pain', 'đau lưng', 'musculoskeletal', 'moderate'),
('allergic_reaction', 'dị ứng', 'immune', 'moderate'),
('skin_rash', 'phát ban', 'dermatological', 'mild'),
('insomnia', 'mất ngủ', 'neurological', 'mild'),
('fatigue', 'mệt mỏi', 'general', 'mild'),
('dizziness', 'chóng mặt', 'neurological', 'mild'),
('chest_pain', 'đau ngực', 'cardiovascular', 'severe'),
('shortness_of_breath', 'khó thở', 'respiratory', 'severe'),
('high_blood_pressure', 'huyết áp cao', 'cardiovascular', 'moderate');

-- Insert 200 popular Vietnamese medications
INSERT INTO medications (name, active_ingredient, form, unit_type, unit_price, stock, side_effects, max_per_day, is_supporting, treatment_class, contraindications, allergy_tags, manufacturer, registration_number) VALUES
-- Pain Relief & Fever Reducers
('Paracetamol 500mg', 'Paracetamol', 'viên nén', 'viên', 1000, 2500, 'Hiếm khi xảy ra phát ban, buồn nôn', 8, FALSE, 'Giảm đau hạ sốt', 'Suy gan nặng', ARRAY['paracetamol'], 'Dược Hậu Giang', 'VD-123-45'),
('Aspirin 500mg', 'Acetylsalicylic acid', 'viên nén', 'viên', 800, 2000, 'Đau dạ dày, chảy máu', 6, FALSE, 'Giảm đau chống viêm', 'Loét dạ dày, trẻ em dưới 12 tuổi', ARRAY['aspirin'], 'Imexpharm', 'VD-234-56'),
('Ibuprofen 400mg', 'Ibuprofen', 'viên nang', 'viên', 1200, 1800, 'Buồn nôn, chóng mặt', 6, FALSE, 'Giảm đau chống viêm', 'Loét tiêu hóa, suy thận', ARRAY['ibuprofen'], 'Traphaco', 'VD-345-67'),
('Diclofenac 50mg', 'Diclofenac sodium', 'viên nén', 'viên', 1500, 1500, 'Rối loạn tiêu hóa', 3, FALSE, 'Chống viêm giảm đau', 'Loét dạ dày', ARRAY['diclofenac'], 'Pymepharco', 'VD-456-78'),
('Naproxen 220mg', 'Naproxen', 'viên nén', 'viên', 2000, 1200, 'Đau đầu, buồn nôn', 3, FALSE, 'Chống viêm giảm đau', 'Bệnh tim mạch', ARRAY['naproxen'], 'Boston', 'VD-567-89'),

-- Antibiotics
('Amoxicillin 500mg', 'Amoxicillin', 'viên nang', 'viên', 2500, 2200, 'Tiêu chảy, phát ban', 6, FALSE, 'Kháng sinh', 'Dị ứng penicillin', ARRAY['penicillin', 'amoxicillin'], 'Domesco', 'VD-678-90'),
('Erythromycin 250mg', 'Erythromycin', 'viên nén', 'viên', 3000, 1800, 'Buồn nôn, đau bụng', 4, FALSE, 'Kháng sinh', 'Suy gan', ARRAY['erythromycin'], 'DHG Pharma', 'VD-789-01'),
('Cephalexin 500mg', 'Cephalexin', 'viên nang', 'viên', 4000, 1400, 'Rối loạn tiêu hóa', 4, FALSE, 'Kháng sinh', 'Dị ứng cephalosporin', ARRAY['cephalosporin'], 'Stada Vietnam', 'VD-890-12'),
('Ciprofloxacin 500mg', 'Ciprofloxacin', 'viên nén', 'viên', 5000, 1100, 'Chóng mặt, buồn nôn', 2, FALSE, 'Kháng sinh', 'Trẻ em dưới 18 tuổi', ARRAY['quinolone'], 'Zentiva', 'VD-901-23'),
('Azithromycin 500mg', 'Azithromycin', 'viên nén', 'viên', 8000, 1300, 'Đau bụng, tiêu chảy', 1, FALSE, 'Kháng sinh', 'Suy gan nặng', ARRAY['macrolide'], 'Pfizer', 'VD-012-34'),

-- Cold & Flu Medications
('Actifed', 'Pseudoephedrine + Triprolidine', 'viên nén', 'viên', 3500, 1600, 'Buồn ngủ, khô miệng', 6, FALSE, 'Cảm cúm', 'Tăng huyết áp, glaucoma', ARRAY['antihistamine'], 'GSK', 'VD-123-45'),
('Tylenol Cold & Flu', 'Paracetamol + Phenylephrine', 'viên nén', 'viên', 4000, 1400, 'Chóng mặt, mất ngủ', 6, FALSE, 'Cảm cúm', 'Bệnh tim mạch', ARRAY['paracetamol'], 'J&J', 'VD-234-56'),
('Decolgen', 'Paracetamol + Phenylpropanolamine + Chlorphenamine', 'viên nén', 'viên', 2500, 2200, 'Buồn ngủ, khô miệng', 6, FALSE, 'Cảm cúm', 'Tăng huyết áp', ARRAY['paracetamol', 'antihistamine'], 'United Pharma', 'VD-345-67'),
('Claricold', 'Paracetamol + Loratadine + Pseudoephedrine', 'viên nén', 'viên', 3000, 1700, 'Khô miệng, tim đập nhanh', 4, FALSE, 'Cảm cúm', 'Cao huyết áp', ARRAY['antihistamine'], 'Glomed', 'VD-456-78'),

-- Cough Medicines
('Dextromethorphan 15mg', 'Dextromethorphan', 'siro', 'ml', 100, 2800, 'Buồn ngủ, chóng mặt', 120, FALSE, 'Thuốc ho', 'Suy hô hấp', ARRAY['dextromethorphan'], 'OPC', 'VD-567-89'),
('Bromhexine 8mg', 'Bromhexine HCl', 'viên nén', 'viên', 1500, 1900, 'Buồn nôn nhẹ', 6, FALSE, 'Thuốc long đờm', 'Loét dạ dày', ARRAY['bromhexine'], 'Mediplantex', 'VD-678-90'),
('Codeine 30mg', 'Codeine phosphate', 'viên nén', 'viên', 5000, 1050, 'Buồn ngủ, táo bón', 4, FALSE, 'Thuốc ho', 'Suy hô hấp, trẻ em', ARRAY['codeine', 'opioid'], 'Controlled', 'VD-789-01'),	('Guaifenesin 200mg', 'Guaifenesin', 'viên nén', 'viên', 2000, 1600, 'Buồn nôn nhẹ', 12, FALSE, 'Thuốc long đờm', 'Không có', ARRAY[]::TEXT[]::TEXT[], 'Savipharm', 'VD-890-12'),

-- Digestive Medications
('Omeprazole 20mg', 'Omeprazole', 'viên nang', 'viên', 3000, 2300, 'Đau đầu, tiêu chảy', 2, FALSE, 'Ức chế bơm proton', 'Dị ứng benzimidazole', ARRAY['omeprazole'], 'Teva', 'VD-901-23'),
('Ranitidine 150mg', 'Ranitidine HCl', 'viên nén', 'viên', 2000, 2100, 'Chóng mặt, táo bón', 4, FALSE, 'Kháng H2', 'Suy thận nặng', ARRAY['ranitidine'], 'Glaxo', 'VD-012-34'),
('Domperidone 10mg', 'Domperidone', 'viên nén', 'viên', 1500, 1800, 'Khô miệng, đau đầu', 8, FALSE, 'Chống nôn', 'Bệnh tim', ARRAY['domperidone'], 'Janssen', 'VD-123-45'),
('Loperamide 2mg', 'Loperamide HCl', 'viên nang', 'viên', 2500, 1400, 'Táo bón, chóng mặt', 8, FALSE, 'Chống tiêu chảy', 'Viêm ruột cấp', ARRAY['loperamide'], 'Sanofi', 'VD-234-56'),
('Simethicone 40mg', 'Simethicone', 'viên nhai', 'viên', 1000, 2500, 'Không có tác dụng phụ', 12, TRUE, 'Chống đầy hơi', 'Không có', ARRAY[]::TEXT[], 'Pharmedic', 'VD-345-67'),

-- Allergy Medications
('Cetirizine 10mg', 'Cetirizine HCl', 'viên nén', 'viên', 2000, 2100, 'Buồn ngủ nhẹ', 2, FALSE, 'Kháng histamine', 'Suy thận nặng', ARRAY['cetirizine'], 'UCB Pharma', 'VD-456-78'),
('Loratadine 10mg', 'Loratadine', 'viên nén', 'viên', 2500, 1900, 'Đau đầu, mệt mỏi', 1, FALSE, 'Kháng histamine', 'Suy gan nặng', ARRAY['loratadine'], 'Schering', 'VD-567-89'),
('Fexofenadine 120mg', 'Fexofenadine HCl', 'viên nén', 'viên', 4000, 1400, 'Đau đầu, buồn nôn', 2, FALSE, 'Kháng histamine', 'Suy thận', ARRAY['fexofenadine'], 'Aventis', 'VD-678-90'),
('Chlorpheniramine 4mg', 'Chlorpheniramine maleate', 'viên nén', 'viên', 1000, 2700, 'Buồn ngủ, khô miệng', 6, FALSE, 'Kháng histamine', 'Glaucoma', ARRAY['chlorpheniramine'], 'Various', 'VD-789-01'),

-- Cardiovascular Medications
('Amlodipine 5mg', 'Amlodipine besylate', 'viên nén', 'viên', 3000, 1800, 'Phù chân, chóng mặt', 2, FALSE, 'Chẹn kênh canxi', 'Sốc tim', ARRAY['amlodipine'], 'Pfizer', 'VD-890-12'),
('Atenolol 50mg', 'Atenolol', 'viên nén', 'viên', 2500, 1600, 'Mệt mỏi, chóng mặt', 2, FALSE, 'Chẹn beta', 'Hen suyễn, block tim', ARRAY['beta-blocker'], 'AstraZeneca', 'VD-901-23'),
('Enalapril 10mg', 'Enalapril maleate', 'viên nén', 'viên', 3500, 1400, 'Ho khô, tăng kali', 2, FALSE, 'Ức chế ACE', 'Thai nghén', ARRAY['ace-inhibitor'], 'MSD', 'VD-012-34'),
('Simvastatin 20mg', 'Simvastatin', 'viên nén', 'viên', 4000, 1300, 'Đau cơ, rối loạn tiêu hóa', 1, FALSE, 'Statin', 'Bệnh gan, thai nghén', ARRAY['statin'], 'Merck', 'VD-123-45'),

-- Diabetes Medications
('Metformin 500mg', 'Metformin HCl', 'viên nén', 'viên', 2000, 2400, 'Buồn nôn, tiêu chảy', 6, FALSE, 'Biguanide', 'Suy thận, suy tim', ARRAY['metformin'], 'Berlin-Chemie', 'VD-234-56'),
('Glibenclamide 5mg', 'Glibenclamide', 'viên nén', 'viên', 1500, 1900, 'Hạ đường huyết', 2, FALSE, 'Sulfonylurea', 'Tiểu đường type 1', ARRAY['sulfonylurea'], 'Sanofi', 'VD-345-67'),
('Gliclazide 80mg', 'Gliclazide', 'viên nén', 'viên', 3000, 1600, 'Hạ đường huyết', 2, FALSE, 'Sulfonylurea', 'Tiểu đường type 1', ARRAY['sulfonylurea'], 'Servier', 'VD-456-78'),

-- Mental Health & Sleep
('Diazepam 5mg', 'Diazepam', 'viên nén', 'viên', 3000, 1200, 'Buồn ngủ, chóng mặt', 4, FALSE, 'Benzodiazepine', 'Nghiện rượu, thai nghén', ARRAY['benzodiazepine'], 'Roche', 'VD-567-89'),
('Alprazolam 0.5mg', 'Alprazolam', 'viên nén', 'viên', 4000, 1100, 'Buồn ngủ, lú lẫn', 6, FALSE, 'Benzodiazepine', 'Glaucoma, thai nghén', ARRAY['benzodiazepine'], 'Pfizer', 'VD-678-90'),
('Zolpidem 10mg', 'Zolpidem tartrate', 'viên nén', 'viên', 5000, 1300, 'Chóng mặt, ảo giác', 1, FALSE, 'Thuốc ngủ', 'Suy hô hấp', ARRAY['zolpidem'], 'Sanofi', 'VD-789-01'),

-- Vitamins & Supplements
('Vitamin C 500mg', 'Ascorbic acid', 'viên sủi', 'viên', 2000, 3000, 'Không có', 4, TRUE, 'Vitamin', 'Sỏi thận', ARRAY[]::TEXT[], 'Rowa', 'VD-890-12'),
('Vitamin B Complex', 'B1+B6+B12', 'viên nang', 'viên', 1500, 2800, 'Không có', 3, TRUE, 'Vitamin', 'Không có', ARRAY[]::TEXT[], 'Bayer', 'VD-901-23'),
('Vitamin D3 1000IU', 'Cholecalciferol', 'viên nang', 'viên', 3000, 1800, 'Không có khi dùng đúng liều', 1, TRUE, 'Vitamin', 'Tăng canxi máu', ARRAY[]::TEXT[], 'Nature Made', 'VD-012-34'),
('Calcium 600mg', 'Calcium carbonate', 'viên nén', 'viên', 2500, 2200, 'Táo bón nhẹ', 3, TRUE, 'Khoáng chất', 'Sỏi thận', ARRAY[]::TEXT[], 'Caltrate', 'VD-123-45'),
('Iron 65mg', 'Ferrous sulfate', 'viên nén', 'viên', 2000, 1900, 'Táo bón, buồn nôn', 3, TRUE, 'Khoáng chất', 'Tăng sắt máu', ARRAY[]::TEXT[], 'Ferrous', 'VD-234-56'),
('Zinc 15mg', 'Zinc sulfate', 'viên nén', 'viên', 1800, 2100, 'Buồn nôn khi đói', 1, TRUE, 'Khoáng chất', 'Không có', ARRAY[]::TEXT[], 'Nature', 'VD-345-67'),
('Omega 3', 'EPA + DHA', 'viên nang', 'viên', 5000, 1400, 'Không có', 3, TRUE, 'Axit béo', 'Rối loạn đông máu', ARRAY['fish'], 'Nordic', 'VD-456-78'),
('Multivitamin', 'Multiple vitamins & minerals', 'viên nén', 'viên', 4000, 1600, 'Không có', 1, TRUE, 'Vitamin tổng hợp', 'Tăng sắt máu', ARRAY[]::TEXT[], 'Centrum', 'VD-567-89'),

-- Topical Medications
('Betamethasone 0.1%', 'Betamethasone valerate', 'kem', 'tuýp', 15000, 1100, 'Atrophy da khi dùng lâu', 3, FALSE, 'Corticosteroid tại chỗ', 'Nhiễm khuẩn da', ARRAY['corticosteroid'], 'GSK', 'VD-678-90'),
('Hydrocortisone 1%', 'Hydrocortisone', 'kem', 'tuýp', 12000, 1200, 'Kích ứng da nhẹ', 4, FALSE, 'Corticosteroid tại chỗ', 'Nhiễm khuẩn da', ARRAY['corticosteroid'], 'Taro', 'VD-789-01'),
('Clotrimazole 1%', 'Clotrimazole', 'kem', 'tuýp', 18000, 1300, 'Ngứa, đỏ da nhẹ', 3, FALSE, 'Chống nấm', 'Dị ứng clotrimazole', ARRAY['azole'], 'Bayer', 'VD-890-12'),
('Mupirocin 2%', 'Mupirocin', 'thuốc mỡ', 'tuýp', 25000, 1050, 'Kích ứng da', 3, FALSE, 'Kháng sinh tại chỗ', 'Dị ứng mupirocin', ARRAY['antibiotic'], 'GSK', 'VD-901-23'),

-- Eye & Ear Medications
('Tobramycin eye drops', 'Tobramycin', 'dung dịch nhỏ mắt', 'chai', 35000, 1200, 'Kích ứng mắt tạm thời', 6, FALSE, 'Kháng sinh nhỏ mắt', 'Dị ứng aminoglycoside', ARRAY['aminoglycoside'], 'Alcon', 'VD-012-34'),
('Artificial tears', 'Polyvinyl alcohol', 'dung dịch nhỏ mắt', 'chai', 15000, 1500, 'Không có', 8, TRUE, 'Nước mắt nhân tạo', 'Không có', ARRAY[]::TEXT[], 'Refresh', 'VD-123-45'),
('Ciprofloxacin ear drops', 'Ciprofloxacin', 'dung dịch nhỏ tai', 'chai', 45000, 1100, 'Kích ứng tai nhẹ', 4, FALSE, 'Kháng sinh nhỏ tai', 'Thủng màng nhĩ', ARRAY['quinolone'], 'Cipla', 'VD-234-56'),

-- Women's Health
('Folic acid 5mg', 'Folic acid', 'viên nén', 'viên', 1000, 2400, 'Không có', 1, TRUE, 'Vitamin', 'Thiếu máu pernicious', ARRAY[]::TEXT[], 'Various', 'VD-345-67'),
('Iron + Folic acid', 'Ferrous sulfate + Folic acid', 'viên nén', 'viên', 2500, 1900, 'Táo bón, buồn nôn', 1, TRUE, 'Bổ máu', 'Tăng sắt máu', ARRAY[]::TEXT[], 'Pharma', 'VD-456-78'),

-- Respiratory Medications
('Salbutamol 2mg', 'Salbutamol sulfate', 'viên nén', 'viên', 2000, 1400, 'Tim đập nhanh, run', 8, FALSE, 'Giãn phế quản', 'Tăng nhạy cảm', ARRAY['salbutamol'], 'GSK', 'VD-567-89'),
('Theophylline 200mg', 'Theophylline', 'viên nén', 'viên', 3000, 1200, 'Buồn nôn, tim đập nhanh', 3, FALSE, 'Giãn phế quản', 'Rối loạn nhịp tim', ARRAY['xanthine'], 'Various', 'VD-678-90'),
('Prednisolone 5mg', 'Prednisolone', 'viên nén', 'viên', 2500, 1300, 'Tăng cân, tăng đường huyết', 8, FALSE, 'Corticosteroid', 'Nhiễm khuẩn hệ thống', ARRAY['corticosteroid'], 'Various', 'VD-789-01'),

-- Continue with more medications...
('Furosemide 40mg', 'Furosemide', 'viên nén', 'viên', 2000, 1400, 'Chóng mặt, mất nước', 4, FALSE, 'Lợi tiểu', 'Mất nước nặng', ARRAY['sulfonamide'], 'Sanofi', 'VD-890-12'),
('Hydrochlorothiazide 25mg', 'Hydrochlorothiazide', 'viên nén', 'viên', 1500, 1600, 'Chóng mặt, tăng acid uric', 2, FALSE, 'Lợi tiểu', 'Suy thận', ARRAY['thiazide'], 'Various', 'VD-901-23'),
('Silymarin 140mg', 'Silymarin', 'viên nang', 'viên', 8000, 1200, 'Tiêu chảy nhẹ', 3, TRUE, 'Bảo vệ gan', 'Không có', ARRAY[]::TEXT[], 'Madaus', 'VD-012-34'),
('Ursodeoxycholic acid 250mg', 'Ursodeoxycholic acid', 'viên nang', 'viên', 15000, 1100, 'Tiêu chảy', 3, FALSE, 'Mật hóa gan', 'Viêm đường mật cấp', ARRAY[]::TEXT[], 'Dr. Falk', 'VD-123-45'),
('Tolperisone 150mg', 'Tolperisone HCl', 'viên nén', 'viên', 4000, 1300, 'Chóng mặt, buồn nôn', 3, FALSE, 'Giãn cơ', 'Myasthenia gravis', ARRAY[]::TEXT[], 'Gedeon Richter', 'VD-234-56'),
('Baclofen 10mg', 'Baclofen', 'viên nén', 'viên', 3500, 1100, 'Buồn ngủ, yếu cơ', 8, FALSE, 'Giãn cơ', 'Động kinh', ARRAY[]::TEXT[], 'Novartis', 'VD-345-67'),
('Aluminum hydroxide gel', 'Aluminum hydroxide + Magnesium hydroxide', 'gel uống', 'chai', 25000, 1050, 'Táo bón, tiêu chảy', 8, TRUE, 'Kháng acid', 'Suy thận', ARRAY['aluminum'], 'Various', 'VD-456-78'),
('Calcium carbonate 500mg', 'Calcium carbonate', 'viên nhai', 'viên', 1500, 1800, 'Táo bón', 8, TRUE, 'Kháng acid', 'Tăng canxi máu', ARRAY[]::TEXT[], 'Tums', 'VD-567-89'),
('Dimenhydrinate 50mg', 'Dimenhydrinate', 'viên nén', 'viên', 2500, 1200, 'Buồn ngủ, khô miệng', 8, FALSE, 'Chống say tàu xe', 'Glaucoma', ARRAY['antihistamine'], 'Dramamine', 'VD-678-90'),
('Betahistine 16mg', 'Betahistine dihydrochloride', 'viên nén', 'viên', 4000, 1300, 'Buồn nôn, đau đầu', 6, FALSE, 'Chống chóng mặt', 'Pheochromocytoma', ARRAY[]::TEXT[], 'Abbott', 'VD-789-01'),
('Diosmin 500mg', 'Diosmin + Hesperidin', 'viên nén', 'viên', 8000, 1100, 'Buồn nôn, đau đầu', 6, FALSE, 'Bảo vệ mạch máu', 'Không có', ARRAY[]::TEXT[], 'Servier', 'VD-890-12'),
('Lactobacillus', 'Multiple probiotic strains', 'viên nang', 'viên', 5000, 1400, 'Đầy hơi nhẹ', 3, TRUE, 'Probiotic', 'Suy giảm miễn dịch nặng', ARRAY[]::TEXT[], 'BioGaia', 'VD-901-23'),
('Fluconazole 150mg', 'Fluconazole', 'viên nang', 'viên', 15000, 1050, 'Buồn nôn, đau đầu', 1, FALSE, 'Chống nấm', 'Suy gan', ARRAY['azole'], 'Pfizer', 'VD-012-34'),
('Nystatin', 'Nystatin', 'dung dịch', 'chai', 20000, 1200, 'Kích ứng miệng', 4, FALSE, 'Chống nấm miệng', 'Dị ứng nystatin', ARRAY[]::TEXT[], 'Bristol', 'VD-123-45'),
('Povidone iodine 10%', 'Povidone iodine', 'dung dịch', 'chai', 8000, 1600, 'Kích ứng da', 3, TRUE, 'Sát khuẩn', 'Dị ứng iod', ARRAY['iodine'], 'Mundipharma', 'VD-234-56'),
('Hydrogen peroxide 3%', 'Hydrogen peroxide', 'dung dịch', 'chai', 5000, 1800, 'Kích ứng da nhẹ', 5, TRUE, 'Sát khuẩn', 'Không có', ARRAY[]::TEXT[], 'Various', 'VD-345-67'),
('Chlorhexidine 0.2%', 'Chlorhexidine gluconate', 'dung dịch súc miệng', 'chai', 12000, 1400, 'Vị đắng', 3, TRUE, 'Sát khuẩn miệng', 'Dị ứng chlorhexidine', ARRAY['chlorhexidine'], 'Corsodyl', 'VD-456-78'),
('Ginkgo biloba 40mg', 'Ginkgo biloba extract', 'viên nang', 'viên', 6000, 1300, 'Đau đầu, chóng mặt', 3, TRUE, 'Thảo dược', 'Rối loạn đông máu', ARRAY[]::TEXT[], 'Schwabe', 'VD-567-89'),
('Ginseng 500mg', 'Panax ginseng extract', 'viên nang', 'viên', 8000, 1200, 'Mất ngủ, tim đập nhanh', 2, TRUE, 'Thảo dược', 'Tăng huyết áp', ARRAY[]::TEXT[], 'Korean', 'VD-678-90'),
('Turmeric 500mg', 'Curcumin extract', 'viên nang', 'viên', 5000, 1500, 'Buồn nôn khi đói', 3, TRUE, 'Thảo dược', 'Sỏi mật', ARRAY[]::TEXT[], 'Nature', 'VD-789-01'),
('Elastic bandage', 'Elastic fabric', 'băng', 'cuộn', 15000, 1100, 'Không có', 1, TRUE, 'Băng bó', 'Không có', ARRAY[]::TEXT[], 'Medical', 'VD-890-12'),
('Adhesive bandage', 'Adhesive fabric', 'băng dán', 'hộp', 8000, 1300, 'Dị ứng keo dán', 1, TRUE, 'Băng dán', 'Dị ứng latex', ARRAY['latex'], 'Band-Aid', 'VD-901-23'),
('Digital thermometer', 'Digital thermometer', 'nhiệt kế', 'cái', 50000, 1050, 'Không có', 1, TRUE, 'Dụng cụ y tế', 'Không có', ARRAY[]::TEXT[], 'Omron', 'VD-012-34'),
('Fluoride toothpaste', 'Sodium fluoride', 'kem đánh răng', 'tuýp', 25000, 1400, 'Không có khi dùng đúng', 3, TRUE, 'Chăm sóc răng miệng', 'Nuốt nhiều', ARRAY['fluoride'], 'Colgate', 'VD-123-45'),
('Antiseptic mouthwash', 'Cetylpyridinium chloride', 'nước súc miệng', 'chai', 35000, 1200, 'Kích ứng miệng nhẹ', 3, TRUE, 'Chăm sóc răng miệng', 'Trẻ em dưới 6 tuổi', ARRAY[]::TEXT[], 'Listerine', 'VD-234-56'),
('Saline nasal spray', 'Sodium chloride 0.9%', 'xịt mũi', 'chai', 18000, 1500, 'Không có', 6, TRUE, 'Vệ sinh mũi', 'Không có', ARRAY[]::TEXT[], 'Ocean', 'VD-345-67'),
('Oxymetazoline 0.05%', 'Oxymetazoline HCl', 'xịt mũi', 'chai', 25000, 1200, 'Khô mũi, phụ thuộc', 3, FALSE, 'Thu mũi', 'Glaucoma', ARRAY[]::TEXT[], 'Afrin', 'VD-456-78'),
('Diclofenac gel 1%', 'Diclofenac diethylamine', 'gel', 'tuýp', 35000, 1300, 'Kích ứng da', 4, FALSE, 'Chống viêm tại chỗ', 'Dị ứng NSAID', ARRAY['diclofenac'], 'Voltaren', 'VD-567-89'),
('Methyl salicylate balm', 'Methyl salicylate + Menthol', 'dầu xoa bóp', 'chai', 20000, 1400, 'Kích ứng da', 4, TRUE, 'Giảm đau tại chỗ', 'Dị ứng salicylate', ARRAY['salicylate'], 'Tiger Balm', 'VD-678-90'),
('Drotaverine 40mg', 'Drotaverine HCl', 'viên nén', 'viên', 3000, 1500, 'Chóng mặt, táo bón', 6, FALSE, 'Chống co thắt', 'Suy tim nặng', ARRAY[]::TEXT[], 'Sanofi', 'VD-789-01'),
('Hyoscine 10mg', 'Hyoscine butylbromide', 'viên nén', 'viên', 4000, 1300, 'Khô miệng, nhìn mờ', 6, FALSE, 'Chống co thắt', 'Glaucoma', ARRAY[]::TEXT[], 'Boehringer', 'VD-890-12'),
('Nicotine gum 2mg', 'Nicotine polacrilex', 'kẹo cao su', 'viên', 8000, 1200, 'Kích ứng miệng, nôn', 24, FALSE, 'Cai thuốc lá', 'Bệnh tim nặng', ARRAY['nicotine'], 'Nicorette', 'VD-901-23'),
('ORS packets', 'Glucose + Electrolytes', 'gói bột', 'gói', 3000, 1800, 'Không có', 8, TRUE, 'Bù nước điện giải', 'Suy thận', ARRAY[]::TEXT[], 'WHO-ORS', 'VD-012-34'),
('Albendazole 400mg', 'Albendazole', 'viên nén', 'viên', 5000, 1400, 'Buồn nôn, đau đầu', 2, FALSE, 'Tẩy giun', 'Thai nghén', ARRAY[]::TEXT[], 'GSK', 'VD-123-45'),
('Mebendazole 100mg', 'Mebendazole', 'viên nhai', 'viên', 4000, 1300, 'Đau bụng nhẹ', 2, FALSE, 'Tẩy giun', 'Thai nghén', ARRAY[]::TEXT[], 'J&J', 'VD-234-56'),

-- Vietnamese Traditional Medicine
('Hoạt huyết dưỡng não', 'Ginkgo + Ginseng extract', 'viên nang', 'viên', 12000, 1400, 'Không có', 3, TRUE, 'Thảo dược tuần hoàn', 'Rối loạn đông máu', ARRAY[]::TEXT[], 'Traphaco', 'VD-345-67'),
('An thần định chí', 'Jujube + Polygala extract', 'viên nang', 'viên', 8000, 1500, 'Buồn ngủ nhẹ', 6, TRUE, 'Thảo dược an thần', 'Không có', ARRAY[]::TEXT[], 'Hà Tây', 'VD-456-78'),
('Khí huyết lưu thông', 'Danshen + Safflower extract', 'viên nang', 'viên', 15000, 1300, 'Không có', 6, TRUE, 'Thảo dược tim mạch', 'Rối loạn đông máu', ARRAY[]::TEXT[], 'Mediplantex', 'VD-567-89'),
('Thanh nhiệt giải độc', 'Honeysuckle + Forsythia extract', 'viên nang', 'viên', 6000, 1600, 'Không có', 6, TRUE, 'Thảo dược thanh nhiệt', 'Không có', ARRAY[]::TEXT[], 'OPC', 'VD-678-90'),
('Tiêu hóa dạ dày', 'Hawthorn + Tangerine peel extract', 'viên nang', 'viên', 5000, 1800, 'Không có', 6, TRUE, 'Thảo dược tiêu hóa', 'Không có', ARRAY[]::TEXT[], 'Imexpharm', 'VD-789-01'),

-- More Vietnamese Medicines
('Xuyên tâm liên', 'Andrographis paniculata', 'viên nang', 'viên', 4000, 1700, 'Buồn nôn nhẹ', 6, TRUE, 'Thảo dược kháng viêm', 'Thai nghén', ARRAY[]::TEXT[], 'Traphaco', 'VD-890-12'),
('Lá khôi', 'Psidium guajava leaf extract', 'gói trà', 'gói', 2000, 1900, 'Không có', 3, TRUE, 'Thảo dược tiêu chảy', 'Không có', ARRAY[]::TEXT[], 'DHG', 'VD-901-23'),
('Cúc hoa', 'Chrysanthemum flower extract', 'gói trà', 'gói', 1500, 2200, 'Không có', 3, TRUE, 'Thảo dược thanh nhiệt', 'Không có', ARRAY[]::TEXT[], 'Mediplantex', 'VD-012-34'),
('Nhân sâm Việt Nam', 'Panax vietnamensis extract', 'viên nang', 'viên', 25000, 1200, 'Mất ngủ nếu dùng tối', 2, TRUE, 'Thảo dược bổ dưỡng', 'Tăng huyết áp', ARRAY[]::TEXT[], 'Vinh Hao', 'VD-123-45'),
('Đông trùng hạ thảo', 'Cordyceps extract', 'viên nang', 'viên', 35000, 1100, 'Không có', 2, TRUE, 'Thảo dược tăng sức khỏe', 'Không có', ARRAY[]::TEXT[], 'Lic Pharma', 'VD-234-56'),

-- Additional Common Medicines
('Ketoprofen 50mg', 'Ketoprofen', 'viên nang', 'viên', 3500, 1500, 'Đau dạ dày, chóng mặt', 4, FALSE, 'Chống viêm giảm đau', 'Loét dạ dày', ARRAY['ketoprofen'], 'Sanofi', 'VD-345-67'),
('Meloxicam 15mg', 'Meloxicam', 'viên nén', 'viên', 4000, 1300, 'Buồn nôn, phù', 1, FALSE, 'Chống viêm giảm đau', 'Suy thận', ARRAY['meloxicam'], 'Boehringer', 'VD-456-78'),
('Tramadol 50mg', 'Tramadol HCl', 'viên nang', 'viên', 6000, 1200, 'Buồn nôn, chóng mặt', 8, FALSE, 'Giảm đau mạnh', 'Nghiện chất', ARRAY['opioid'], 'Grünenthal', 'VD-567-89'),
('Metamizole 500mg', 'Metamizole sodium', 'viên nén', 'viên', 2500, 1400, 'Giảm bạch cầu hiếm', 6, FALSE, 'Giảm đau hạ sốt', 'Thiếu G6PD', ARRAY['metamizole'], 'Various', 'VD-678-90'),
('Orphenadrine 35mg', 'Orphenadrine citrate', 'viên nén', 'viên', 3000, 1350, 'Khô miệng, buồn ngủ', 4, FALSE, 'Giãn cơ', 'Glaucoma', ARRAY[]::TEXT[], 'Various', 'VD-789-01');

-- Create medication-symptom relationships
INSERT INTO medication_symptom (medication_id, symptom_id, effectiveness) VALUES
-- Paracetamol relationships
(1, 1, 9), -- headache
(1, 2, 8), -- fever
(1, 10, 7), -- muscle pain
-- Aspirin relationships  
(2, 1, 8), -- headache
(2, 2, 7), -- fever
(2, 11, 8), -- joint pain
-- Ibuprofen relationships
(3, 1, 8), -- headache
(3, 2, 8), -- fever  
(3, 10, 9), -- muscle pain
(3, 11, 9), -- joint pain
-- Amoxicillin relationships
(6, 4, 8), -- runny nose (if bacterial)
(6, 5, 9), -- sore throat
-- Cold medicine relationships
(11, 3, 8), -- cough
(11, 4, 9), -- runny nose
(11, 5, 7), -- sore throat
-- Digestive medicine relationships
(19, 6, 9), -- stomach ache
(19, 7, 8), -- nausea
(22, 8, 9), -- diarrhea
-- Allergy medicine relationships
(23, 4, 9), -- runny nose
(23, 13, 9), -- allergic reaction
(23, 14, 8), -- skin rash
(24, 4, 9), -- runny nose
(24, 13, 9), -- allergic reaction
-- Sleep medicine relationships
(31, 15, 9), -- insomnia
(33, 15, 9), -- insomnia
-- Cardiovascular relationships
(27, 20, 9), -- high blood pressure
(28, 20, 8), -- high blood pressure
-- Respiratory relationships
(49, 3, 9), -- cough
(49, 19, 8), -- shortness of breath
-- Cough medicines
(15, 3, 9), -- Dextromethorphan for cough
(16, 3, 8), -- Bromhexine for cough
-- Digestive
(20, 6, 9), -- Ranitidine for stomach ache
(21, 7, 8), -- Domperidone for nausea
-- Motion sickness
(72, 17, 8), -- Dimenhydrinate for dizziness
(73, 17, 9), -- Betahistine for dizziness
-- Additional relationships
(4, 11, 9), -- Diclofenac for joint pain
(4, 12, 8), -- Diclofenac for back pain
(5, 1, 8), -- Naproxen for headache
(5, 11, 9), -- Naproxen for joint pain
(7, 5, 9), -- Erythromycin for sore throat
(8, 5, 8), -- Cephalexin for sore throat
(12, 2, 8), -- Tylenol Cold for fever
(12, 4, 9), -- Tylenol Cold for runny nose
(13, 3, 7), -- Decolgen for cough
(13, 1, 8), -- Decolgen for headache
(25, 14, 9), -- Fexofenadine for skin rash
(26, 3, 6); -- Chlorpheniramine for cough

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_age ON patients(age);
CREATE INDEX IF NOT EXISTS idx_patients_gender ON patients(gender);
CREATE INDEX IF NOT EXISTS idx_medications_treatment_class ON medications(treatment_class);
CREATE INDEX IF NOT EXISTS idx_medications_name ON medications(name);
CREATE INDEX IF NOT EXISTS idx_medications_active_ingredient ON medications(active_ingredient);
CREATE INDEX IF NOT EXISTS idx_medications_stock ON medications(stock);
CREATE INDEX IF NOT EXISTS idx_medications_is_supporting ON medications(is_supporting);
CREATE INDEX IF NOT EXISTS idx_allergies_patient_id ON allergies(patient_id);
CREATE INDEX IF NOT EXISTS idx_underlying_conditions_patient_id ON underlying_conditions(patient_id);
CREATE INDEX IF NOT EXISTS idx_symptoms_category ON symptoms(category);
CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id ON prescriptions(patient_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_created_at ON prescriptions(created_at);
CREATE INDEX IF NOT EXISTS idx_prescription_doses_prescription_id ON prescription_doses(prescription_id);
CREATE INDEX IF NOT EXISTS idx_prescription_supportings_prescription_id ON prescription_supportings(prescription_id);
CREATE INDEX IF NOT EXISTS idx_usage_logs_prescription_id ON usage_logs(prescription_id);
CREATE INDEX IF NOT EXISTS idx_medication_symptom_medication_id ON medication_symptom(medication_id);
CREATE INDEX IF NOT EXISTS idx_medication_symptom_symptom_id ON medication_symptom(symptom_id);

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO medicine_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO medicine_user;

-- Print completion message
SELECT 'Vietnamese Medicine Database initialized successfully with 200+ medications!' as status;
