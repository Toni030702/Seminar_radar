import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import serial
import keyboard

ser = serial.Serial('COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)

matplotlib.use('TkAgg')

fig = plt.figure(facecolor='k')
fig.canvas.toolbar.pack_forget()  # brisanje toolbara
fig.canvas.manager.set_window_title('Radar')  # naslov

mgn = plt.get_current_fig_manager()  # dobavljanje managera/upravitelja
mgn.window.state('zoomed')  # fullscreen

ax = fig.add_subplot(1, 1, 1, polar=True, facecolor='#32a852')  # 1 red, 1 stupac, polarni k.s.
ax.tick_params(axis='both', color='w')   # bojanje k.s. u bijelo
r_max = 100
ax.set_ylim([0.0, r_max])  # ogranici od 0-r_max
ax.set_xlim([0.0, np.pi])  # ogranici x osi 0-pi radijana
ax.set_position([-0.05, -0.05, 1, 1.2])  # za subplot [left, bottom, width, height]
ax.set_rticks(np.linspace(0.0, r_max, 5))  # oznake na r osi 0-r_max s korakom 5
ax.set_thetagrids(np.linspace(0.0, 180, 10))  # oznake na kutnoj osi 0-180, 10 dijelova

angles = np.arange(0, 181, 1)  # kutovi
theta = angles * (np.pi/180)   # pretvorba kutova u radijane

pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='r', markeredgecolor='w', markeredgewidth=1.0,
                markersize=3.0, alpha=0.5)

line1, = ax.plot([], [], color='w', linewidth=3.0)  # prazna linija za prikazivanje podataka

fig.canvas.draw()  # crta inicijalni prikaz slike
dists = np.ones((len(angles),))
axbackground = fig.canvas.copy_from_bbox(ax.bbox)  # pozadinska kopija subplot ax za brzo azuriranje grafa

while True:
    try:
        data = ser.readline().decode().strip()  # Čitanje i dekodiranje podataka, uklanjanje početnih/završnih razmaka
        if not data:
            continue  # Preskoči prazne podatke

        vals = [float(ii.rstrip('.')) for ii in data.split(',') if ii.strip() and '.' in ii and ii != '.']
        if len(vals) < 2:
            continue  # Preskoči ako nema dovoljno vrijednosti

        pos, udaljenost = vals
        dists[int(pos)] = udaljenost

        pols.set_data(theta, dists)    # postavljanje podataka u polarne koordinate na grafu
        fig.canvas.restore_region(axbackground)    # Obnavljanje pozadine grafa
        ax.draw_artist(pols)    # crtanje podataka o udaljenosti

        line1.set_data(np.repeat((pos * (np.pi/180)), 2), np.linspace(0.0, r_max, 2))
        ax.draw_artist(line1)     # Crtanje linije
        fig.canvas.blit(ax.bbox)   # Brzo azuriranje dijela grafa
        fig.canvas.flush_events()   # Azuriranje prikaza

        if keyboard.is_pressed('esc'):
            plt.close('all')
            print("Korisnik zeli zatvoriti aplikaciju")
            break

    except KeyboardInterrupt:      # Ručno prekidanje CTRL+C
        plt.close('all')
        print('Prekid s tipkovnice')
        break
exit()
