class wydarzenie_add:
    def __init__(self, nazwa, data, h_start, data_koniec, h_stop, lokalizacja=None, opis=None):
        if lokalizacja is None and opis is None:
            self.nazwa = nazwa
            self.data = data
            self.h_start = h_start
            self.h_stop = h_stop
            self.data_koniec = data_koniec
            self.event = {'summary': self.nazwa,
                          'start': {'dateTime': '{}T{}+01:00'.format(self.data, self.h_start)},
                          'end': {'dateTime': '{}T{}+01:00'.format(self.data_koniec, self.h_stop)}}
        if lokalizacja is None:
            self.nazwa = nazwa
            self.data = data
            self.h_start = h_start
            self.h_stop = h_stop
            self.opis = opis
            self.data_koniec = data_koniec
            self.event = {'summary': self.nazwa, 'description': self.opis,
                          'start': {'dateTime': '{}T{}+01:00'.format(self.data, self.h_start)},
                          'end': {'dateTime': '{}T{}+01:00'.format(self.data_koniec, self.h_stop)}}
        if opis is None:
            self.nazwa = nazwa
            self.data = data
            self.h_start = h_start
            self.h_stop = h_stop
            self.lokalizacja = lokalizacja
            self.data_koniec = data_koniec
            self.event = {'summary': self.nazwa, 'location': self.lokalizacja,
                          'start': {'dateTime': '{}T{}+01:00'.format(self.data, self.h_start)},
                          'end': {'dateTime': '{}T{}+01:00'.format(self.data_koniec, self.h_stop)}}
        else:
            self.nazwa = nazwa
            self.data = data
            self.h_start = h_start
            self.h_stop = h_stop
            self.lokalizacja = lokalizacja
            self.opis = opis
            self.data_koniec = data_koniec
            self.event = {'summary': self.nazwa, 'location': self.lokalizacja, 'description': self.opis,
                          'start': {'dateTime': '{}T{}+01:00'.format(self.data, self.h_start)},
                          'end': {'dateTime': '{}T{}+01:00'.format(self.data_koniec, self.h_stop)}}
class wydarzenie_del:
    def __init__(self, nazwa, data=None, h_start=None):
        if data is None and h_start is None:
            self.nazwa = nazwa
        else:
            self.nazwa = nazwa
            self.data = data
            self.h_start = h_start