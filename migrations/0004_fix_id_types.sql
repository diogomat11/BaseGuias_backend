-- Migration 0004: Fix id_paciente and id_pagamento to Integer type
-- Date: 2026-01-10

-- Drop indexes first
DROP INDEX IF EXISTS idx_carteirinhas_id_paciente;
DROP INDEX IF EXISTS idx_carteirinhas_id_pagamento;

-- Change column types to INTEGER
-- Use USING clause to convert text to integer
ALTER TABLE carteirinhas 
ALTER COLUMN id_paciente TYPE INTEGER USING id_paciente::INTEGER;

ALTER TABLE carteirinhas 
ALTER COLUMN id_pagamento TYPE INTEGER USING id_pagamento::INTEGER;

-- Recreate indexes
CREATE INDEX idx_carteirinhas_id_paciente 
ON carteirinhas(id_paciente);

CREATE INDEX idx_carteirinhas_id_pagamento 
ON carteirinhas(id_pagamento);
