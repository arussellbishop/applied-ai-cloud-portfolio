CREATE TABLE IF NOT EXISTS standard_requirements (
  requirement_id TEXT PRIMARY KEY,
  standard TEXT NOT NULL,
  clause_or_reference TEXT,
  requirement_summary TEXT NOT NULL,
  applicable TEXT NOT NULL,
  control_ids TEXT,
  evidence_required TEXT,
  test_method TEXT,
  decision TEXT,
  status TEXT NOT NULL DEFAULT 'OPEN',
  owner TEXT,
  review_date TEXT,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS requirement_evidence (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  requirement_id TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  reviewer TEXT,
  review_date TEXT,
  result TEXT,
  notes TEXT,
  FOREIGN KEY(requirement_id) REFERENCES standard_requirements(requirement_id)
);
CREATE TABLE IF NOT EXISTS assessment_decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  requirement_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL,
  decision_owner TEXT NOT NULL,
  decision_date TEXT NOT NULL,
  follow_up_date TEXT,
  FOREIGN KEY(requirement_id) REFERENCES standard_requirements(requirement_id)
);
