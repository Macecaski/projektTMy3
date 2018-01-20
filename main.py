import pyaudio
import wave
from techmo_trybun_pyclient import TTS_pb2
from techmo_trybun_pyclient.wave_saver import WaveSaver
from GoogleAPICalendar import add, edit_jedno,edit_konkret, del1, del2, del3, check, get_credentials, sprawdzam, sprawdzam2
from playsound import playsound
from techmo_sarmata_pyclient.utils.wave_loader import load_wave
from techmo_sarmata_pyclient.service.sarmata_settings import SarmataSettings
from techmo_sarmata_pyclient.service.sarmata_recognize import SarmataRecognizer
from techmo_sarmata_pyclient.service.asr_service_pb2 import ResponseStatus
from techmo_dictation_pathfinder_pyclients.audio_provider import get_audio
from techmo_dictation_pathfinder_pyclients.dictation_client import DictationClient
from address_provider import AddressProvider
from Klasy import wydarzenie_add, wydarzenie_del
import grpc
import os
import time
import shutil
import sys


#program -> użytkownik - głosowo

def mow(tekst):
    def text2speech(tekst):
        if __name__ == '__main__':
            # Config:
            output_wave_file = 'tts_output.wav'
            ap = AddressProvider()
            address = ap.get("trybun")
            sampling_rate = 44100
            input_text = tekst

            # Establish GRPC channel
            channel = grpc.insecure_channel(address)
            stub = TTS_pb2.TTSStub(channel)

            # Synthesis request
            config = TTS_pb2.SynthesizeConfig(sample_rate_hertz=44100)
            request = TTS_pb2.SynthesizeRequest(text=input_text, config=config)
            ws = WaveSaver()
            for response in stub.Synthesize(request):
                if response.HasField('error'):
                    print("Error [" + str(response.error.code) + "]: " + response.error.description)
                    break
                else:
                    if ws._samplerate:
                        if ws._samplerate != response.audio.sample_rate_hertz:
                            raise RuntimeError("Sample rate does not match previously received")
                    else:
                        ws.setFrameRate(response.audio.sample_rate_hertz)
                    ws.append(response.audio.content)
                    if response.audio.end_of_stream:
                        ws.save(output_wave_file)
            ws.clear()

    def odtwarzanie(name):
        CHUNK = 1024

        wf = wave.open(name, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()
    text2speech(tekst)
    #playsound('tts_output.wav')
    odtwarzanie('tts_output.wav')
    time.sleep(0.1)

#główne funkcje
def autoryzacja():
    if os.path.exists(".credentials/user_data.json") == True:
        mow("Wygląda na to że już korzystałeś z systemu")
        mow("Czy chcesz korzystać z poprzednich ustawień konta ? ")
        odp=sarmata("noyes")
        if odp == "nie":
            shutil.rmtree(".credentials")
            mow("Zaloguj się na swoje konto gu gl ")
            odp_serwera = get_credentials()
        else:
            pass
    else:
        mow("Zaloguj się na swoje konto gu gl ")
        odp_serwera = get_credentials()



#główne funkcje
def dodaj():
    licznik= 0
    while licznik < 8:
        if licznik == 0:
            mow("Podaj nazwe wydarzenia")
            print("Podaj nazwe wydarzenia")
            nazwa = dictation()
            if nazwa == 'wróć' or nazwa == 'cofnij' or nazwa == 'anuluj':
                return 0

            else:
                nazwa = nazwa
                licznik = 1

        if licznik == 1:
            mow("Podaj date")
            print("Podaj date")
            data = sarmata("daty")
            print(data)
            if data == '7777-77-77':
                licznik = 0
            elif data == '9999-99-99':
                return 0
            else:
                data = data
                licznik = 2

        if licznik == 2:
            mow("Podaj godzine rozpoczÍcia")
            print("Podaj godzine rozpoczÍcia")
            rozpoczecie = sarmata("godziny")
            print("rozpoczÍcie")
            if rozpoczecie == '90:90:00':
                licznik = 1
            elif rozpoczecie == '97:97:00':
                return 0
            else:
                if rozpoczecie == "70:70:00":
                    h_poczatek = "00:00:00"
                    h_koniec = "23:59:59"
                    data_koniec = data
                    licznik = 5
                else:
                    h_poczatek = rozpoczecie
                    licznik = 3

        if licznik == 3:
            mow("Podaj date zakończenia wydarzenia ")
            print("Podaj date zakończenia wydarzenia ")
            data_koniec = sarmata("daty")
            if data_koniec == '7777-77-77':
                licznik = 2
            elif data_koniec == '9999-99-99':
                return 0
            else:
                data_koniec = data_koniec
                licznik = 4

        if licznik == 4:
            mow("Podaj godzine zakoŮczenia wydarzenia")
            print("Podaj godzine zakoŮczenia wydarzenia: ")
            h_koniec = sarmata("godziny")
            if h_koniec == '90:90:00':
                licznik = 3
            elif h_koniec == '97:97:00':
                return 0
            else:
                h_koniec = h_koniec
                licznik = 5

        if licznik == 5:
            mow("Podaj lokalizacje")
            print("Podaj lokalizacje")
            lokalizacja = dictation()
            if lokalizacja == "wróć":
                licznik = 4
            elif lokalizacja == 'anuluj':
                return 0
            else:
                lokalizacja = lokalizacja
                licznik = 6

        if licznik == 6:
            mow("Podaj opis")
            print("Podaj opis")
            opis = dictation()
            if opis == 'wróć':
                licznik = 5
            elif nazwa == 'anuluj':
                return 0
            else:
                opis = opis
                licznik = 7

        if licznik == 7:
            dodawane = wydarzenie_add(nazwa, data, h_poczatek, data_koniec, h_koniec, lokalizacja, opis)
            add(dodawane.event)
            licznik = 8

    mow("Utworzono wydarzenie")
    mow(nazwa)

def usun():

    licznik = 0

    while licznik < 4:

        if licznik == 0:
            mow('Podaj nazwe wydarzenia')
            print('Podaj nazwe wydarzenia')
            nazwa = dictation()
            if nazwa == 'wróć' or nazwa == 'cofnij' or nazwa == 'anuluj':
                return 0
            elif nazwa == "":
                mow("Nie zrozumiałam, powtórz")
                licznik = 0
            else:
                nazwa2=nazwa
                print(nazwa2)
                do_usuniecia = wydarzenie_del(nazwa2)
                odp = del1(do_usuniecia)
                licznik = 1
                if odp == 2:
                    mow("Usunełam wydarzenie.")
                    mow(nazwa)
                    mow("Z twojego życia.")
                    return 0

                if odp == 1:
                    mow("Nie znaleziono wydarzenia!")
                    return 0

                mow("Więcej niż jedno wydarzenie o tej nazwie")
                print("Więcej niż jedno wydarzenie o tej nazwie")

                if licznik == 1:
                    mow("Czy usunąć wszystkie wydarzenia?")
                    print("Czy usunąć wszystkie wydarzenia?")
                    odp = sarmata("takinie")
                    if odp == "wróć":
                        usun()
                    if odp == "tak":

                        odp = del3(do_usuniecia)
                        print("Usunełam wszystkie wydarzenia o nazwie {}.".format(nazwa))
                        mow("Usunełam wszystkie wydarzenia.")
                        mow(nazwa)
                        mow("Z twojego życia.")

                    else:
                        licznik = 2
                        if licznik == 2:
                            mow("Sprecyzuj o któro wydarzenie ci chodzi ")
                            print("Sprecyzuj o któro wydarzenie ci chodzi ")
                            mow("Podaj datę")
                            print("Podaj datę ")
                            data = sarmata("daty")
                            if data == '7777-77-77':
                                licznik = 1
                            elif data == '9999-99-99':
                                return 0
                            else:
                                licznik = 3
                                mow("Podaj godzinę rozpoczęcia")
                                print("Podaj godzinę rozpoczęcia")
                                h_start = sarmata("godziny")
                                if h_start == "90:90:00":
                                    licznik = 2
                                elif h_start == "97:97:00":
                                    return 0
                                else:
                                    do_usuniecia = wydarzenie_del(nazwa, data, h_start)
                                    odp = del2(do_usuniecia)
                                    if odp == 2:
                                        mow("Usunełam wydarzenie ")
                                        print("Usunełam wydarzenie o nazwie: {} z dnia {}, z godziny {}".format(nazwa,
                                                                                                                data,
                                                                                                                h_start))
                                        mow(nazwa)
                                        mow("Z twojego życia.")

                                    if odp == 1:
                                        mow("Nie znaleziono wydarzenia!")


def sprawdz():
    mow('Podaj date')
    print("Podaj date")
    data = input()
    check(data)
def edytuj():

    def edytuje(tekst):

        odpowiedz = tekst.split()
        print(odpowiedz)

        def _godziny():

            def check_action():
                mow("Chcesz zmienić tylko godzinę rozpoczęcia, godzinę zakończenia czy obie?")
                odp = input()
                if odp == "rozpoczęcia":
                    return 0
                if odp == "zakończenia":
                    return 1
                if odp == "obie":
                    return 2
                if odp == "żadnej":
                    return 3

            odp = check_action()

            if odp == 0:
                mow("Podaj nową godzine rozpoczęcia")
                rozpoczecie = sarmata("godziny")
                zakonczenie = ""
            if odp == 1:
                rozpoczecie = ""
                mow("Podaj nową godzine zakończenia")
                zakonczenie = sarmata("godziny")
            if odp == 2:
                mow("Podaj nową godzine rozpoczęcia")
                rozpoczecie = sarmata("godziny")
                mow("Podaj nową godzine zakończenia")
                zakonczenie = sarmata("godziny")
            if odp == 3:
                rozpoczecie = ""
                zakonczenie = ""

            return rozpoczecie, zakonczenie

        def _daty():

            def check_action():
                mow("Chcesz zmienić tylko datę rozpoczęcia, datę zakończenia czy obie?")
                odp = dictation()
                if odp == "rozpoczęcia":
                    return 0
                if odp == "zakończenia":
                    return 1
                if odp == "obie":
                    return 2
                if odp == "żadnej":
                    return 3

            odp = check_action()

            if odp == 0:
                mow("Podaj nową datę rozpoczęcia")
                rozpoczecie = sarmata("daty")
                zakonczenie = ""
            if odp == 1:
                rozpoczecie = ""
                mow("Podaj nową datę zakończenia")
                zakonczenie = sarmata("daty")
            if odp == 2:
                mow("Podaj nową datę rozpoczęcia")
                rozpoczecie = sarmata("godziny")
                mow("Podaj nową datę zakończenia")
                zakonczenie = sarmata("godziny")
            if odp == 3:
                rozpoczecie = ""
                zakonczenie = ""

            return rozpoczecie, zakonczenie

        def _nazwa():

            mow("Podaj nową nazwę")
            nazwa = dictation()

            return nazwa

        def _lokalizacja():
            mow("Podaj nową lokalizacje")
            lokalizacja = dictation()

            return lokalizacja

        def _opis():
            mow("Podaj nowy opis")
            opis = dictation()

            return opis

        nowa_data_start = ""
        nowa_data_koniec = ""
        nowa_h_start = ""
        nowa_h_koniec = ""
        nowy_opis = ""
        nowa_lokalizacja = ""
        nowa_nazwa = ""

        for zmiana in odpowiedz:
            if zmiana == "godzina":
                nowa_h_start, nowa_h_koniec = _godziny()

            if zmiana == "data":
                nowa_data_start, nowa_data_koniec = _daty()

            if zmiana == "lokalizacja":
                nowa_lokalizacja = _lokalizacja()

            if zmiana == "opis":
                nowy_opis = _opis()

            if zmiana == "nazwa":
                nowa_nazwa = _nazwa()

        print(nowa_h_start)
        print(nowa_h_koniec)
        print(nowa_data_start)
        print(nowa_data_koniec)
        print(nowa_nazwa)
        print(nowa_data_start)
        return nowa_data_start, nowa_data_koniec, nowa_h_start, nowa_h_koniec, nowy_opis, nowa_lokalizacja, nowa_nazwa

    mow('Podaj nazwe wydarzenia')
    mow('Podaj nazwe wydarzenia')
    nazwa = dictation()

    odp=sprawdzam(nazwa)

    if odp == 0:
        mow("Nie znaleziono")

    if odp == 1:
        mow("znalazłam wydarzenie")
        mow('Powiedz co chciałbyś we mnie zmienić')
        zmiany = sarmata("edytuj")
        nowa_data_start, nowa_data_koniec, nowa_h_start, nowa_h_koniec, nowy_opis, nowa_lokalizacja, nowa_nazwa = edytuje(zmiany)

        edit_jedno(nazwa,nowa_nazwa,nowa_data_start,nowa_h_start,nowa_data_koniec,nowa_h_koniec,nowy_opis,nowa_lokalizacja)
    if odp == 2:
        mow("wiecej niż jedno wydarzenie o tej nazwie")
        mow("sprecyzuj")
        mow("Podaj datę")
        data = sarmata("daty")
        mow("Podaj godzinę rozpoczęcia")
        mow("Podaj godzinę rozpoczęcia")
        h_start = sarmata("godziny")
        odp=sprawdzam2(nazwa,data,h_start)
        if odp == 1:
            mow("znalazłam wydarzenie")
            mow('Powiedz co chciałbyś we mnie zmienić')
            zmiany = sarmata("edytuj")
            nowa_data_start, nowa_data_koniec, nowa_h_start, nowa_h_koniec, nowy_opis, nowa_lokalizacja, nowa_nazwa=edytuje(zmiany)
            edit_konkret(nazwa, data,h_start,nowa_nazwa,nowa_data_start,nowa_h_start,nowa_data_koniec,nowa_h_koniec,nowy_opis,nowa_lokalizacja)
            mow("edytowano")
        if odp == 0:
            mow("nie znaleziono")


#użytkownik -> program - głosowo
def nagrywanie():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return WAVE_OUTPUT_FILENAME
def sarmata(grammar):

    nagranie=nagrywanie()



    def formatowanie_daty(tekst):
        odpowiedz = tekst.split()
        print(odpowiedz)

        if tekst == 'wróć':
            data = '7777-77-77'
            return data
        elif tekst == 'anuluj':
            data = '9999-99-99'
            return data
        else:
            def find_month(tekst):
                miesiace = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia',
                            'września',
                            'października', 'listopada', 'grudnia']

                for miesiac in miesiace:
                    if miesiac in odpowiedz:
                        month = miesiac
                        index = odpowiedz.index(month)
                        index_month = miesiace.index(month)
                        print(index)
                        return index, miesiac, index_month

                return -1, "brak", -1

            miesiac_index, miesiac, index_month = find_month(odpowiedz)

            if miesiac_index == -1:
                print("Nie znaleziono miesiąca")

            else:
                # dodawanie dnia
                for i in range(0, miesiac_index):
                    if i == 0:
                        dzien = odpowiedz[i]

                    else:
                        dzien = dzien + odpowiedz[i]
                print(dzien)

                # dodawanie roku
                for i in range(miesiac_index + 1, len(odpowiedz)):
                    if i == miesiac_index + 1:
                        rok = odpowiedz[i]

                    else:
                        rok = rok + odpowiedz[i]
                print(rok)

            print(miesiac)

            if index_month == -1:
                print("Nic")

            if index_month < 10:
                miesiac = "0{}".format(index_month + 1)

            else:
                miesiac = "{}".format(index_month + 1)

            data = rok + "-" + miesiac + "-" + dzien

            print(data)
            return data

    def formatuj_godzine(tekst):
        odpowiedzi = tekst.split()
        print(odpowiedzi)


        if "cały" in odpowiedzi:
            minuty=str(70)
            godziny=str(70)

        elif "wróć" in odpowiedzi:
            minuty = str(90)
            godziny = str(90)
        elif "anuluj" in odpowiedzi:
            minuty = str(97)
            godziny = str(97)

        elif "za" in odpowiedzi:
            if len(odpowiedzi) == 5:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(60 - int(odpowiedzi[1]) - int(odpowiedzi[2]))
                godziny = str(int(odpowiedzi[3]) + int(odpowiedzi[4]))
            if len(odpowiedzi) == 4:
                if 'm' in odpowiedzi[2]:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(60 - int(odpowiedzi[1]) - int(odpowiedzi[2]))
                    godziny = str(int(odpowiedzi[3]))
                else:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(60 - int(odpowiedzi[1]))
                    godziny = str(int(odpowiedzi[2]) + int(odpowiedzi[3]))
            if len(odpowiedzi) == 3:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(60 - int(odpowiedzi[1]))
                godziny = str(int(odpowiedzi[2]))

        elif "po≥udniu" in odpowiedzi:
            if len(odpowiedzi) == 5:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(int(odpowiedzi[1]) + int(odpowiedzi[2]))
                godziny = str(int(odpowiedzi[0]))
            if len(odpowiedzi) == 4:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(int(odpowiedzi[1]))
                godziny = str(int(odpowiedzi[0]))
            if len(odpowiedzi) == 3:
                minuty = str('00')
                godziny = str(int(odpowiedzi[0]))

        elif "po" in odpowiedzi:
            if len(odpowiedzi) == 5:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(int(odpowiedzi[0]) + int(odpowiedzi[1]))
                godziny = str(int(odpowiedzi[3]) + int(odpowiedzi[4]))
            if len(odpowiedzi) == 4:
                if 'm' in odpowiedzi[1]:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(int(odpowiedzi[0]) + int(odpowiedzi[1]))
                    godziny = str(int(odpowiedzi[3]))
                else:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(int(odpowiedzi[0]))
                    godziny = str(int(odpowiedzi[2]) + int(odpowiedzi[3]))
            if len(odpowiedzi) == 3:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(int(odpowiedzi[0]))
                godziny = str(int(odpowiedzi[2]))

        elif "30m" in odpowiedzi[0]:
            if len(odpowiedzi) == 3:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str('30')
                godziny = str(int(odpowiedzi[1]) + int(odpowiedzi[2]))
            if len(odpowiedzi) == 2:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str('30')
                godziny = str(int(odpowiedzi[1]))

        else:
            if len(odpowiedzi) == 4:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str(int(odpowiedzi[2]) + int(odpowiedzi[3]))
                godziny = str(int(odpowiedzi[0]) + int(odpowiedzi[1]))
            if len(odpowiedzi) == 3:
                if 'm' in odpowiedzi[1]:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(int(odpowiedzi[1]) + int(odpowiedzi[2]))
                    godziny = str(int(odpowiedzi[0]))
                else:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(int(odpowiedzi[2]))
                    godziny = str(int(odpowiedzi[0]) + int(odpowiedzi[1]))
            if len(odpowiedzi) == 2:
                if 'm' in odpowiedzi[1]:
                    odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                    minuty = str(int(odpowiedzi[1]))
                    godziny = str(int(odpowiedzi[0]))
                else:
                    minuty = str('00')
                    godziny = str(int(odpowiedzi[0]) + int(odpowiedzi[1]))
            if len(odpowiedzi) == 1:
                odpowiedzi = [s.replace('m', '') for s in odpowiedzi]
                minuty = str('00')
                godziny = str(int(odpowiedzi[0]))

        if len(minuty) == 1:
            minuty = '0' + minuty

        if len(godziny) == 1:
            godziny = '0' + godziny

        format_godzina = godziny + ':' + minuty + ':00'

        return format_godzina

    def print_results(responses,grammar):
        if responses is None:
            print("Empty results - None object")
            return

        for response in responses:
            if response is None:
                print("Empty results - skipping response")
                continue

            print("Received response with status: {}".format(ResponseStatus.Name(response.status)))

            if response.error:
                print("[ERROR]: {}".format(response.error))

            for n, res in enumerate(response.results):
                transcript = " ".join([word.transcript for word in res.words])
                print("[{}.] {} /{}/ ({})".format(n, transcript, res.semantic_interpretation, res.confidence))

                if grammar == "daty" and res.semantic_interpretation!="":
                    odp = formatowanie_daty(res.semantic_interpretation)
                    return odp

                if grammar == "godziny" and res.semantic_interpretation!="":
                    odp = formatuj_godzine(res.semantic_interpretation)
                    return odp

                else:
                    return res.semantic_interpretation

    if __name__ == '__main__':
        ap = AddressProvider()
        wave_file = nagranie
        grammar_file = "grammars/{}.abnf".format(grammar)
        address = ap.get("sarmata")

        audio = load_wave(wave_file)

        settings = SarmataSettings()
        session_id = os.path.basename(wave_file)
        settings.set_session_id(session_id)
        settings.load_grammar(grammar_file)

        recognizer = SarmataRecognizer(address)
        results = recognizer.recognize(audio, settings)

        odp = print_results(results,grammar)




        return odp


def dictation():
    nagrywanie()
    if __name__ == '__main__':
        ap = AddressProvider()
        address = ap.get("dictation")
        dc = DictationClient(address)

        # Read wave file
        wave_filepath = "output.wav"
        audio = get_audio(wave_filepath)

        # Run Pathfinder
        try:
            results = dc.recognize(method="sync", audio=audio)
        except grpc.RpcError as e:
            print("[Server-side error] Received following RPC error from the Pathfinder service:", str(e))
            import sys
            sys.exit(1)

        for idx, response in enumerate(results):
            if not len(response):
                print("No phrases detected.")
                return ""
            else:
                print("Transcription:")
                print("\"{}\"".format(response['transcript']))
                if response['transcript']=='brak':
                    return ""
                else:
                    return response['transcript']



#main
def maly_main():
        mow('Co mogę dla ciebie zrobic?')
        odp = sarmata("main")

        if odp == 'dodaj':
            dodaj()
        if odp == 'usuń':
            usun()
        if odp == 'sprawdź':
            sprawdz()
        if odp == 'edytuj':
            edytuj()
        elif odp == 'zakończ':
            sys.exit()
        elif odp == '':
            mow('Nie zrozumiałam, powtórz polecenie')
            maly_main()
        else:
            maly_main()

def main():
    autoryzacja()
    mow('Witaj! Pozwól że pomogę Ci w organizacji twojego kalendarza')
    maly_main()


#main()

usun()



