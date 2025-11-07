-- =====================================================
-- SEED DATA: Learning Plans by Track
-- Each entry is linked to a result (when created)
-- =====================================================

INSERT INTO plans (result_id, plan_json)
VALUES

-- =======================
-- DATA TRACK
-- =======================
(1, '{
    "track": "Data",
    "stages": [
        {
            "stage": "Beginner",
            "milestones": [
                "Learn Python and SQL",
                "Understand basic statistics",
                "Practice data cleaning with Pandas",
                "Build simple dashboards"
            ],
            "duration": "3-6 months"
        },
        {
            "stage": "Intermediate",
            "milestones": [
                "Learn data visualization (Tableau/Power BI)",
                "Explore machine learning",
                "Work on Kaggle datasets",
                "Build portfolio projects"
            ],
            "duration": "6-12 months"
        },
        {
            "stage": "Advanced",
            "milestones": [
                "Specialize in NLP or Deep Learning",
                "Contribute to open-source ML projects",
                "Publish data blogs",
                "Interview for data science roles"
            ],
            "duration": "12-24 months"
        }
    ]
}'),

-- =======================
-- SOFTWARE TRACK
-- =======================
(2, '{
    "track": "Software",
    "stages": [
        {
            "stage": "Beginner",
            "milestones": [
                "Learn Python or JavaScript",
                "Understand version control (Git)",
                "Build small CLI projects",
                "Debug simple programs"
            ],
            "duration": "3-6 months"
        },
        {
            "stage": "Intermediate",
            "milestones": [
                "Work with frameworks (Flask, Django, React)",
                "Learn databases and APIs",
                "Build and deploy web apps",
                "Write unit tests"
            ],
            "duration": "6-12 months"
        },
        {
            "stage": "Advanced",
            "milestones": [
                "Master system design",
                "Contribute to open-source",
                "Optimize performance and scalability",
                "Prepare for technical interviews"
            ],
            "duration": "12-24 months"
        }
    ]
}'),

-- =======================
-- PRODUCT TRACK
-- =======================
(3, '{
    "track": "Product",
    "stages": [
        {
            "stage": "Beginner",
            "milestones": [
                "Understand product lifecycle",
                "Learn user research basics",
                "Study product case studies",
                "Develop communication skills"
            ],
            "duration": "3-6 months"
        },
        {
            "stage": "Intermediate",
            "milestones": [
                "Run mock product sprints",
                "Learn metrics and A/B testing",
                "Use analytics tools (Mixpanel, GA)",
                "Collaborate with tech/design teams"
            ],
            "duration": "6-12 months"
        },
        {
            "stage": "Advanced",
            "milestones": [
                "Lead product strategy",
                "Run growth experiments",
                "Mentor junior PMs",
                "Own product roadmap delivery"
            ],
            "duration": "12-24 months"
        }
    ]
}'),

-- =======================
-- DESIGN TRACK
-- =======================
(4, '{
    "track": "Design",
    "stages": [
        {
            "stage": "Beginner",
            "milestones": [
                "Learn Figma or Sketch",
                "Understand color and typography",
                "Practice wireframing",
                "Study UX principles"
            ],
            "duration": "3-6 months"
        },
        {
            "stage": "Intermediate",
            "milestones": [
                "Work on UI projects",
                "Build a personal portfolio",
                "Master design systems",
                "Gather user feedback"
            ],
            "duration": "6-12 months"
        },
        {
            "stage": "Advanced",
            "milestones": [
                "Lead UX workshops",
                "Mentor junior designers",
                "Contribute to open design systems",
                "Explore motion and interaction design"
            ],
            "duration": "12-24 months"
        }
    ]
}'),

-- =======================
-- HEALTH-INFORMATICS TRACK
-- =======================
(5, '{
    "track": "Health-Informatics",
    "stages": [
        {
            "stage": "Beginner",
            "milestones": [
                "Understand healthcare systems",
                "Learn EHR and data privacy basics",
                "Study data ethics",
                "Practice simple analytics"
            ],
            "duration": "3-6 months"
        },
        {
            "stage": "Intermediate",
            "milestones": [
                "Work with healthcare datasets",
                "Visualize clinical metrics",
                "Learn interoperability standards (HL7, FHIR)",
                "Support reporting teams"
            ],
            "duration": "6-12 months"
        },
        {
            "stage": "Advanced",
            "milestones": [
                "Lead analytics initiatives",
                "Implement predictive models",
                "Collaborate with clinicians",
                "Publish informatics research"
            ],
            "duration": "12-24 months"
        }
    ]
}');
