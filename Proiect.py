# -*- coding: utf-8 -*-


# ----- Implementare algoritm Niblack -----

# Parametrii algoritmului:
 # imagine
 # n: marimea vecinatatii
 # k: factor de corectie, depinde de zgomotul activ in fundal, cu val -0,1 sau -0,2
 # t: valoarea de prag
 # m: valoarea medie a pixelilor pi
 #
 
 # Rezultat:
 # imagine binara pe niveluri de gri, obtinuta prin metoda Niblack

import cv2
import math 
import numpy as np
from matplotlib import pyplot as plt

#citirea imaginii
InImg = cv2.imread('handwriting.jpg',0)


DPI=100
H,W=InImg.shape

#binarizarea simpla
ret,thresh1 = cv2.threshold(InImg,128,255,cv2.THRESH_BINARY)

plt.figure(figsize=(W/DPI+1,H/DPI+1));

n = 2 #mărimea vecinătății
k= -0.2 #factor de coretie

Height, Width = InImg.shape # obtinem lungimea si inaltimea imaginii pe niveluri de gri

image = np.pad(InImg, [n, n],'symmetric') # largeste matricea imaginii originale

NewHeight = Height + 2*n
NewWidth = Width +2*n

imagineNiblack = np.zeros((NewHeight, NewWidth)) # o matrice noua de zerouri cu noile dimensiuni
 
for i in range(1+n, Height+n) :
   for j in range(1+n, Width+n) :
       
       #trasarea chenarului 
       randSus = i - math.floor(n/2 - 1/2); # Randul de sus, randul de jos
       randJos = i + math.floor(n/2); 
       randSus_Jos = range(randSus, randJos+1)
       
       coloanaStanga = j - math.floor(n/2 - 1/2); # Coloana din stanga, dreapta
       coloanaDreapta = j + math.floor(n/2); 
       coloanaStanga_Dreapta = range(coloanaStanga, coloanaDreapta+1)
       
       #pregatim chenarul
       chenar = [randSus_Jos, coloanaStanga_Dreapta]
       
       # calculam valoarea medie a tuturor pixelilor
       mean_all = np.mean(np.mean((image))) 
       
       # Calculam deviatia standard
       deviatiaPatrata = chenar - mean_all
       deviatiaPatrata = np.mean(np.mean(deviatiaPatrata * deviatiaPatrata))
       deviatia = math.sqrt(deviatiaPatrata) 
       
       #setam o valoare de prag conform Niblack
       T = mean_all + k * deviatia # T=k*s(x,y)+m(x,y) valoare prag
       
       #construim noua imagine, cu pixelii stabiliti in functie de pragul ales
       if (image[i][j] > T) : imagineNiblack[i][j] = 1 #daca e mai mare decat pragul, pixelul e negru
       else : imagineNiblack[i][j] = 0  #daca e mai mic decat pragul, pixelul e alb

# pregatirea imaginilor, a titlurilor, si afisarea rezultatelor : 
titles = ['Imagine Originala Pe Niveluri De Gri','Imagine Binarizata', 'Imagine Niblack']
images = [InImg, thresh1, imagineNiblack]

plt.figure(figsize=(1000/DPI+1,1000/DPI+1));

for i in range(0,3) :
    plt.subplot(3,1, i+1), plt.imshow(images[i], cmap= 'gray' )
    plt.title(titles[i])
    
plt.show()



