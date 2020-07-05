import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider, Button
import matplotlib
from matplotlib import patches
matplotlib.rc('xtick', labelsize=24)
matplotlib.rc('ytick', labelsize=24)
matplotlib.rcParams.update({'font.size': 22})

#Ce script affiche la courbe de la loi d'emission du corps noir de Planck, avec un slider pour pouvoir changer la temperature. Il affiche egalement la couleur associée a l'émission, avec un algorithme basé sur des lois empiriques convertissant la temperature en donnees RGB

#Rq : uniquement la couleur de l'émission est représentée, par son intensité, comme elle varie en T^4 il est difficile d'afficher de telles variations sur un écran

#Constantes-------------------------
h = 6.63e-34
c = 3e8
k = 1.38e-23



lamda = np.arange(0.001,5,0.001)

#----------------------------------
#Temperature en RGB. Les lois de conversion proviennent d'un ajustement numerique que l'on pourra trouver a l'url http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/ (url active le 16 fevrier 2017)
def get_color(T):
    #Red
    if T < 6600:
        r = 255
    else:
        r = 329.698727446 * (T/100.-60)**(-0.1332047592)
        if r<0:
            r=0
        elif r>255:
            r=255
    #Green
    if T < 6600:
        g = 99.4708025861 * np.log(T/100.) - 161.1195681661
    else:
        g = 288.1221695283 * (T/100.-60)**(-0.0755148492)
    if g<0:
        g=0
    elif g>255:
        g=255
    #Blue
    if T>6600:
        b=255
    elif T<1900:
        b=0
    else:
        b = 138.5177312231 * np.log(T/100.-10) - 305.0447927307
    if b<0:
        b=0
    elif b>255:
        b=255
    r *= 1/255.
    g *= 1/255.
    b *= 1/255.
    return (r,g,b)

#----------------------------------

T = 3000
T_min = 1000
T_max = 15000
u = 8*np.pi*h*c/((lamda*1e-6)**5)* 1 / (np.exp(h*c/(lamda*1e-6*k*T))-1)



T_wien = np.linspace(T_min, T_max, 100)
w = []
lbd_wien = []

for temp in T_wien :
     u_k = 8*np.pi*h*c/((lamda*1e-6)**5)* 1 / (np.exp(h*c/(lamda*1e-6*k*temp))-1)
     w.append(max(u_k))
     lbd = np.argmax(u_k)
     lbd_wien.append(lamda[lbd])




fig = plt.figure()
plt.subplots_adjust(bottom=0.20)

ax1 = plt.subplot(121)
plt.plot(lamda,u, '-k', lw=4, label = "Planck")
plt.plot(lbd_wien, w, '--b', lw=2, label = "Wien $\lambda_{max} = C/T$")
plt.plot(lamda[np.argmax(u)],np.max(u), 'or', lw=4, markersize=15)
plt.xlabel("$\lambda (\mathrm{\mu m})$")
plt.ylabel("$u_\lambda (\mathrm{J/m^4})$")
plt.title('Loi de Planck')
plt.xticks(np.arange(0,5,0.8))
#l1, = ax1.plot([0.4, 0.4], [0, 200], '--', color = 'gray',  zorder = 0, lw=2)
#l2, = ax1.plot([0.8, 0.8],[0, 200], '--', color = 'gray', zorder = 1, lw=2)
plt.ylim([0., max(u[1:]*1.1)])
plt.legend(framealpha = 0.4)


def rect(x,y,w,h,c) :
    polygon = plt.Rectangle((x,y), w, h, color = c)
    ax1.add_patch(polygon)



def rainbow(X, Y, cmap = plt.get_cmap("jet")) :
    dx = X[1]-X[0]
    N = float(X.size)

    for n, (x,y) in enumerate(zip(X,Y)) :
        color = cmap(n/N)
        rect(x,0,dx,y,color)


X = np.arange(0.4, 0.801, 0.02)
Y = u[399:800:20]
rainbow(X,Y)




ax2 = plt.subplot(122)
circle = ax2.add_patch(
        patches.Circle(
            (0.5,0.5),0.4,color=get_color(T)
        )
)
ax2.set_yticklabels([])
ax2.set_xticklabels([])
plt.title('Couleur correspondante')

#Slider de temperature
axTemp = plt.axes([0.20,0.04,0.65,0.03])
sTemp = Slider(axTemp, 'Temperature (en $K$)', valmin=T_min, valmax=T_max, valinit=T, valfmt='%0.f')
def update(val):
    yl = ax1.get_ylim()
    ax1.clear()
    T = sTemp.val
    u1 = 8*np.pi*h*c/((lamda*1e-6)**5)* 1 / (np.exp(h*c/(lamda*1e-6*k*T))-1)
    w1 = 8*np.pi*h*c/((lamda*1e-6)**5)*np.exp(-h*c/(k*T*lamda*1e-6))
    rj1 = 8*np.pi*k*T/((lamda*1e-6)**4)
    ax1.plot(lamda,u1, '-k', lw=4, label = "Planck")
    ax1.plot(lbd_wien, w, '--b', lw=2, label = "Wien $\lambda_{max} = C/T$")
    ax1.plot(lamda[np.argmax(u1)],np.max(u1), 'or', lw=4, markersize=15)
    ax1.set_xlabel("$\lambda (\mathrm{\mu m})$")
    ax1.set_ylabel("$u_\lambda (\mathrm{J/m^4})$")
    ax1.set_title('Loi de Planck')
    ax1.set_xticks(np.arange(0,5,0.8))
    ax1.set_ylim(yl)
    ax1.legend(framealpha = 0.4)
    Y = u1[399:800:20]
    rainbow(X,Y)
    circle.set_facecolor(get_color(T))
    circle.set_edgecolor(get_color(T))
sTemp.on_changed(update)



#Rescale button
axBout = plt.axes([0.35,0.6,0.1,0.05])
Breset = Button(axBout, 'Rescale')
def rescale(event):
    u = ax1.lines[0].get_ydata()
    ax1.set_ylim([0,max(u)*1.1])
Breset.on_clicked(rescale)

mng = plt.get_current_fig_manager()     #Plein ecran
mng.window.showMaximized()
plt.show()