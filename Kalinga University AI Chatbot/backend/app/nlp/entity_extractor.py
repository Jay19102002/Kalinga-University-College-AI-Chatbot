import re
from typing import Dict, Any

PROGRAM_MAP = {
    "bba": "BBA",
    "mba": "MBA",
    "btech": "B.Tech",
    "b.tech": "B.Tech",
    "bca": "BCA",
    "mca": "MCA",
    "llb": "LLB",
    "llm": "LLM",
    "bpharm": "B.Pharm",
    "dpharm": "D.Pharm",
    "pharmd": "Pharm.D",
    "bcom": "B.Com",
    "mcom": "M.Com",
    "bed": "B.Ed",
    "med": "M.Ed",
    "ba": "BA",
    "ma": "MA",
    "msw": "MSW",
    "bsw": "BSW",
    "bsc": "B.Sc",
    "msc": "M.Sc",
    "phd": "Ph.D."
}

EXAM_MAP = {
    "kalsee": "KALSEE",
    "kalmat": "KAL-MAT",
    "kal-mat": "KAL-MAT"
}

def extract_entities(text: str) -> Dict[str, Any]:
    """Extract recognized domain entities from text."""
    entities = {}
    lower_text = text.lower()
    
    # 1. Program / Course Entity
    found_programs = []
    for key, val in PROGRAM_MAP.items():
        if re.search(r'\b' + re.escape(key) + r'\b', lower_text):
            found_programs.append(val)
    if found_programs:
        entities["program"] = found_programs[0]
        entities["all_programs"] = list(set(found_programs))
        
    # 2. Entrance Exam Entity
    for key, val in EXAM_MAP.items():
        if key in lower_text:
            entities["entrance_exam"] = val
            break
            
    # 3. Academic Year Entity
    year_match = re.search(r'202\d[-–]?2\d', lower_text)
    if year_match:
        entities["academic_year"] = year_match.group(0)
    else:
        entities["academic_year"] = "2026-27"
        
    # 4. Fee query entity
    if any(term in lower_text for term in ["fee", "cost", "charge", "tuition", "price", "amount", "structure"]):
        entities["fee_query"] = True
        
    # 5. Placement query entity
    if any(term in lower_text for term in ["placement", "package", "salary", "recruiter", "ctc", "company", "hired"]):
        entities["placement_query"] = True
        
    return entities
