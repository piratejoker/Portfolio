#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from collections import defaultdict

import class_sound as cs


class Library:
    """
    The song library, used for both identifying and normal library 
    functions.

    Attributes
    ----------
    sounds : dict
        dictionary of sounds, keyed by some metadata (?what works best?)
    to_search : dict
        dictionary of sounds, keyed by fingerprint
    """

    def __init__(self, files=[]):
        """Construct a sound library.

        Parameters
        ----------
        files : list
            filepaths to song files, to add when creating the library
        """
        self.sounds = defaultdict(int)
        self.sig_lib = defaultdict(bool)
        for file in files:
            self.add(file)

    def convert(self, sound_name, file_type):
        """Converts the file at sound.wavpath to a specific file type.

      Parameters
        ----------
        sound_name : a string
            a song title
        file_type : a string
            the file type to convert to

        Returns
        -------
        file
            file_type of sound_name
        """
        return self

    def add(self, connection, meta=[]):
        """
        Does all analysis functions.
        Generate an object of class sound.
        Checks that it is not in the database, which is like a dict.
        Hashes are hashes of the signatures.

        Parameters
        ----------
        connection : ?a string?
            a file path or connection

        Returns
        -------
        Sound
            a object of class Sound
        """
        assert self.search(connection) is False, "Song already in Library"
        new_sound = cs.Sound(connection, meta)
        self.sounds[new_sound.key] = new_sound.filename
        self.sig_lib.update(new_sound.sig_dict)
        return self

    def remove(self, connection):
        """
        Removes a sound from the library.
        """
        sound = cs.Sound(connection)
        for sig in list(sound.sig_dict.keys()):
            self.sig_lib.pop(sig, None)
        self.sounds.pop(sound.key, None)
        return self

    def list_lib(self):
        """
        Lists the sounds in the library. The titles from self.sounds.

        Returns
        -------
        list
            The titles of all songs in the library. ?maybe more metadata?
        """
        for sound in list(self.sounds.values()):
            if sound != 0:
                print(sound)

    def search(self, connection):
        """
        Searches the library for a sound based on meta.

        Parameters
        ----------
        meta : ?a list of strings?
            non-sound related metadata (song title, albumn, artist), etc.

        Returns
        -------
        bool
            whether the song is in the library.
        """
        sound = cs.Sound(connection)
        if self.sounds[sound.key] != 0:
            return True
        else:
            return False

    def identify(self, connection):
        """
        Searches the library for a sound based on a snippet with 
        signatures.

        Matches window  of in-library sounds using self.to_search.

        Parameters
        ----------
        sound : object of Sound class.
            the snippet to identify in the library.

        Returns
        -------
        str
            the title of the song, ?maybe  more metadata?
        """
        sound = cs.Sound(connection)
        sigs = list(sound.sig_dict.keys())
        found_dict = defaultdict(int) # all start at zero
        for sig in sigs:
            found = self.sig_lib[sig]
            if found is not False: # in case found is 0
                found_dict[found] += 1
        vals = list(found_dict.values())
        best_match_ind = np.argmax(vals)
        best_match = list(found_dict.keys())[best_match_ind]
        print(self.sounds[best_match])
        return self.sounds[best_match]

    def show_spectrogram(self, connection):
        """Displays an image of the spectrogram of a given sound from path."""
        sound = cs.Sound(connection)
        sound.plot_spectrogram()
        
    def slow_search(self, snip):
        """Searches the library for a sound based on a snippet with full data.

        Parameters
        ----------
        sound : object of Sound class.
            the snippet to identify in the library.

        Returns
        -------
        str
            the title of the song.
        """
        snip_spec = snip.spectrogram[2]
        min_dist_metric = None
        for key in list(self.sounds.keys):
            sound = self.sounds[key]
            for local_periodogram in sound.spectrogram[2]:
                dist_metric = sum(snip_spec) - sum(local_periodogram)
            if min_dist_metric == None or dist_metric < min_dist_metric:
                min_dist_metric = dist_metric
                best_match = key
        return self.sounds[best_match].datapath
