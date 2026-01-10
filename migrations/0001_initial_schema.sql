-- Migration 0001: Initial Schema

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    api_key TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('Ativo', 'Inativo')),
    validade DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS carteirinhas (
    id SERIAL PRIMARY KEY,
    carteirinha TEXT NOT NULL UNIQUE,
    paciente TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    carteirinha_id INTEGER REFERENCES carteirinhas(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('success', 'pending', 'processing', 'error')),
    attempts INTEGER DEFAULT 0,
    priority INTEGER DEFAULT 0,
    locked_by TEXT, -- Server URL that locked this job
    timeout TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS base_guias (
    id SERIAL PRIMARY KEY,
    carteirinha_id INTEGER REFERENCES carteirinhas(id) ON DELETE CASCADE,
    guia TEXT,
    data_autorizacao DATE,
    senha TEXT,
    validade DATE,
    codigo_terapia TEXT,
    nome_terapia TEXT,
    sessoes_autorizadas INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_locked_by ON jobs(locked_by);
CREATE INDEX idx_base_guias_carteirinha ON base_guias(carteirinha_id);
