def test_the_adventure_of_retired_colorman():
    from neuro_noir.datasets import the_adventure_of_retired_colorman
    data = the_adventure_of_retired_colorman()
    assert "Sherlock Holmes was in a melancholy and philosophic mood that morning." in data

def test_the_adventure_of_the_three_students():
    from neuro_noir.datasets import the_adventure_of_the_three_students
    data = the_adventure_of_the_three_students()
    assert "It was in the year ’95 that a combination of events" in data

def test_the_five_orange_pips():
    from neuro_noir.datasets import the_five_orange_pips
    data = the_five_orange_pips()
    assert "When I glance over my notes and records of the Sherlock Holmes cases" in data