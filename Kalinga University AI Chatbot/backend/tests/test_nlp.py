from app.services.chatbot import chatbot_service

def test_admission_intents():
    ans, intent, conf, _, _ = chatbot_service.process_query("How can I apply for admission?")
    assert intent == "admission_process"
    assert conf > 0.30

def test_kalsee_intent():
    ans, intent, conf, _, _ = chatbot_service.process_query("What is KALSEE exam?")
    assert intent == "kalsee"
    assert conf > 0.30

def test_fee_intent():
    ans, intent, conf, entities, _ = chatbot_service.process_query("What is the fee for BBA?")
    assert intent in ["course_fee", "fees"]
    assert entities.get("program") == "BBA"

def test_scholarship_intent():
    ans, intent, conf, _, _ = chatbot_service.process_query("Does the university provide scholarships?")
    assert intent in ["scholarship", "merit_scholarship"]

def test_placement_intent():
    ans, intent, conf, _, _ = chatbot_service.process_query("Which companies recruit from Kalinga?")
    assert intent in ["placement_companies", "placement", "recruiter_list"]

def test_highest_package_intent():
    ans, intent, conf, _, _ = chatbot_service.process_query("What is the highest package?")
    assert intent == "highest_package"
