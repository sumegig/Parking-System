-- Parkolóhelyek beszúrása
CREATE TABLE IF NOT EXISTS parking_spaces (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(30) NOT NULL DEFAULT 'REGULAR',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservations (
    id SERIAL PRIMARY KEY,
    parking_space_id INT NOT NULL REFERENCES parking_spaces(id) ON DELETE CASCADE,
    applicant_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'CONFIRMED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Alap értékek inicializálása
INSERT INTO parking_spaces (code, type, is_active) VALUES
('A-101', 'REGULAR', TRUE),
('A-102', 'REGULAR', TRUE),
('B-201', 'ELECTRIC_VEHICLE', TRUE),  -- felkészülés az extra feladatra
('C-301', 'HANDICAPPED', TRUE)       -- felkészülés az extra feladatra
ON CONFLICT (code) DO NOTHING;