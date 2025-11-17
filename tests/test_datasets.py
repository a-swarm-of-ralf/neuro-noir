def test_the_adventure_of_retired_colorman():
    from neuro_noir.datasets import the_adventure_of_retired_colorman
    doc = the_adventure_of_retired_colorman()
    assert doc.title == "The Adventure of the Retired Colorman"
    assert "Sherlock Holmes was in a melancholy and philosophic mood that morning." in doc.content

def test_the_adventure_of_the_three_students():
    from neuro_noir.datasets import the_adventure_of_the_three_students
    doc = the_adventure_of_the_three_students()
    assert doc.title == "The Adventure of the Three Students"
    assert "It was in the year ’95 that a combination of events" in doc.content

def test_the_five_orange_pips():
    from neuro_noir.datasets import the_five_orange_pips
    doc = the_five_orange_pips()
    assert doc.title == "The Five Orange Pips"
    assert "When I glance over my notes and records of the Sherlock Holmes cases" in doc.content

def test_the_mysterious_affair_at_styles():
    from neuro_noir.datasets import the_mysterious_affair_at_styles
    doc = the_mysterious_affair_at_styles()
    assert doc.title == "The Mysterious Affair at Styles"
    assert "The intense interest aroused in the public by what was known at the" in doc.content

def test_the_adventure_of_retired_colorman_annotations():
    from neuro_noir.datasets import the_adventure_of_retired_colorman
    doc = the_adventure_of_retired_colorman()
    annotation = doc.annotations[3]
    assert annotation["paragraph"] == "\"You mean the old fellow who has just gone out?\""
    assert "Speaker: Dr. John Watson." in annotation["annotation"]

def test_list_datasets():
    from neuro_noir.datasets import list_datasets
    datasets = list_datasets()
    expected_datasets = [
        "the-adventure-of-the-retired-colourman",
        "the-adventure-of-the-three-students",
        "the-five-orange-pips",
        "the-mysterious-affair-at-styles",
    ]
    for dataset in expected_datasets:
        assert dataset in datasets

def test_load_dataset():
    from neuro_noir.datasets import load_dataset
    doc = load_dataset("the-adventure-of-the-retired-colourman")
    assert doc.title == "The Adventure Of The Retired Colourman"
    assert "Sherlock Holmes was in a melancholy and philosophic mood that morning." in doc.content
    annotation = doc.annotations[3]
    assert annotation["paragraph"] == "\"You mean the old fellow who has just gone out?\""
    assert "Speaker: Dr. John Watson." in annotation["annotation"]
    