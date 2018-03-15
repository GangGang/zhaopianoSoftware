class MidiAnalyzer(object):

    def __init__(self, midi_file):
        self.midi_file = midi_file
        self.midi_track = self._GetLongestTrack(self.midi_file)
        self.resolution = self.midi_file.resolution
        self.get_tempo()
        self.state = [-1] * 256
        self.time = 0
        self.n_event = 0
        self.clearMidiEvents()
        self.all_frames = []
        self.fps = 30

    def clearMidiEvents(self):  # save useful events only
        targets = ['NoteOnEvent', 'NoteOffEvent','ControlChangeEvent', 'EndOfTrackEvent']
        i = 0
        while (i < len(self.midi_track)):
            if self.midi_track[i].__class__.__name__ not in targets:
                del self.midi_track[i]
            else:
                i += 1

    def _GetLongestTrack(self, midi_file):
        longestTrack = midi_file[0]
        for track in midi_file:
            if len(longestTrack) < len(track):
                longestTrack = track
        return longestTrack
    def get_tempo(self):
        for event in self.midi_track:
            if event.__class__.__name__ == 'SetTempoEvent':
                self.tempo = round(event.bpm)
        print('tempo:',self.tempo)
    def EndOfSong(self):
        return self.n_event >= len(self.midi_track)

    def Advance(self, delta):
        """Advances waterfall by delta ticks.
        Returns False iff EOF reached.
        """
        while not self.EndOfSong():
            event = self.midi_track[self.n_event]
            if event.tick >= delta:
                event.tick -= delta
                self.time += delta
                break  # 不论程序怎么运行，最后都会从这里退出。
            self.time += event.tick
            delta -= event.tick
            self.n_event += 1
            if event.statusmsg == 0x80:
                self.state[event.pitch] = -1
            elif event.statusmsg == 0x90:
                self.state[event.pitch] = self.time
            elif event.statusmsg == 0xb0:
                if event.value == 127:
                    self.state[109] = 1
                elif event.value == 0:
                    self.state[109] = -1


    def WaterfallNoteColor(self, note):
        if note in self.active_notes:
            if self.state[note] >= 0:
                return '#00ff00'
        if note % 12 in (0, 2, 4, 5, 7, 9, 11):
            return '#8080ff'  # white note
        else:
            return '#80ffff'  # black note

    def run(self):
        while not self.EndOfSong():
            self.all_frames.append(self.state[21:110])  # 88 piano keys + 1 pedal status
            tps = self.resolution * self.tempo/60
            delta = tps / self.fps  # ticks between two frames
            self.Advance(delta)  # update state( if possible)
        return self.all_frames
