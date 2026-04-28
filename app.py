# app.py
from flask import Flask, render_template, request, redirect, url_for, session, abort
import os
import random
import json

app = Flask(__name__)
app.secret_key = 'career_compass_super_secret_key_2026'  # Required for session management

# ==================================================
# CAREER DATA AND ANALYSIS LOGIC (Simulated AI)
# ==================================================

# Career categories and their display names
CAREERS = {
    'software_engineer': {
        'name': 'Software Engineer',
        'icon': 'fa-code',
        'color': '#4F46E5',
        'description': 'Design, develop, and maintain software systems and applications.'
    },
    'data_scientist': {
        'name': 'Data Scientist',
        'icon': 'fa-chart-line',
        'color': '#22C55E',
        'description': 'Extract insights and build predictive models from complex data.'
    },
    'ux_designer': {
        'name': 'UX/UI Designer',
        'icon': 'fa-paintbrush',
        'color': '#8B5CF6',
        'description': 'Create intuitive and beautiful user experiences for digital products.'
    },
    'cybersecurity': {
        'name': 'Cybersecurity Analyst',
        'icon': 'fa-shield-halved',
        'color': '#EF4444',
        'description': 'Protect systems and networks from digital threats and attacks.'
    },
    'ai_engineer': {
        'name': 'AI/ML Engineer',
        'icon': 'fa-brain',
        'color': '#EC4899',
        'description': 'Develop and implement artificial intelligence models and algorithms.'
    },
    'product_manager': {
        'name': 'Product Manager',
        'icon': 'fa-lightbulb',
        'color': '#F59E0B',
        'description': 'Define the product vision and lead cross-functional teams to deliver value.'
    },
    'cloud_architect': {
        'name': 'Cloud Architect',
        'icon': 'fa-cloud',
        'color': '#0EA5E9',
        'description': 'Design and manage scalable cloud infrastructure and systems.'
    },
    'marketing': {
        'name': 'Digital Marketing Specialist',
        'icon': 'fa-bullhorn',
        'color': '#F59E0B',
        'description': 'Drive brand growth through strategic online marketing campaigns.'
    }
}

# Questions for the AI Career Quiz (10 questions)
QUESTIONS = [
    {
        'id': 1,
        'text': 'How do you prefer to solve problems?',
        'options': [
            {'text': 'Writing step-by-step logical solutions', 'scores': {'software_engineer': 5, 'data_scientist': 2, 'cybersecurity': 3, 'ai_engineer': 4, 'cloud_architect': 3}},
            {'text': 'Finding patterns and analyzing data', 'scores': {'data_scientist': 5, 'ai_engineer': 5, 'software_engineer': 1, 'cybersecurity': 2}},
            {'text': 'Creating visual and interactive designs', 'scores': {'ux_designer': 5, 'product_manager': 2, 'software_engineer': 1}},
            {'text': 'Leading teams and defining product goals', 'scores': {'product_manager': 5, 'ux_designer': 2, 'software_engineer': 1}},
            {'text': 'Identifying security vulnerabilities', 'scores': {'cybersecurity': 5, 'cloud_architect': 4, 'software_engineer': 2}}
        ]
    },
    {
        'id': 2,
        'text': 'What type of tasks energize you the most?',
        'options': [
            {'text': 'Building functional applications from scratch', 'scores': {'software_engineer': 5, 'cybersecurity': 2, 'ai_engineer': 3, 'cloud_architect': 4}},
            {'text': 'Analyzing datasets and finding trends', 'scores': {'data_scientist': 5, 'ai_engineer': 5, 'product_manager': 2}},
            {'text': 'Creating user flows and wireframes', 'scores': {'ux_designer': 5, 'product_manager': 3, 'software_engineer': 1}},
            {'text': 'Developing security protocols', 'scores': {'cybersecurity': 5, 'cloud_architect': 5, 'software_engineer': 3}},
            {'text': 'Defining product vision and roadmaps', 'scores': {'product_manager': 5, 'ux_designer': 2, 'data_scientist': 1}}
        ]
    },
    {
        'id': 3,
        'text': 'Rate your interest in mathematics and statistics:',
        'options': [
            {'text': 'Very high - I love working with numbers', 'scores': {'data_scientist': 5, 'ai_engineer': 5, 'software_engineer': 2, 'cybersecurity': 2}},
            {'text': 'Moderate - I can work with them if needed', 'scores': {'software_engineer': 3, 'cloud_architect': 3, 'product_manager': 3}},
            {'text': 'Low - I prefer creative or practical tasks', 'scores': {'ux_designer': 4, 'product_manager': 4, 'software_engineer': 1}},
            {'text': 'Not at all - I avoid math whenever possible', 'scores': {'ux_designer': 3, 'product_manager': 3}}
        ]
    },
    {
        'id': 4,
        'text': 'What is your preferred working style?',
        'options': [
            {'text': 'Working alone on complex technical problems', 'scores': {'software_engineer': 4, 'data_scientist': 4, 'cybersecurity': 4, 'ux_designer': 1, 'marketing': 0}},
            {'text': 'Collaborating with a creative team', 'scores': {'ux_designer': 5, 'marketing': 4, 'software_engineer': 1, 'data_scientist': 1, 'cybersecurity': 1}},
            {'text': 'Leading projects and influencing people', 'scores': {'marketing': 5, 'ux_designer': 3, 'software_engineer': 2, 'data_scientist': 2, 'cybersecurity': 2}},
            {'text': 'A mix of independent and team work', 'scores': {'software_engineer': 3, 'data_scientist': 3, 'cybersecurity': 3, 'ux_designer': 3, 'marketing': 3}}
        ]
    },
    {
        'id': 5,
        'text': 'Which high school subject did you enjoy most?',
        'options': [
            {'text': 'Computer Science / Programming', 'scores': {'software_engineer': 5, 'data_scientist': 4, 'cybersecurity': 4, 'ux_designer': 1, 'marketing': 0}},
            {'text': 'Mathematics / Statistics', 'scores': {'data_scientist': 5, 'software_engineer': 3, 'cybersecurity': 2, 'marketing': 1, 'ux_designer': 0}},
            {'text': 'Art / Design', 'scores': {'ux_designer': 5, 'marketing': 3, 'software_engineer': 0, 'data_scientist': 0, 'cybersecurity': 0}},
            {'text': 'Business / Economics', 'scores': {'marketing': 5, 'data_scientist': 2, 'software_engineer': 1, 'ux_designer': 1, 'cybersecurity': 0}},
            {'text': 'Psychology / Social Sciences', 'scores': {'marketing': 3, 'ux_designer': 4, 'cybersecurity': 1, 'data_scientist': 1, 'software_engineer': 0}}
        ]
    },
    {
        'id': 6,
        'text': 'How important is creativity in your ideal job?',
        'options': [
            {'text': 'Essential - I need to create something new daily', 'scores': {'ux_designer': 5, 'marketing': 4, 'software_engineer': 2, 'data_scientist': 1, 'cybersecurity': 0}},
            {'text': 'Important - I like some creative freedom', 'scores': {'ux_designer': 3, 'marketing': 3, 'software_engineer': 3, 'data_scientist': 2, 'cybersecurity': 1}},
            {'text': 'Not very important - I prefer structured work', 'scores': {'cybersecurity': 4, 'software_engineer': 3, 'data_scientist': 3, 'marketing': 1, 'ux_designer': 0}},
            {'text': 'Not important at all', 'scores': {'cybersecurity': 3, 'data_scientist': 2, 'software_engineer': 2, 'marketing': 0, 'ux_designer': 0}}
        ]
    },
    {
        'id': 7,
        'text': 'What is your approach to learning new technology?',
        'options': [
            {'text': 'I dive deep into documentation and code', 'scores': {'software_engineer': 5, 'cybersecurity': 4, 'data_scientist': 4, 'ux_designer': 1, 'marketing': 0}},
            {'text': 'I prefer visual tutorials and hands-on projects', 'scores': {'ux_designer': 5, 'software_engineer': 3, 'data_scientist': 2, 'marketing': 2, 'cybersecurity': 1}},
            {'text': 'I learn best by analyzing case studies', 'scores': {'data_scientist': 4, 'marketing': 4, 'cybersecurity': 3, 'software_engineer': 2, 'ux_designer': 1}},
            {'text': 'I need structured courses with clear goals', 'scores': {'cybersecurity': 3, 'data_scientist': 3, 'software_engineer': 3, 'ux_designer': 2, 'marketing': 2}}
        ]
    },
    {
        'id': 8,
        'text': 'How do you handle stress and pressure?',
        'options': [
            {'text': 'I thrive and perform better under tight deadlines', 'scores': {'marketing': 4, 'software_engineer': 3, 'cybersecurity': 4, 'data_scientist': 2, 'ux_designer': 1}},
            {'text': 'I stay calm and methodically work through problems', 'scores': {'data_scientist': 4, 'cybersecurity': 4, 'software_engineer': 3, 'ux_designer': 2, 'marketing': 1}},
            {'text': 'I prefer a low-pressure, steady environment', 'scores': {'ux_designer': 4, 'data_scientist': 3, 'software_engineer': 2, 'cybersecurity': 2, 'marketing': 1}},
            {'text': 'I use creative thinking to find solutions', 'scores': {'ux_designer': 4, 'marketing': 4, 'software_engineer': 2, 'data_scientist': 2, 'cybersecurity': 1}}
        ]
    },
    {
        'id': 9,
        'text': 'Which statement best describes your career goal?',
        'options': [
            {'text': 'Build innovative products that solve real problems', 'scores': {'software_engineer': 5, 'ux_designer': 4, 'data_scientist': 3, 'cybersecurity': 2, 'marketing': 1}},
            {'text': 'Discover insights that help businesses grow', 'scores': {'data_scientist': 5, 'marketing': 4, 'software_engineer': 2, 'cybersecurity': 1, 'ux_designer': 1}},
            {'text': 'Design beautiful and user-friendly interfaces', 'scores': {'ux_designer': 5, 'software_engineer': 3, 'marketing': 3, 'data_scientist': 0, 'cybersecurity': 0}},
            {'text': 'Protect people and organizations from cyber threats', 'scores': {'cybersecurity': 5, 'software_engineer': 2, 'data_scientist': 2, 'ux_designer': 0, 'marketing': 0}},
            {'text': 'Create impactful digital marketing campaigns', 'scores': {'marketing': 5, 'ux_designer': 3, 'data_scientist': 2, 'software_engineer': 0, 'cybersecurity': 0}}
        ]
    },
    {
        'id': 10,
        'text': 'What is your greatest strength?',
        'options': [
            {'text': 'Logical thinking and problem-solving', 'scores': {'software_engineer': 5, 'data_scientist': 4, 'cybersecurity': 4, 'ux_designer': 1, 'marketing': 0}},
            {'text': 'Attention to detail and accuracy', 'scores': {'cybersecurity': 5, 'data_scientist': 4, 'software_engineer': 4, 'ux_designer': 2, 'marketing': 1}},
            {'text': 'Creativity and visual thinking', 'scores': {'ux_designer': 5, 'marketing': 4, 'software_engineer': 1, 'data_scientist': 0, 'cybersecurity': 0}},
            {'text': 'Communication and persuasion', 'scores': {'marketing': 5, 'ux_designer': 3, 'data_scientist': 2, 'software_engineer': 1, 'cybersecurity': 1}},
            {'text': 'Adaptability and quick learning', 'scores': {'software_engineer': 3, 'data_scientist': 3, 'cybersecurity': 3, 'marketing': 3, 'ux_designer': 3}}
        ]
    }
]

def analyze_career_scores(answers):
    """Calculate career scores based on quiz answers (simulated AI)"""
    scores = {career_id: 0 for career_id in CAREERS.keys()}
    
    # Aggregate scores from each answer
    for i, answer_index in enumerate(answers):
        if 0 <= answer_index < len(QUESTIONS[i]['options']):
            option_scores = QUESTIONS[i]['options'][answer_index]['scores']
            for career_id, points in option_scores.items():
                scores[career_id] += points
    
    # Sort careers by score
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Get top 2-3 careers with their scores
    recommendations = []
    for career_id, score in sorted_careers[:3]:
        if score > 0:
            recommendations.append({
                'id': career_id,
                'name': CAREERS[career_id]['name'],
                'description': CAREERS[career_id]['description'],
                'icon': CAREERS[career_id]['icon'],
                'color': CAREERS[career_id]['color'],
                'score': score,
                'reason': generate_reason(career_id, answers)
            })
    
    return recommendations

def generate_reason(career_id, answers):
    """Generate personalized reason for career recommendation"""
    reasons = {
        'software_engineer': [
            "Your strong logical thinking and problem-solving skills are perfect for software development.",
            "You enjoy building functional applications and working with technology.",
            "Your approach to learning shows you'd thrive in programming environments."
        ],
        'data_scientist': [
            "Your analytical mindset and interest in patterns make data science a natural fit.",
            "You enjoy finding insights from complex information.",
            "Your comfort with numbers and statistics aligns perfectly with data science."
        ],
        'ux_designer': [
            "Your creativity and attention to user experience will shine in UX/UI design.",
            "You have a natural eye for visual harmony and user-centered solutions.",
            "Your collaborative and creative approach matches design team dynamics."
        ],
        'cybersecurity': [
            "Your detail-oriented and security-conscious mindset is ideal for cybersecurity.",
            "You enjoy protecting systems and solving security puzzles.",
            "Your methodical approach to threats makes you a great security analyst."
        ],
        'marketing': [
            "Your communication skills and strategic thinking are perfect for digital marketing.",
            "You enjoy influencing others and creating impactful campaigns.",
            "Your creativity combined with analytical ability suits modern marketing."
        ],
        'ai_engineer': [
            "Your passion for data and advanced algorithms makes AI engineering a perfect fit.",
            "You enjoy building intelligent systems that can learn and adapt.",
            "Your strong logical and mathematical foundation is ideal for machine learning."
        ],
        'product_manager': [
            "Your ability to lead teams and define a clear vision is perfect for product management.",
            "You balance technical understanding with a focus on user value and business goals.",
            "You excel at strategic thinking and project coordination."
        ],
        'cloud_architect': [
            "Your interest in scalable infrastructure and systems design makes cloud architecture ideal.",
            "You enjoy building the backbone of modern digital services.",
            "Your methodical approach to security and performance is perfect for cloud systems."
        ]
    }
    
    # Select reason based on highest scoring questions if possible
    base_reason = random.choice(reasons.get(career_id, ["Your profile matches this career path well."]))
    return base_reason

# Learning Roadmaps for each career
ROADMAPS = {
    'software_engineer': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn Python or JavaScript fundamentals',
                'Understand basic data structures and algorithms',
                'Master Git version control',
                'Build 3-5 small projects (calculator, to-do list, etc.)',
                'Learn HTML, CSS, and basic frontend development'
            ],
            'tools': ['Python', 'VS Code', 'Git', 'GitHub', 'Basic Terminal']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Learn a web framework (Django/Flask or React)',
                'Understand databases (SQL, PostgreSQL)',
                'Build full-stack applications',
                'Learn API design and integration',
                'Practice code reviews and testing'
            ],
            'tools': ['Django/Flask', 'React', 'PostgreSQL', 'Postman', 'Docker Basics']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master system design and architecture',
                'Learn cloud services (AWS/Azure/GCP)',
                'Understand DevOps and CI/CD pipelines',
                'Contribute to open source projects',
                'Build a portfolio with complex applications'
            ],
            'tools': ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins']
        }
    },
    'data_scientist': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Master Python programming fundamentals',
                'Learn statistics and probability basics',
                'Study data manipulation with Pandas',
                'Learn data visualization with Matplotlib/Seaborn',
                'Practice with real datasets (Kaggle beginner)'
            ],
            'tools': ['Python', 'Jupyter', 'Pandas', 'NumPy', 'Matplotlib']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Learn machine learning fundamentals (Scikit-learn)',
                'Study SQL for data extraction',
                'Understand feature engineering techniques',
                'Build predictive models and evaluate them',
                'Learn basic deep learning concepts'
            ],
            'tools': ['Scikit-learn', 'SQL', 'TensorFlow/PyTorch', 'Tableau']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master deep learning and neural networks',
                'Learn big data technologies (Spark)',
                'Deploy models to production (MLOps)',
                'Specialize in NLP or Computer Vision',
                'Participate in Kaggle competitions'
            ],
            'tools': ['Spark', 'Docker', 'MLflow', 'Kubeflow', 'Cloud AI Services']
        }
    },
    'ux_designer': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn design fundamentals (color, typography, layout)',
                'Master Figma or Adobe XD basics',
                'Study user research methods',
                'Create paper prototypes and wireframes',
                'Build a portfolio with 3-5 design exercises'
            ],
            'tools': ['Figma', 'Adobe XD', 'Miro', 'Canva', 'Notion']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Learn interaction design and prototyping',
                'Study usability testing techniques',
                'Understand UI design patterns',
                'Learn basic HTML/CSS for implementation',
                'Create high-fidelity mockups for real products'
            ],
            'tools': ['Figma Advanced', 'Principle', 'Zeplin', 'InVision', 'Basic CSS']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master design systems and component libraries',
                'Learn advanced user research and analytics',
                'Build a comprehensive design portfolio',
                'Specialize in mobile or web UX',
                'Learn design thinking facilitation'
            ],
            'tools': ['Design System Tools', 'UX Research Tools', 'Hotjar', 'FullStory']
        }
    },
    'cybersecurity': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn networking fundamentals (TCP/IP, DNS, HTTP)',
                'Master Linux command line and basics',
                'Study cybersecurity fundamentals and threats',
                'Learn basic cryptography concepts',
                'Set up a home lab with virtual machines'
            ],
            'tools': ['Wireshark', 'VirtualBox', 'Linux', 'Nmap', 'Metasploit Basics']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Learn security frameworks (NIST, ISO 27001)',
                'Study penetration testing techniques',
                'Understand security monitoring and SIEM',
                'Learn Python for security automation',
                'Earn Security+ or CEH certification'
            ],
            'tools': ['Burp Suite', 'Splunk', 'Python', 'Kali Linux', 'Snort']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master advanced penetration testing',
                'Learn cloud security (AWS/Azure Security)',
                'Study incident response and forensics',
                'Earn advanced certifications (CISSP, OSCP)',
                'Specialize in security research or red teaming'
            ],
            'tools': ['Cloud Security Tools', 'Volatility', 'REMnux', 'Cobalt Strike']
        }
    },
    'marketing': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn digital marketing fundamentals (SEO, SEM, Social Media)',
                'Master Google Analytics and basic data analysis',
                'Study content marketing and copywriting basics',
                'Create social media campaigns for practice',
                'Learn email marketing tools'
            ],
            'tools': ['Google Analytics', 'Mailchimp', 'Hootsuite', 'Canva', 'WordPress']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Learn advanced SEO and paid advertising',
                'Study marketing automation and CRM',
                'Master A/B testing and conversion optimization',
                'Learn basic HTML/CSS for landing pages',
                'Build a personal brand or blog portfolio'
            ],
            'tools': ['HubSpot', 'Google Ads', 'SEMrush', 'Marketo', 'Salesforce']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Learn data-driven marketing and analytics',
                'Master omnichannel marketing strategies',
                'Study growth hacking techniques',
                'Earn certifications (Google Analytics, HubSpot)',
                'Lead marketing campaigns with measurable ROI'
            ],
            'tools': ['Tableau', 'Marketo Advanced', 'Optimizely', 'Salesforce Marketing Cloud']
        }
    },
    'ai_engineer': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Master Python for Data Science',
                'Learn Linear Algebra and Calculus',
                'Study Statistics and Probability',
                'Learn Data Manipulation with Pandas',
                'Build basic regression models'
            ],
            'tools': ['Python', 'NumPy', 'Pandas', 'Jupyter']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Master Scikit-Learn and ML algorithms',
                'Learn Deep Learning fundamentals',
                'Study Neural Networks and Backpropagation',
                'Work with Image and Text data',
                'Implement models from research papers'
            ],
            'tools': ['Scikit-Learn', 'TensorFlow', 'PyTorch', 'Keras']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master Large Language Models (LLMs)',
                'Learn MLOps and Model Deployment',
                'Study Reinforcement Learning',
                'Specialize in Computer Vision or NLP',
                'Build scalable AI applications'
            ],
            'tools': ['Hugging Face', 'MLflow', 'Docker', 'Kubernetes']
        }
    },
    'product_manager': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn Product Lifecycle basics',
                'Study Market Research techniques',
                'Understand User Persona development',
                'Learn basic Agile/Scrum methodologies',
                'Build a product teardown portfolio'
            ],
            'tools': ['Jira', 'Trello', 'Miro', 'Notion']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Master Product Strategy and Roadmap planning',
                'Learn Data Analytics for PMs',
                'Study UX Design principles',
                'Learn stakeholder management',
                'Manage a small feature from start to finish'
            ],
            'tools': ['Amplitude', 'Mixpanel', 'Figma', 'Confluence']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master Growth Product Management',
                'Learn advanced Business Strategy',
                'Study Product-Led Growth (PLG)',
                'Lead major product launches',
                'Mentor junior PMs and designers'
            ],
            'tools': ['Salesforce', 'Looker', 'Advanced Analytics']
        }
    },
    'cloud_architect': {
        'beginner': {
            'title': 'Foundation Stage (3-6 months)',
            'steps': [
                'Learn Networking fundamentals',
                'Study Linux Systems Administration',
                'Learn Cloud fundamentals (AWS/Azure)',
                'Understand Virtualization and Containers',
                'Build basic static websites on Cloud'
            ],
            'tools': ['AWS Console', 'Linux', 'Docker', 'Terraform Basics']
        },
        'intermediate': {
            'title': 'Building Skills (6-12 months)',
            'steps': [
                'Master Infrastructure as Code (IaC)',
                'Learn Serverless Architecture',
                'Study Cloud Security best practices',
                'Learn CI/CD pipeline automation',
                'Build multi-tier cloud applications'
            ],
            'tools': ['Terraform', 'AWS Lambda', 'GitHub Actions', 'CloudFormation']
        },
        'advanced': {
            'title': 'Mastery Level (1-2 years)',
            'steps': [
                'Master Multi-Cloud strategies',
                'Learn Disaster Recovery planning',
                'Study Cloud Cost Optimization',
                'Design high-availability systems',
                'Earn professional cloud certifications'
            ],
            'tools': ['Kubernetes', 'Ansible', 'Jenkins', 'Advanced Cloud Services']
        }
    }
}

# ==================================================
# FLASK ROUTES
# ==================================================

@app.route('/')
def home():
    """Home page with hero section and tips"""
    tips = [
        "🎯 Start building your portfolio from day one – real projects matter more than grades!",
        "💡 Soft skills like communication and teamwork are just as important as technical skills.",
        "🚀 The best time to start learning is now – Consistency beats intensity.",
        "🔗 Network with professionals on LinkedIn – many opportunities come from connections.",
        "📚 Never stop learning – Technology and industries evolve constantly."
    ]
    random_tip = random.choice(tips)
    return render_template('index.html', tip=random_tip)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """Interactive career quiz page"""
    print(f"Quiz route accessed: {request.method}")
    if request.method == 'POST':
        # Collect answers from form
        answers = []
        for i in range(len(QUESTIONS)):
            answer_key = f'q{i}'
            if answer_key in request.form:
                answers.append(int(request.form[answer_key]))
            else:
                # If missing answer, redirect back to quiz
                return render_template('quiz.html', questions=QUESTIONS, error="Please answer all questions")
        
        # Analyze career recommendations
        recommendations = analyze_career_scores(answers)
        
        # Store in session for results page
        session['recommendations'] = recommendations
        session['quiz_completed'] = True
        
        return redirect(url_for('results'))
    
    return render_template('quiz.html', questions=QUESTIONS)

@app.route('/results')
def results():
    """Display career recommendations based on quiz results"""
    if not session.get('quiz_completed'):
        return redirect(url_for('quiz'))
    
    recommendations = session.get('recommendations', [])
    if not recommendations:
        return redirect(url_for('quiz'))
    
    return render_template('results.html', recommendations=recommendations)

@app.route('/roadmap')
def roadmap():
    """Display learning roadmap for selected career"""
    career_id = request.args.get('career')
    
    # Validate career ID
    if not career_id or career_id not in ROADMAPS:
        # Try to get from session if available
        recommendations = session.get('recommendations', [])
        if recommendations:
            career_id = recommendations[0]['id']
        else:
            # Instead of 404, show a selection page
            return render_template('roadmap.html', 
                                 careers=CAREERS,
                                 roadmap=None)
    
    roadmap_data = ROADMAPS.get(career_id)
    career_name = CAREERS.get(career_id, {}).get('name', 'Career')
    
    return render_template('roadmap.html', 
                         roadmap=roadmap_data, 
                         career_name=career_name,
                         career_id=career_id,
                         careers=CAREERS)

@app.route('/cv', methods=['GET', 'POST'])
def cv_generator():
    """AI CV Generator - Create professional CV from user input"""
    cv_data = None
    
    if request.method == 'POST':
        # Collect CV data from form
        cv_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'location': request.form.get('location', ''),
            'summary': request.form.get('summary', ''),
            'skills': request.form.get('skills', '').split(','),
            'education': request.form.get('education', ''),
            'experience': request.form.get('experience', ''),
            'projects': request.form.get('projects', ''),
            'certifications': request.form.get('certifications', ''),
            'languages': request.form.get('languages', '')
        }
        
        # Clean skills list
        cv_data['skills'] = [skill.strip() for skill in cv_data['skills'] if skill.strip()]
        
        # Store in session for download
        session['generated_cv'] = cv_data
    
    return render_template('cv.html', cv_data=cv_data)

# ==================================================
# MAIN APPLICATION ENTRY POINT
# ==================================================

if __name__ == '__main__':
    print("Starting Career Compass AI Server...")
    # Using debug=True but disabling reloader to prevent connection resets in sandbox
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)