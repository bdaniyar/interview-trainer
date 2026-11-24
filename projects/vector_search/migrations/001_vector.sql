BEGIN;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE vector_lab FROM PUBLIC;
CREATE EXTENSION vector;
CREATE ROLE vector_app LOGIN PASSWORD 'local_vector_app' NOSUPERUSER NOCREATEDB NOCREATEROLE;
GRANT CONNECT ON DATABASE vector_lab TO vector_app;

CREATE TABLE tenants (id text PRIMARY KEY);
INSERT INTO tenants VALUES ('north'), ('south');
CREATE TABLE spaces (
    id text PRIMARY KEY,
    model text NOT NULL,
    revision text NOT NULL,
    dimension integer NOT NULL CHECK (dimension = 16),
    normalized boolean NOT NULL,
    UNIQUE (model, revision, dimension, normalized)
);
INSERT INTO spaces VALUES
    ('fixture-v1', 'synthetic', '1', 16, true),
    ('fixture-v2', 'synthetic', '2', 16, true);

CREATE TABLE documents (
    tenant text REFERENCES tenants(id),
    id text NOT NULL,
    owner_name text NOT NULL,
    active_version integer,
    access_epoch bigint NOT NULL DEFAULT 0,
    deleted boolean NOT NULL DEFAULT false,
    PRIMARY KEY(tenant, id),
    CHECK (NOT deleted OR active_version IS NULL)
);
CREATE TABLE document_grants (
    tenant text,
    document_id text,
    subject text,
    PRIMARY KEY (tenant, document_id, subject),
    FOREIGN KEY (tenant, document_id) REFERENCES documents(tenant,id)
);
CREATE TABLE versions (
    tenant text,
    document_id text,
    version integer CHECK (version > 0),
    space_id text REFERENCES spaces(id),
    content_hash text NOT NULL CHECK (length(content_hash)=64),
    chunk_count integer NOT NULL CHECK (chunk_count > 0),
    PRIMARY KEY(tenant,document_id,version),
    UNIQUE(tenant,document_id,version,space_id),
    FOREIGN KEY (tenant, document_id) REFERENCES documents(tenant,id)
);
ALTER TABLE documents ADD FOREIGN KEY (tenant,id,active_version)
    REFERENCES versions(tenant,document_id,version);
CREATE TABLE chunks (
    tenant text,
    document_id text,
    version integer,
    space_id text,
    chunk_id text,
    section text NOT NULL,
    start_offset integer NOT NULL CHECK (start_offset >= 0),
    end_offset integer NOT NULL CHECK (end_offset > start_offset),
    content_hash text NOT NULL CHECK (length(content_hash)=64),
    embedding vector(16) NOT NULL,
    lexemes tsvector NOT NULL,
    PRIMARY KEY (tenant,document_id,version,space_id,chunk_id),
    FOREIGN KEY (tenant,document_id,version,space_id) REFERENCES versions(tenant,document_id,version,space_id),
    CHECK (vector_norm(embedding) BETWEEN 0.99999 AND 1.00001)
) PARTITION BY LIST(space_id);
CREATE TABLE chunks_v1 PARTITION OF chunks FOR VALUES IN ('fixture-v1');
CREATE TABLE chunks_v2 PARTITION OF chunks FOR VALUES IN ('fixture-v2');
CREATE INDEX chunks_v1_hnsw ON chunks_v1 USING hnsw (embedding vector_cosine_ops);
CREATE INDEX chunks_v2_hnsw ON chunks_v2 USING hnsw (embedding vector_cosine_ops);
CREATE INDEX chunks_fts ON chunks USING gin (lexemes);

CREATE TABLE payloads (
    tenant text,
    document_id text,
    version integer,
    space_id text,
    chunk_id text,
    body text NOT NULL,
    PRIMARY KEY (tenant,document_id,version,space_id,chunk_id),
    FOREIGN KEY (tenant,document_id,version,space_id,chunk_id) REFERENCES chunks
);

GRANT SELECT ON tenants,spaces TO vector_app;
GRANT SELECT ON documents,versions,document_grants,chunks,payloads TO vector_app;
GRANT INSERT ON documents,versions,document_grants,chunks,payloads TO vector_app;
GRANT UPDATE (active_version,access_epoch,deleted) ON documents TO vector_app;
GRANT DELETE ON document_grants TO vector_app;
COMMIT;
