from app.services.chatbot import chatbot_service

def test_multi_turn_fee_context():
    session_id = "test_context_session"
    
    # Query 1: BBA Fee
    ans1, intent1, conf1, ent1, _ = chatbot_service.process_query("What is the fee for BBA?", session_id)
    assert ent1.get("program") == "BBA"
    
    # Query 2: Follow-up "What about MBA?"
    ans2, intent2, conf2, ent2, _ = chatbot_service.process_query("What about MBA?", session_id)
    assert ent2.get("program") == "MBA"
    assert intent2 in ["course_fee", "fees", "mba_courses"]
