from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import serial
import keyboard

ser = serial.Serial('COM4', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)

fig = plt.figure(facecolor='k')
fig.canvas.toolbar.pack_forget()
fig.canvas.manager.set_window_title('Ultrasonic Radar Plot')
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

ax = fig.add_subplot(1, 1, 1, polar=True, facecolor='#006b70')
ax.tick_params(axis='both', colors='w')
r_max = 100.0
ax.set_ylim([0.0, r_max])
ax.set_xlim([0.0, np.pi])
ax.set_position([-0.05, -0.05, 1, 1.2])
ax.set_rticks(np.linspace(0.0, r_max, 5))
ax.set_thetagrids(np.linspace(0, 180, 10))
ax.grid(color='w', alpha=0.4)

angles = np.arange(0, 181, 1)
theta = angles * (np.pi / 180.0)

pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='r', markeredgecolor='w', markeredgewidth=1.0, markersize=3.0, alpha=0.9)
line1, = ax.plot([], color='w', linewidth=4.0)

fig.canvas.draw()
dists = np.ones((len(angles),))
fig.show()
fig.canvas.blit(ax.bbox)
fig.canvas.flush_events()
axbackground = fig.canvas.copy_from_bbox(ax.bbox)

while True:
    try:
        data = ser.readline().decode().strip()
        print("Primljeni podaci:", data)
        if not data:
            print("Prazni podaci, preskačem...")
            continue

        vals = data.split(",")
        if len(vals) < 2:
            print("Nedovoljno vrijednosti, preskačem:", vals)
            continue

        pos, udaljenost = map(float, vals)
        print("Primljeno: pozicija =", pos, ", udaljenost =", udaljenost)
        dists[int(pos)] = udaljenost

        pols.set_data(theta, dists)
        fig.canvas.restore_region(axbackground)
        ax.draw_artist(pols)

        line1.set_data(np.repeat((pos * (np.pi/180)), 2), np.linspace(0.0, r_max, 2))
        ax.draw_artist(line1)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()

        plt.pause(0.01)

        if keyboard.is_pressed('esc'):
            plt.close('all')
            print("Korisnik želi zatvoriti aplikaciju")
            break

    except KeyboardInterrupt:
        plt.close('all')
        print('Prekid s tipkovnice')
        break
