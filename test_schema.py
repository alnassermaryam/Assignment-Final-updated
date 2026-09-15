from ai_engineering.schemas import AssistantOutput
def test_contract():
    x=AssistantOutput(language="en",intent="general",answer="ok")
    assert x.safe is True
