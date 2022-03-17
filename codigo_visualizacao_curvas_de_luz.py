#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 18:16:39 2022

@author: taina
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.table import Table
from astropy.io import fits

#------------------Carregando os dados--------------------
with open('/home/taina/Projetos_IC/TargetDatas_tic/TDs_tic.pkl', 'rb') as arquivo:
    stars_tic = pickle.load(arquivo)

#-------------------------Menu----------------------------
print("\n" 
      "Menu:",
      "\n[n] para mostrar a próxima estrela \n"
      "[s] para pesquisar uma estrela específica no setor (TIC Id) \n"
      "[e] sair")

def funcao_saida():
    confirm = input('Tem certeza de que deseja sair? [y/n] ')
    if confirm == 'n':
        return True
    else:
        StopIteration

#---------Função que plota as curvas de luz e TPFs-------
def principal():
    n = 0
    while True:
        for i in stars_tic[n:]:
            folder = '/home/taina/Projetos_IC/TargetDatas_tic/starTIC_' + str(i)

            #mostra os dados iniciais
            source = pd.read_csv(folder + '/source_' + str(i) + '.csv', index_col=False)
            print(source)
            
            #Acesso ao arquivo .fit da estrela
            data = folder + '/TD_starTIC_' + str(i) + '.fits'    
            hdul1 = fits.getdata(data, ext=1)
            hdul2 = fits.getdata(data, ext=2)
            hdul3 = Table.read(data, hdu=3)

            #mostra TPF e abertura escolhida automaticamente
            raw = list(hdul1['RAW_FLUX'])
            dado = hdul3.values_equal(raw)
            colnames = [name for name in dado.colnames]
            for colname in colnames:
                if np.any(dado[colname] == True):
                    aperture = str(colname[:-4])

            tpf = hdul1[0][2]

            fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(12,6))
            ax1.imshow(hdul2[aperture])
            ax1.set_title('Abertura escolhida')
            ax2.imshow(tpf)
            ax2.set_title('Target Pixel File')
            ax3.imshow(tpf)
            ax3.imshow(hdul2[aperture], cmap='Greys', alpha=0.7)
            ax3.set_title('Abertura sobre TPF')
            plt.savefig(folder + '/TPF_Abertura_starTIC_' + str(i) + '.png', format='png')
        
            #mostra as curvas de luz bruta e corrigida
            q = hdul1['QUALITY'] == 0
        
            fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(16,12), sharex=True, sharey=True)
            fig.suptitle('TIC Id: 24265684', x=0.5, y=1.)
            data_raw_normalized = hdul1.field('RAW_FLUX')[q]/np.nanmedian(hdul1.field('RAW_FLUX')[q])
            data_corr_normalized = hdul1['CORR_FLUX'][q]/np.nanmedian(hdul1['CORR_FLUX'][q])
            time = hdul1['TIME'][q] - min(hdul1['TIME'][q])
            ax1.plot(time, data_raw_normalized , '.k', label='Curva de luz bruta')
            ax2.plot(time, data_corr_normalized, '.r', label='Curva de luz corrigida')
            ax1.set_xlim(min(time),max(time))
            y_ticks = np.linspace(round(min(data_raw_normalized),3), round(max(data_corr_normalized),3), 4)
            ax1.set_yticks(y_ticks)
            plt.subplots_adjust(bottom=0.1, top=0.9)
            fig.supylabel('Normalized Flux', x=0.07)
            ax2.set(xlabel='Time [BJD - 2457000]')
            ax1.legend(bbox_to_anchor=(0., 1.02), loc='lower left', borderaxespad=0.)
            ax2.legend(bbox_to_anchor=(0., 1.02), loc='lower left', borderaxespad=0.)
            #ax1.text(24, 0.4, "Data o primeiro ponto = 1325")
            ax1.grid()
            ax2.grid()
            plt.savefig(folder + '/comparação_starTIC_' + str(i) + '.png', format='png')
            
            plt.show()
            
            #mostra curva de luz PSF
            plt.plot(time, hdul1['PSF_FLUX'][q]/np.nanmedian(hdul1['PSF_FLUX'][q]))
            plt.title('Curva de luz PSF para TIC Id ' + str(i))
            plt.xlabel('Time [BJD - 2457000]')
            plt.ylabel('Normalized Flux')
            plt.xlim(min(time), max(time))
            plt.savefig(folder + '/curva_PSF_starTIC_' + str(i) + '.png', format='png')

            plt.show()        


            opcao = input("Digite a opção desejada conforme menu: ")
            if (opcao == "n"):
                continue   
            elif (opcao == "s"):
                break
            elif (opcao == "e"):
                if not funcao_saida():
                        return 
                    
        while True: 
            #usuário digita TIC Id da estrela
            search = input("Digite o TIC Id da estrela: ")
            #verifica se essa estrela está na amostra
            test = int(search) in stars_tic
            #se a estrela estiver na amostra, o índice dela na lista será o próximo a ser acessado
            if test == True:
                n = stars_tic.index(int(search))
                break
            else:
                print("Id inválido, tente novamente!")
                pass
            
principal()