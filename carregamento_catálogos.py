#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 12:17:19 2022

@author: taina
"""

import eleanor
import pickle
import pandas as pd
from pathlib import Path
from astroquery.mast import Catalogs


#------------------DIRETÓRIOS--------------------
folder1 = '/home/taina/Projetos_IC/TargetDatas_tic'
Path(folder1).mkdir(exist_ok=True)
#folder = '/home/taina/curvas_de_luz/TargetDatas_ctl'
#Path(folder).mkdir(exist_ok=True)

#-------------Acesso aos catálogos-------------
'''
O acesso ao catálogo se dá por um critério, o intervalo entre mínima e máxima declinação das observações.
O catálogo TIC está separado por esse critério, portanto, para percorrer o catálogo, é interessante seguir 
os intervalos que podem ser vistos no link: https://archive.stsci.edu/tess/tic_ctl.html 
'''
dados1 = Catalogs.query_criteria(catalog="Tic", dec=[88.,90.], objType="STAR")
#criando lista de amostras do Catálogo TIC - TIC Ids das estrelas não repetidas
tic_teste = list(dict.fromkeys(dados1['ID']))   
stars_tic = tic_teste[:5]
print(stars_tic)


#dados2 = Catalogs.query_criteria(catalog="CTL", Tmag=[10.75,11], objType="STAR")

#criando lista de amostras do Catálogo CTL - TIC Ids das estrelas não repetidas
#ctl_teste = list(dict.fromkeys(dados2['objID']))   
#amostra_ctl = ctl_teste[:5]
#print(amostra_ctl)


#----------Carregamento prévio dos dados--------

with open(folder1 + '/TDs_tic.pkl', 'wb') as arquivo:
    pickle.dump(stars_tic, arquivo)
    
#with open('/home/taina/curvas_de_luz/Testes/TargetDatas_ctl_amostra/amostra_ctl.pkl', 'wb') as arquivo:
    #pickle.dump(amostra_ctl, arquivo)

for i in stars_tic:
    '''
    Cria um diretório para cada estrela da amostra, onde são armazenados os dados carregados
    o arquivo .fit e as curvas de luz
    '''
    folder = folder1 + '/starTIC_' + str(i)
    Path(folder).mkdir(exist_ok=True)
    star = eleanor.Source(tic=i) #sem setor, retorna o mais recente
    dados = pd.DataFrame({'TIC_Id':star.tic,'Gaia':star.gaia, 
                          'TESS_Magnitude':star.tess_mag,'RA':star.coords[0],
                          'DEC':star.coords[1]}, index=[0])
    dados.to_csv(folder + '/source_' + str(i) + '.csv', index=False)
    data = eleanor.TargetData(star, height=15, width=15, bkg_size=31, do_psf=True, do_pca=True)    
    data.save(folder + '/TD_starTIC_' + str(i) + '.fits')
  
        
    