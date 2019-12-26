## Run the tests by running
## pytest -v test_shazam.py
## All test functions must start with test_.

import pytest

import class_library as cl


def test_add():
    """Adding a song adds it to the search scope at the very least"""
    test_library = cl.Library()

    test_library.add("Data/Songs/bass-mono.wav")
    assert test_library.search("Data/Songs/bass-mono.wav") is not False


def test_remove():
    """Removing a file should remove it from the library"""
    test_library = cl.Library()

    test_library.add("Data/Songs/bass-mono.wav")
    test_library.remove("Data/Songs/bass-mono.wav")
    assert test_library.search("Data/Songs/bass-mono.wav") is False


def test_duplicates():
    """Adding two of the same file should result in only one entry"""
    test_library = cl.Library()
    test_library.add("Data/Songs/bass-mono.wav")
    with pytest.raises(AssertionError):
        test_library.add("Data/Songs/bass-mono.wav")
    # What constitutes a duplicate? Same file? Same data? Same name? Same meta?


def test_identify():
    """Generate sinusoids and add to library, then try to identify snips"""
    test_library = cl.Library()
    test_library.add("Data/Songs/bass-mono.wav")
    found = test_library.identify("Data/Songs/bass-snippet.wav") 
    assert found == "bass-mono.wav"

