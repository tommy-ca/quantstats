import os

def test_requirements_contains_hvplot():
    req_file = "requirements.txt"
    with open(req_file, "r") as f:
        requirements = f.read()
    
    assert "hvplot" in requirements, "hvplot should be in requirements.txt"

def test_requirements_contains_bs4():
    req_file = "requirements.txt"
    with open(req_file, "r") as f:
        requirements = f.read()
    
    assert "beautifulsoup4" in requirements, "beautifulsoup4 should be in requirements.txt"
