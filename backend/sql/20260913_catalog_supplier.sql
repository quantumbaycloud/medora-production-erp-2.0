-- MEDORAX ERP commercial catalog + supplier master migration
CREATE TABLE IF NOT EXISTS catalog_options (
  id VARCHAR PRIMARY KEY,
  pharmacy_id VARCHAR(128) NOT NULL REFERENCES pharmacies(id) ON DELETE CASCADE,
  option_type VARCHAR(60) NOT NULL,
  code VARCHAR(80) NOT NULL,
  name VARCHAR(160) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  sort_order INTEGER NOT NULL DEFAULT 0,
  metadata_json TEXT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_catalog_pharmacy_type_code UNIQUE (pharmacy_id, option_type, code)
);
CREATE INDEX IF NOT EXISTS ix_catalog_pharmacy_id ON catalog_options(pharmacy_id);
CREATE INDEX IF NOT EXISTS ix_catalog_option_type ON catalog_options(option_type);
ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS category_id VARCHAR REFERENCES catalog_options(id) ON DELETE SET NULL;
ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS status VARCHAR(30) NOT NULL DEFAULT 'active';
ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS description VARCHAR;
CREATE INDEX IF NOT EXISTS ix_suppliers_category_id ON suppliers(category_id);
CREATE INDEX IF NOT EXISTS ix_suppliers_status ON suppliers(status);
