from app.services.chatbot import chatbot_service

def test_unknown_out_of_scope_query():
    ans, intent, conf, _, _ = chatbot_service.process_query("What is the recipe for chocolate cake?")
    assert intent == "unknown"
    assert "not fully sure" in ans.lower() or "help with" in ans.lower()

def test_no_invented_fee():
    ans, intent, conf, _, _ = chatbot_service.process_query("What is the fee for Aeronautical Engineering?")
    # Must explicitly direct to official fee page rather than inventing a number
    assert "official fee page" in ans.lower() or "don't have a reliable fee" in ans.lower()

def test_placement_qualification():
    ans, intent, conf, _, _ = chatbot_service.process_query("What is the highest package?")
    assert "individual published" in ans.lower() or "not be interpreted as a guaranteed" in ans.lower()

def test_scholarship_qualification():
    ans, intent, conf, _, _ = chatbot_service.process_query("Tell me about scholarships")
    assert "up to 100%" in ans.lower() or "subject to" in ans.lower()
