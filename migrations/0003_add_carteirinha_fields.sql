-- Migration 0003: Add id_paciente, id_pagamento, and status to carteirinhas
-- Date: 2026-01-10

-- Add new columns
ALTER TABLE carteirinhas 
ADD COLUMN IF NOT EXISTS id_paciente TEXT,
ADD COLUMN IF NOT EXISTS id_pagamento TEXT,
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'ativo';

-- Update existing records to have default status
UPDATE carteirinhas 
SET status = 'ativo' 
WHERE status IS NULL;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_carteirinhas_id_paciente 
ON carteirinhas(id_paciente);

CREATE INDEX IF NOT EXISTS idx_carteirinhas_id_pagamento 
ON carteirinhas(id_pagamento);

CREATE INDEX IF NOT EXISTS idx_carteirinhas_status 
ON carteirinhas(status);
