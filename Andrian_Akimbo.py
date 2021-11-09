# NEXAFS Adrian


from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import fftpack
from colorama import Fore
import time

########################ANLEITUNG######################
# Datenordner und Dunkelbildpfad angeben. Daten müssen tifs sein. Oben muss das Referenzspektrum sein und unten das Probenspektrum.
# Das Referenzspektrum muss die (in photonenrichtung) linke ORZ sein. Mehr ist eigendlich erstmal nicht zu beachten. Ist es anders herum muss die NEXAFS definition geändert werden.
# Falls eine Wellenlängenachse herrauskommt und keine Energieachse, muss das obere Spektrum geflipt werden und nicht das untere.


start = time.time()

DataDirectory = 'Z:/eigene_dateien/data/XAFS/mg/mg_foil/20180822'  # Datenordner
BGFile = 'Z:/eigene_dateien/data/XAFS/mg/mg_foil/20180822/bg/rzp_20180810_bg0000.tif'  # Dunkelbild

I_thresh_min = 0  # Unterer Schwellwert zum Aussortieren von "schlechten" Bildern"
I_thresh_max = 100
bgKor = 0  # offset des Untergrundbildes

bg = Image.open(BGFile)  # Listen und Arrays und so
bg = np.array(bg)
bg = bg.astype(float)
bg = bg - bgKor
NEXAFSlist = np.array(0)
NEXAFSsum = np.array(0)
j = 0
l = 0


def compareSpectra3(spekOben, spekUnten):  # Übereinanderschieben der Spektren (funktioniert nicht gut)
    A = fftpack.fft(spekOben)
    B = fftpack.fft(spekUnten)
    Br = -B.conjugate()
    shift = len(spekOben) - np.argmax(np.abs(fftpack.ifft(A * Br)))
    return shift, A


def roll(spekUnten, shift):
    spekUntenshift = np.roll(spekUnten, shift)
    return spekUntenshift


def nexafs(probe, ref):  # Bildung des NEXAFS
    nexafs_list = []
    for i in range(0, len(probe)):
        nexafs = -np.log(probe[i] / ref[i])
        nexafs_list.append(nexafs)
    return nexafs_list


DataList = []
# Hier werden Tifs geladen

for File in os.listdir(DataDirectory):
    if File[-3:] == 'TIF':
        DataList.append(File)

print(DataDirectory)

print(DataList)

for i in range(len(DataList)):

    FullDataDirectory = DataDirectory + '/' + DataList[i]  # Laden der Datein
    rb = Image.open(FullDataDirectory)
    rb = np.array(rb)
    rb = rb.astype(float)
    rb = rb - bg  # Abzug des Untergrundbildes
    rb_weg = np.mean(rb)

    if np.mean(rb_weg) > I_thresh_min and np.mean(rb_weg) < I_thresh_max:

        shape = rb.shape
        # print ("shape", shape)                                                          #Aufteilung in Probe (rechte ORZ) und Referenz (linke ORZ)
        halflenght = int(shape[0] / 2)
        print(halflenght)
        rbOben = rb[0:halflenght]
        rbUnten = rb[halflenght:]
        rbUnten = np.fliplr(
            rbUnten)  # Spiegelung des Unteren Spektrums (rechte ORZ) damit beide Energieachse von links nach rechts haben.

        spekOben = []
        spekUnten = []

        spekOben = np.sum(rbOben, axis=0)  # NORMALES Aufsummieren (funktiniert gut)
        spekUnten = np.sum(rbUnten, axis=0)

        shift = compareSpectra3(spekOben[:], spekUnten[:])
        shift = compareSpectra3(spekOben[:], spekUnten[:])
        print('Spektrum:', i + 1, 'Verschiebung:', (shape[1] - shift[0]), 'gem. Int:', round(np.mean(rb_weg), 0))
        spekUntenshift = roll(spekUnten, 18)  # Verschiebung des Unteren Spektrums Manuell (funktioniert gut)
        # spekUntenshift = roll(spekUnten, -shift[0])                                                     #Verschiebung durch Faltung (funktioniert Mittel)

        NEXAFS = nexafs(spekUntenshift, spekOben)
        NEXAFSlist = np.array(NEXAFSlist) + np.array(NEXAFS)

        NEXAFSsum = np.array(NEXAFSsum) + np.array(NEXAFS)
        j = j + 1
        plt.figure(0)
        plt.plot(spekOben)
        plt.plot(spekUntenshift)
        plt.figure(2)
        plt.plot(NEXAFS)



    else:

        l = l + 1
        print(Fore.RED)
        print('Aussortiert:', i + 1, 'gem. Int:', round(np.mean(rb_weg), 0), 'Schwelle =', I_thresh_min, I_thresh_max)
        print(Fore.BLACK)

NEXAFS_mean = NEXAFSsum / j
plt.figure(6)
# plt.xlim(1200,1800)
# plt.ylim(-0.5 ,0.5)
plt.plot(NEXAFS_mean, c='blue')

print('##########################################################')
print('##########################################################')
print('#########################Ergebnis#########################')
print('##########################################################')
print('##########################################################')
print('##########################################################')

print('Spektren:', j, 'Rausgeworfene Spektren', l)

end = time.time()
print('Rechenzeit in s:', end - start)











