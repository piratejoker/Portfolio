
import re
import wave
import urllib
import audio_metadata as am
import os
from scipy.io import wavfile

import analysis_functions as af
import matplotlib.pyplot as plt

class Sound:
    """A sound, used for storing attributes related to a particular song

    Attributes
    ----------
    connection : str
        the link or path containing the file
    key : int
        unique identifier, just a hash of the connection for now
    source : str
        the url source if file is remote
    samprate : int
        the sampling rate of the song
    starttime : float
        the starting time of a song, in seconds
    length : float
        the length of the song, in seconds
    """

    def __init__(self, connection, meta=[], snip=False):
        """Construct a sound

        Parameters
        ----------
        file : class ReadData
            the read file with pertinant metadata
        """
        # random unique key
        self.connection = connection
        self.read_data()

        self.key = hash(self.bytes)

        self.assign_spectrogram()
        self.assign_signatures()

####### Reading File

    def read_data(self):
        """Considers the file types and then passes to appropriate function"""
        self.type = ""
        self.tempdatapath = ""
        if re.search("http.*://", self.connection) is None:
            self.type = "local"
            self.read_local()
        else:
            self.type = "remote"
            self.read_remote()
        return self


    def read_local(self):
        """Reads a local file"""
        name = re.search("(?!.*/).*", self.connection).group()
        wav = wave.open(self.connection)
        self.bytes = open(self.connection, "rb").read()
        self.filename = name
        self.framerate, self.data = wavfile.read(self.connection)
        self.assign_params(wav)
        self.metadata = am.load(self.connection)
        return self


    def read_remote(self):
        """Reads a file over a connection."""
        self.url = self.connection
        wav_bytes = urllib.request.urlopen(self.connection).read()
        self.bytes = wav_bytes

        temp_wav = open("temp.wav", "wb")
        temp_wav.write(wav_bytes)
        temp_wav.close()
        wav = wave.open("temp.wav")
        self.assign_params(wav)
        self.metadata = am.load("temp.wav")
        self.framerate, self.data = wavfile.read("temp.wav")
        os.remove("temp.wav")

        name = re.search("(?!.*/).*", self.connection).group()
        self.filename = name
        return self


    def assign_params(self, wav):
        self.params = wav.getparams()
        self.nchannels = wav.getnchannels()
        self.sampwidth = wav.getsampwidth()
        self.framerate = wav.getframerate()
        self.nframes = wav.getnframes()
        wav.close()
        return self

####### File Operations

    def convert(self, file_type):
        """Converts the file to a specific file type

        Parameters
        ----------
        file_type : a string
            the file type to convert to
        """
        return self

    def assign_spectrogram(self):
        """Assigns periodograms. May extend to let user select window function

        Parameters
        ----------
        file : class ReadData
            the read file with pertinant metadata
        """
        self.spectrogram = af.calculate_spectrogram(self)
        return self

    def plot_spectrogram(self):
        f, t, Sxx = self.spectrogram
        plt.pcolormesh(t, f, Sxx)

    def assign_signatures(self):
        """Assigns signatures"""
        self.signatures, self.sig_dict = af.calculate_signatures(self.spectrogram,
                                                                 self.key)
        return self
