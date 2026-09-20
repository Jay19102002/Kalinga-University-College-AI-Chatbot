import os
import json
import zipfile
import xml.etree.ElementTree as ET

SOURCE_DOCX = os.path.join("data", "raw", "Kalinga_University_Admission_Fees_Courses_Internships_Placements_Analysis_2026-27.docx")
KB_DIR = os.path.join("data", "knowledge_base")
REGISTRY_FILE = os.path.join("data", "source_registry.json")

def parse_docx(file_path):
    """Extract raw text paragraphs and tables from docx XML."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")
    
    with zipfile.ZipFile(file_path) as z:
        xml_content = z.read('word/document.xml')
    
    tree = ET.fromstring(xml_content)
    # Extract text content
    paragraphs = []
    for elem in tree.iter():
        if elem.tag.endswith('p'):
            p_text = ''.join(elem.itertext()).strip()
            if p_text:
                paragraphs.append(p_text)
    return paragraphs

def create_source_registry():
    sources = [
        {
            "id": "official_homepage",
            "title": "Kalinga University Homepage",
            "url": "https://kalingauniversity.ac.in/",
            "type": "official",
            "description": "University overview, statistics, claims, and main portals."
        },
        {
            "id": "admissions_page",
            "title": "Kalinga University Admissions Portal",
            "url": "https://kalingauniversity.ac.in/admissions?studyLevel=UG",
            "type": "official",
            "description": "UG/PG admissions guidelines, application portals, and study levels."
        },
        {
            "id": "admission_procedure",
            "title": "Kalinga University Admission Procedure",
            "url": "https://kalingauniversity.ac.in/admission-procedure",
            "type": "official",
            "description": "Step-by-step admission procedure and required documents."
        },
        {
            "id": "kalsee_page",
            "title": "Kalinga University KALSEE Entrance Examination",
            "url": "https://kalingauniversity.ac.in/kalsee",
            "type": "official",
            "description": "KALSEE exam details, format, duration, and fee structure."
        },
        {
            "id": "fees_page",
            "title": "Kalinga University Fee Structure (2026-27)",
            "url": "https://kalingauniversity.ac.in/ku-fees",
            "type": "official",
            "description": "Official fee structure for 2026-27 academic session."
        },
        {
            "id": "departments_page",
            "title": "Kalinga University Academic Departments & Faculties",
            "url": "https://kalingauniversity.ac.in/departments",
            "type": "official",
            "description": "Faculties, departments, and course inventory overview."
        },
        {
            "id": "placements_page",
            "title": "Kalinga University Training & Placements",
            "url": "https://kalingauniversity.ac.in/training-and-placements",
            "type": "official",
            "description": "Placement records, recruiter partners, CRT details, and student success highlights."
        },
        {
            "id": "campus_page",
            "title": "Kalinga University Campus Life & Facilities",
            "url": "https://kalingauniversity.ac.in/campuslife",
            "type": "official",
            "description": "Student life, internship details, CoE labs, and campus amenities."
        }
    ]
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2)
    print(f"Created {REGISTRY_FILE}")

def create_knowledge_base():
    os.makedirs(KB_DIR, exist_ok=True)
    
    # 1. University Overview
    university_data = {
        "name": "Kalinga University",
        "location": "Kotni, Near Mantralaya, Naya Raipur, Chhattisgarh, India",
        "contact": {
            "phone": "+91-9907252100",
            "email": "registrar@kalingauniversity.ac.in",
            "website": "https://kalingauniversity.ac.in/"
        },
        "reported_claims": {
            "programs_offered": "130+ undergraduate, postgraduate and doctoral programs",
            "international_students": "650+ from 33+ countries",
            "recruitment_partners": "400+",
            "research_publications": "7,200+",
            "patents": "562+",
            "mous": "200+",
            "laboratories": "100+ laboratories; 7 Centres of Excellence"
        },
        "source": {
            "title": "Kalinga University Homepage",
            "url": "https://kalingauniversity.ac.in/"
        }
    }
    with open(os.path.join(KB_DIR, "university.json"), "w", encoding="utf-8") as f:
        json.dump(university_data, f, indent=2)

    # 2. Admissions Data
    admissions_data = {
        "current_academic_year": "2026-27",
        "status": "Admission Open 2026–27",
        "status_disclaimer": "Admission dates can change by program and phase. Please verify the current admission status on Kalinga University's official admission page.",
        "steps": [
            "Step 1: Visit the official admissions portal (https://kalingauniversity.ac.in/admissions).",
            "Step 2: Register for the relevant entrance examination (KALSEE for general UG/PG or KAL-MAT for BBA/MBA).",
            "Step 3: Take the computer-based entrance exam and get shortlisted.",
            "Step 4: Complete the online admission form after selection.",
            "Step 5: Attach self-attested academic documents (mark sheets, TC/CC/Migration, Gap certificate if applicable).",
            "Step 6: Pay the applicable program fee within 10 days of receiving the offer letter."
        ],
        "required_documents": [
            "10th & 12th Mark sheets and passing certificates",
            "Graduation mark sheets & degree certificate (for PG programs)",
            "Original Transfer Certificate (TC) / College Leaving Certificate (CLC)",
            "Character Certificate (CC) & Migration Certificate",
            "Gap Certificate / Undertaking (if applicable)",
            "Proof of Employment / Self-Employment (for working professional applicants)",
            "Passport-size photographs & ID Proof (Aadhaar / Passport)"
        ],
        "entrance_exams": [
            {
                "name": "KALSEE (Kalinga Scholastic Entrance Examination)",
                "applies_to": "All UG/PG programs except BBA and MBA",
                "format": "Multiple Choice Questions (MCQ); Computer-based test",
                "duration": "90 minutes for UG/PG (120 minutes for Ph.D.)",
                "total_questions": "90 questions for UG/PG (100 for Ph.D.)",
                "negative_marking": "No negative marking",
                "qualifying_score": "Minimum 50%",
                "exam_fee": "₹1,400 for UG/PG (India/SAARC candidates)",
                "source": "https://kalingauniversity.ac.in/kalsee"
            },
            {
                "name": "KAL-MAT (Kalinga Management Aptitude Test)",
                "applies_to": "BBA and MBA programs",
                "format": "Management aptitude test",
                "source": "https://kalingauniversity.ac.in/admission-procedure"
            }
        ],
        "sources": [
            {
                "title": "Kalinga University Admission Procedure",
                "url": "https://kalingauniversity.ac.in/admission-procedure"
            },
            {
                "title": "Kalinga University KALSEE",
                "url": "https://kalingauniversity.ac.in/kalsee"
            }
        ]
    }
    with open(os.path.join(KB_DIR, "admissions.json"), "w", encoding="utf-8") as f:
        json.dump(admissions_data, f, indent=2)

    # 3. Courses Data
    courses_data = {
        "total_programs_advertised": "130+",
        "disclaimer": "The chatbot knowledge base contains selected programs from the available source material. For the complete current list, please check the official departments/programs page.",
        "faculties": [
            {
                "faculty": "Arts & Humanities",
                "programs": ["BA in Liberal Arts with PSC Coaching", "BA (PSC Coaching)", "MA", "MSW with PSC Coaching", "BSW with PSC Coaching", "MA (Journalism & Mass Communication) with PSC Coaching", "BA (Journalism & Mass Communication) with PSC Coaching", "MA Film Making"]
            },
            {
                "faculty": "Commerce & Management",
                "programs": ["BBA", "B.Com", "B.Com (Honours)", "M.Com", "MBA"]
            },
            {
                "faculty": "Education",
                "programs": ["B.Ed", "B.P.Ed", "M.Ed"]
            },
            {
                "faculty": "Hotel Management",
                "programs": ["B.Sc Hotel Management", "Diploma in Hotel Management", "Hospitality & Tourism Management"]
            },
            {
                "faculty": "Information Technology",
                "programs": ["BCA", "BCA in Artificial Intelligence & Machine Learning", "BCA in Game Development with AI", "MCA"]
            },
            {
                "faculty": "Law",
                "programs": ["Bachelor of Law (LLB)", "Integrated BBA + LLB", "Integrated BA + LLB", "Master of Laws (LLM)"]
            },
            {
                "faculty": "Pharmacy",
                "programs": ["Bachelor of Pharmacy (B.Pharm)", "Diploma in Pharmacy (D.Pharm)", "Doctor of Pharmacy (Pharm.D)"]
            },
            {
                "faculty": "Science",
                "programs": ["B.Sc / M.Sc in Biochemistry", "Bioinformatics", "Biotechnology", "Forensic Science", "Microbiology", "PCM", "Zoology-Botany-Chemistry"]
            },
            {
                "faculty": "Technology / Engineering",
                "programs": ["B.Tech in Computer Science Engineering (CSE)", "B.Tech in CSE (AI & ML)", "B.Tech in Civil Engineering", "B.Tech in Electrical Engineering", "B.Tech in Mechanical Engineering", "Diploma in Engineering"]
            },
            {
                "faculty": "Ph.D. Doctoral Studies",
                "programs": ["Ph.D. in Management", "Ph.D. in Computer Science", "Ph.D. in Law", "Ph.D. in Pharmacy", "Ph.D. in Science", "Ph.D. in Humanities"]
            }
        ],
        "source": {
            "title": "Kalinga University Departments",
            "url": "https://kalingauniversity.ac.in/departments"
        }
    }
    with open(os.path.join(KB_DIR, "courses.json"), "w", encoding="utf-8") as f:
        json.dump(courses_data, f, indent=2)

    # 4. Fees Data
    fees_data = {
        "academic_year": "2026-27",
        "note": "The live official fee page labels the fee structure as 2026–27. Below are exact visible figures for Arts & Humanities programs. Other faculty tables load dynamically on the official site.",
        "fee_records": [
            {
                "program": "BA in Liberal Arts with PSC Coaching",
                "faculty": "Arts & Humanities",
                "duration": "3 years / 6 sem",
                "tuition_fee_per_sem": "₹50,000",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000; Uniform ₹4,950",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹3,18,350",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "MA",
                "faculty": "Arts & Humanities",
                "duration": "2 years / 4 sem",
                "tuition_fee_per_sem": "₹17,500",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹80,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "BA (PSC Coaching)",
                "faculty": "Arts & Humanities",
                "duration": "3 years / 6 sem",
                "tuition_fee_per_sem": "₹25,000",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000; Uniform ₹4,950",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹1,68,350",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "MSW",
                "faculty": "Arts & Humanities",
                "duration": "2 years / 4 sem",
                "tuition_fee_per_sem": "₹17,500",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹80,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "BSW with PSC Coaching",
                "faculty": "Arts & Humanities",
                "duration": "3 years / 6 sem",
                "tuition_fee_per_sem": "₹20,000",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹1,33,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "MA (J & MC) with PSC Coaching",
                "faculty": "Arts & Humanities",
                "duration": "2 years / 4 sem",
                "tuition_fee_per_sem": "₹27,500",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹1,20,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "BA (J & MC) with PSC Coaching",
                "faculty": "Arts & Humanities",
                "duration": "3 years / 6 sem",
                "tuition_fee_per_sem": "₹27,500",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000; Uniform ₹4,950",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹1,78,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            },
            {
                "program": "MA Film Making",
                "faculty": "Arts & Humanities",
                "duration": "2 years / 4 sem",
                "tuition_fee_per_sem": "₹40,000",
                "one_time_fees": "Prospectus/KALSEE ₹1,400; Caution Money ₹3,000",
                "exam_fee_per_sem": "₹1,500",
                "published_total": "₹1,70,400",
                "academic_year": "2026-27",
                "source": "https://kalingauniversity.ac.in/ku-fees"
            }
        ],
        "unsupported_fee_fallback": "I don't have a reliable fee value for that program in my current knowledge base. Please check Kalinga University's official fee page at https://kalingauniversity.ac.in/ku-fees.",
        "source": {
            "title": "Kalinga University Official Fee Page",
            "url": "https://kalingauniversity.ac.in/ku-fees"
        }
    }
    with open(os.path.join(KB_DIR, "fees.json"), "w", encoding="utf-8") as f:
        json.dump(fees_data, f, indent=2)

    # 5. Scholarships Data
    scholarships_data = {
        "max_advertised_scholarship": "Up to 100%",
        "qualification_note": "Kalinga University advertises scholarships of up to 100%, subject to applicable eligibility criteria and university policy.",
        "total_distributed_claim": "More than ₹3 crore distributed in scholarships (university-reported claim).",
        "categories": [
            {"category": "Merit Scholarship", "details": "Awarded based on academic excellence in qualifying examinations."},
            {"category": "Entrance Test Scholarship", "details": "Awarded based on performance in KALSEE, KAL-MAT, or national entrance exams."},
            {"category": "Sports Scholarship", "details": "For state, national, and international level sports achievements."},
            {"category": "Cultural Scholarship", "details": "For outstanding performance in recognized cultural and extra-curricular events."},
            {"category": "Sibling Scholarship", "details": "Fee concession for siblings studying concurrently at Kalinga University."},
            {"category": "Social Category Scholarship", "details": "Concessions under social category welfare schemes as per university norms."},
            {"category": "Social Media / Knowledge Dissemination", "details": "Concessions for student ambassadors and academic contributors."},
            {"category": "Innovation & Research Scholarship", "details": "For candidates with published patents, research work, or innovative startup projects."}
        ],
        "source": {
            "title": "Kalinga University Scholarships",
            "url": "https://kalingauniversity.ac.in/"
        }
    }
    with open(os.path.join(KB_DIR, "scholarships.json"), "w", encoding="utf-8") as f:
        json.dump(scholarships_data, f, indent=2)

    # 6. Internships Data
    internships_data = {
        "overview": "Kalinga University promotes both on-campus and off-campus internship programs to give students practical industry exposure prior to graduation.",
        "six_month_co_e_initiative": "A 6-month industry-exposure initiative in emerging technologies including AI, Machine Learning, Robotics, Drones, and Python through Centre of Excellence collaboration.",
        "activities": ["Industrial visits", "Workshops", "Masterclasses", "Guest lectures", "Hackathons", "Ideathons", "Value-added certification courses"],
        "disclaimer": "These are published examples of student internships. They do not constitute a guarantee that every student receives an internship at those exact organizations.",
        "examples": [
            {"student": "Aditi Singh", "program": "BBA", "company": "Aditya Birla Fashion Retail Ltd."},
            {"student": "Maryam Nasiru", "program": "B.Pharm", "company": "Artemis Hospital, Gurugram"},
            {"student": "Nayna Chakhiyar", "program": "B.Com B&F", "company": "Tata Steel Ltd."},
            {"student": "Trupti Ranjan Sahu", "program": "MBA", "company": "Aditya Birla Group"}
        ],
        "source": {
            "title": "Kalinga University Campus Life & Internships",
            "url": "https://kalingauniversity.ac.in/campuslife"
        }
    }
    with open(os.path.join(KB_DIR, "internships.json"), "w", encoding="utf-8") as f:
        json.dump(internships_data, f, indent=2)

    # 7. Placements Data
    placements_data = {
        "recruitment_partners_claim": "400+",
        "crt_details": "Campus Recruitment Training (CRT) is a 100-hour program covering attitude, quantitative aptitude, reasoning, mock interviews, role plays, case studies, practice tests, and individual feedback.",
        "published_individual_examples": [
            {"program": "LLM", "student": "Ankita Shrivastava", "company": "Cornerstone", "package": "₹33 LPA"},
            {"program": "B.Tech", "student": "Shubham Sharma", "company": "Oracle", "package": "₹29.98 LPA"},
            {"program": "MCA", "student": "Bidyasagar Pradhan", "company": "Ascendion", "package": "₹17.50 LPA"},
            {"program": "B.Sc Fashion Designing", "student": "Khushi Rai", "company": "Air India", "package": "₹12 LPA"}
        ],
        "package_qualification": "Kalinga University's published examples include an LLM placement at Cornerstone with a reported ₹33 LPA CTC and B.Tech at Oracle with ₹29.98 LPA. These are individual published placement examples and should not be interpreted as a guaranteed package or average salary for all students.",
        "historical_brochure_data": {
            "status": "historical",
            "year": "Older brochure archive",
            "recruiters": 121,
            "students_placed": "1,100+",
            "placement_rate": "73.82%",
            "highest_domestic_ctc": "₹10 LPA",
            "average_ctc": "₹2.30 LPA",
            "note": "These historical brochure statistics belong to a past academic period and must not be confused with current 2026-27 statistics."
        },
        "recruiters": [
            "Infosys", "Capgemini", "Airtel", "Amul", "Cipla", "Wipro", "Adani", "Bosch", 
            "Biocon", "Apollo", "Axis Bank", "Cognizant", "Suzuki", "Himalaya", "Decathlon", 
            "Godrej", "Genpact", "HDFC Bank", "Jio", "Justdial", "LG", "Nestle", "SAIL", 
            "Tata Motors", "Tech Mahindra", "UltraTech", "Cisco", "IBM"
        ],
        "recruiter_qualification": "Companies appearing in the university's published recruiter information represent organizations that have participated in recruitment drives; recruiting participation may vary by year and program.",
        "source": {
            "title": "Kalinga University Training & Placements",
            "url": "https://kalingauniversity.ac.in/training-and-placements"
        }
    }
    with open(os.path.join(KB_DIR, "placements.json"), "w", encoding="utf-8") as f:
        json.dump(placements_data, f, indent=2)

    # 8. Campus Data
    campus_data = {
        "laboratories": "100+ state-of-the-art laboratories",
        "centres_of_excellence": "7 Centres of Excellence in AI, ML, Robotics, Drones, IoT, and Cyber Security",
        "facilities": [
            "Central Library with digital access & research databases",
            "On-campus separate Hostels for Boys & Girls with mess & security",
            "Sports Complex (Cricket ground, Football, Basketball, Badminton, Gym)",
            "Auditorium & Seminar Halls",
            "Moot Court for Law students",
            "Language Laboratory & Soft Skills Centre",
            "Medical Centre & 24/7 Ambulance facility",
            "Transport facility across Raipur and nearby regions",
            "Wi-Fi enabled smart campus"
        ],
        "source": {
            "title": "Kalinga University Campus Life",
            "url": "https://kalingauniversity.ac.in/campuslife"
        }
    }
    with open(os.path.join(KB_DIR, "campus.json"), "w", encoding="utf-8") as f:
        json.dump(campus_data, f, indent=2)

    print("Created structured JSON knowledge base files in data/knowledge_base/")

if __name__ == "__main__":
    create_source_registry()
    create_knowledge_base()
