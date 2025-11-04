-- ===========================
-- Career Knowledge Base Seed
-- ===========================

-- Data Scientist (id = 1)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(1, 'Essential Skills', 'Master Python, statistics, and machine learning fundamentals.', '{"python","ml","statistics"}'),
(1, 'Certifications', 'Recommended: TensorFlow Developer, AWS Data Specialty.', '{"certification","aws","tensorflow"}'),
(1, 'Interview Prep', 'Focus on SQL, ML algorithms, and scenario-based questions.', '{"interview","ml","sql"}');

-- Business Analyst (id = 2)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(2, 'Essential Skills', 'Develop strong analytical, documentation, and stakeholder communication skills.', '{"analytics","communication","requirements"}'),
(2, 'Certifications', 'Recommended: CBAP, PMI-PBA, or Google Data Analytics Certificate.', '{"cbap","pmi","google"}'),
(2, 'Interview Prep', 'Prepare for case studies and data interpretation questions.', '{"interview","case-study"}');

-- Software Engineer (id = 3)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(3, 'Essential Skills', 'Master data structures, algorithms, and version control systems.', '{"programming","algorithms","git"}'),
(3, 'Certifications', 'Recommended: AWS Developer, Microsoft Certified: Azure Developer.', '{"aws","azure"}'),
(3, 'Interview Prep', 'Practice coding problems on LeetCode or HackerRank.', '{"interview","coding"}');

-- DevOps Engineer (id = 4)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(4, 'Essential Skills', 'Learn CI/CD pipelines, Docker, and cloud infrastructure.', '{"docker","kubernetes","ci/cd"}'),
(4, 'Certifications', 'Recommended: AWS DevOps Engineer Professional, Docker Certified Associate.', '{"aws","docker"}'),
(4, 'Interview Prep', 'Be ready to explain deployment pipelines and automation scripts.', '{"interview","deployment"}');

-- Product Manager (id = 5)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(5, 'Essential Skills', 'Develop business acumen, leadership, and user research skills.', '{"leadership","research","communication"}'),
(5, 'Certifications', 'Recommended: Pragmatic Institute PM, AIPMM Certified Product Manager.', '{"product-management","certification"}'),
(5, 'Interview Prep', 'Focus on product strategy and metrics (OKRs, KPIs).', '{"interview","strategy"}');

-- UX Designer (id = 7)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(7, 'Essential Skills', 'Build expertise in Figma, usability testing, and design systems.', '{"figma","design","usability"}'),
(7, 'Certifications', 'Recommended: Google UX Design Certificate.', '{"ux","google","certification"}'),
(7, 'Interview Prep', 'Prepare a strong portfolio with detailed case studies.', '{"portfolio","interview"}');

-- Health Informatics Specialist (id = 9)
INSERT INTO career_kb (career_id, title, content, tags) VALUES
(9, 'Essential Skills', 'Learn EHR systems, healthcare analytics, and data compliance (HIPAA).', '{"ehr","hipaa","data"}'),
(9, 'Certifications', 'Recommended: CHDA, RHIA.', '{"chda","rhia"}'),
(9, 'Interview Prep', 'Be ready to discuss healthcare data workflows and patient outcomes.', '{"interview","data"}');
