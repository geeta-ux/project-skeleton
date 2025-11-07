-- ===== CAREER SEED DATA =====

INSERT INTO careers (title, track, skills, description, avg_salary_range, sample_roles)

VALUES

-- Data Track

('Data Scientist', 'Data',

 '{"skills": ["Analytical Thinking", "Python", "Machine Learning", "Data Visualization"]}',

 'Data Scientists analyze complex datasets to extract insights and build predictive models for decision-making.',

 'INR8-25 LPA',

 '["Data Analyst", "Machine Learning Engineer", "Data Engineer"]'),



('Business Analyst', 'Data',

 '{"skills": ["Analytical Thinking", "SQL", "Communication", "Excel"]}',

 'Business Analysts interpret data trends to support business strategy and improve performance.',

 'INR6-18 LPA',

 '["Operations Analyst", "Strategy Analyst", "BI Specialist"]'),



-- Software Track

('Software Engineer', 'Software',

 '{"skills": ["Programming", "Problem Solving", "Algorithms", "Debugging"]}',

 'Software Engineers design, develop, and test software applications and systems.',

 'INR7-20 LPA',

 '["Backend Developer", "Frontend Developer", "Full Stack Developer"]'),



('DevOps Engineer', 'Software',

 '{"skills": ["Automation", "Linux", "Cloud Infrastructure", "Scripting"]}',

 'DevOps Engineers streamline software deployment and infrastructure management for faster delivery cycles.',

 'INR9-22 LPA',

 '["Site Reliability Engineer", "Cloud Engineer", "Infrastructure Specialist"]'),



-- Product Track

('Product Manager', 'Product',

 '{"skills": ["Communication", "Analytical Thinking", "Leadership", "User Research"]}',

 'Product Managers lead cross-functional teams to design and deliver impactful products.',

 'INR12-30 LPA',

 '["Associate Product Manager", "Growth PM", "Technical PM"]'),



('Business Development Manager', 'Product',

 '{"skills": ["Negotiation", "Strategy", "Market Research", "Communication"]}',

 'BD Managers identify growth opportunities, partnerships, and market expansion strategies.',

 'INR8-20 LPA',

 '["Account Manager", "Sales Strategy Lead", "Partnership Manager"]'),



-- Design Track

('UX Designer', 'Design',

 '{"skills": ["Creativity", "Empathy", "Prototyping", "User Research"]}',

 'UX Designers craft intuitive and engaging experiences based on user behavior and psychology.',

 'INR7-18 LPA',

 '["UI Designer", "Interaction Designer", "User Researcher"]'),



('Graphic Designer', 'Design',

 '{"skills": ["Creativity", "Visual Design", "Adobe Suite", "Branding"]}',

 'Graphic Designers communicate ideas visually through logos, layouts, and marketing materials.',

 'INR4-12 LPA',

 '["Brand Designer", "Illustrator", "Visual Communication Specialist"]'),



-- Health-Informatics Track

('Health Informatics Specialist', 'Health-Informatics',

 '{"skills": ["Empathy", "Data Management", "Healthcare Systems", "Analytics"]}',

 'Health Informatics Specialists combine healthcare knowledge and IT to optimize patient care through data.',

 'INR8-22 LPA',

 '["Clinical Data Analyst", "Health IT Consultant", "Medical Data Manager"]'),



('Clinical Research Associate', 'Health-Informatics',

 '{"skills": ["Empathy", "Attention to Detail", "Medical Knowledge", "Reporting"]}',

 'CRAs plan and monitor clinical trials to ensure data accuracy and patient safety.',

 'INR6-18 LPA',

 '["Clinical Data Coordinator", "Regulatory Associate", "Research Monitor"]');
