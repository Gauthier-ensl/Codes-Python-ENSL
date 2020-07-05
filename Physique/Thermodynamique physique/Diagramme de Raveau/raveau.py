# This import registers the 3D projection, but is otherwise unused.

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.colors import LogNorm
matplotlib.rc('xtick', labelsize=24)
matplotlib.rc('ytick', labelsize=24)
matplotlib.rcParams.update({'font.size': 22})

#  cree une figure et une tableau d'abscisses
### Initialisation des grandeurs
#positions sur l'ecran d'observation
qf = np.linspace(-1,1,10) # [J] chaleur recue par le systeme venant de la source froide

#parametres initiaux
Tc = 500 #temperature source chaude
Tf = 300 #temperature source froide
qc0 = 0.8


Sc = 0.1/Tc #entropie creee (irreversibilite)



def qc_s(qf, Tc, Tf, Sc):
    return(-Tc*qf/Tf - Tc*Sc)

def qc_u(qf, Tc, Tf, Sc, qc0):
    qf0 = -Tf*qc0/Tc - Tf*Sc
    W = - qc0 - qf0
    return(-qf - W)

def work(qf, Tc, Tf, Sc, qc0):
    qf0 = -Tf*qc0/Tc - Tf*Sc
    W = - qc0 - qf0
    return(-W)


### Affichage initial
fig = plt.figure()
ax = fig.add_subplot(111)
f, = plt.plot(qf, qc_u(qf, Tc, Tf, Sc, qc0), lw=4, label='$Q_c = - Q_f - W$')
g, = plt.plot(qf, qc_s(qf, Tc, Tf, Sc), lw=4, label='$Q_c = - \dfrac{T_c}{T_f}Q_f- T_c S_\mathrm{créée}$')
h, = plt.plot(qf,qc0*np.ones(len(qf)), lw=4)
i, = plt.plot(0,work(qf, Tc, Tf, Sc, qc0),  'or', markersize=15, label='$-W$')
plt.subplots_adjust(left=0.15, bottom=0.25)
plt.xticks([])
plt.yticks([])
plt.ylim([-1.8,1.8])
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
plt.text(0,2,'$Q_c$', fontsize = 28)
plt.text(0.01, 0.92 ,'$Q_c^{ref}$', fontsize = 28)
plt.text(1.15,0,'$Q_f$', fontsize = 28)
plt.legend(frameon=False)
plt.show()

### Slider

# cree les glissieres pour ajuster a et b
axcolor = 'lightgoldenrodyellow'
axTc  = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axTf = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
axSc = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)

sTc = Slider(axTc, '$T_c$ [K]', 100, 600, valinit=Tc)
sTf = Slider(axTf, '$T_f$ [K]', 100, 600, valinit=Tf)
sSc = Slider(axSc, '$S_c$ [$\mathrm{mJ \cdot K^{-1}}$] ', 0, 1, valinit=Sc*1e3)
plt.subplots_adjust()

def update(val):
    Tc1 = sTc.val
    Tf1 = sTf.val
    Sc1 = sSc.val*1e-3
    f.set_ydata(qc_u(qf, Tc1, Tf1, Sc1, qc0))
    g.set_ydata(qc_s(qf, Tc1, Tf1, Sc1))
    h.set_ydata(qc0*np.ones(len(qf)))
    i.set_ydata(work(qf, Tc1, Tf1, Sc1, qc0))
    fig.canvas.draw_idle()

# rendre les glissieres actives :
sTc.on_changed(update)
sTf.on_changed(update)
sSc.on_changed(update)

#  creer un bouton reset , pour les glissieres :
resetax = plt.axes([0.05, 0.07, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    sTc.reset()
    sTf.reset()
    sSc.reset()
button.on_clicked(reset)


# afficher le graphe :

mng = plt.get_current_fig_manager()     #Plein ecran
mng.window.showMaximized()
plt.show()