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



-- ===== QUESTION SEED DATA =====

INSERT INTO questions (section, difficulty, text, options, correct_option, weight)

VALUES

-- Logical

('logical', 'medium',

 'If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?',

 '["Yes", "No", "Cannot be determined", "Only sometimes"]',

 'Yes', 1.0),



('logical', 'hard',

 'A train leaves Station A at 6 PM and reaches Station B at 10 PM. Another train leaves Station B at 8 PM and reaches Station A at 11 PM. At what time do they cross each other?',

 '["7 PM", "8:15 PM", "8:30 PM", "8:45 PM"]',

 '8:30 PM', 1.5),



-- Numerical

('numerical', 'medium',

 'A company''s profit increased from INR2 lakh to INR2.5 lakh. What is the percentage increase?',

 '["10%", "20%", "25%", "50%"]',

 '25%', 1.0),



('numerical', 'hard',

 'If the average of 5 consecutive odd numbers is 25, what is the largest number?',

 '["27", "29", "31", "33"]',

 '29', 1.2),



-- Verbal

('verbal', 'medium',

 'Choose the correct synonym for "Ambiguous".',

 '["Clear", "Vague", "Precise", "Certain"]',

 'Vague', 1.0),



('verbal', 'hard',

 'Select the correct option: "She insisted ____ going out."',

 '["in", "on", "at", "for"]',

 'on', 1.0),



-- Creative

('creative', 'medium',

 'You are designing a new logo for an eco-friendly brand. Which concept suits best?',

 '["Tree made of circuit lines", "Burning globe", "Skyscraper silhouette", "Car logo"]',

 'Tree made of circuit lines', 1.0),



('creative', 'hard',

 'A storytelling ad must evoke emotions while promoting a product. Which is the most creative approach?',

 '["Show specs and prices", "Highlight user success story", "Focus on brand colors", "Use only text slides"]',

 'Highlight user success story', 1.2),



-- Empathy

('empathy', 'medium',

 'Your colleague seems withdrawn and quiet during meetings. What should you do?',

 '["Ignore it", "Confront them publicly", "Ask privately if they''re okay", "Report to HR immediately"]',

 'Ask privately if they''re okay', 1.0),

('empathy', 'hard',

 'A patient is anxious before surgery. What''s the best response?',

 '["Tell them to relax", "Explain clearly what to expect", "Avoid talking", "Rush through the procedure"]',

 'Explain clearly what to expect', 1.2);

