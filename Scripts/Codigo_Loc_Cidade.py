#IMPORTANDO BIBLIOTECAS
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.patches import Polygon, Rectangle
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#Abrindo shape do Brasil
brasil = gpd.read_file('/caminho/BR_Pais_2024.shp')

#Abrindo shape do estado do desejado
shp_estados= gpd.read_file('/caminho/Unidades_Federacao_2024.shp')

  #selecionando o estado por seu código
estado = shp_estados[shp_estados['CD_UF'] == 'cod do estado desejado']

#Abrindo shp dos municípios do estado
shp_cidade = gpd.read_file('/caminho/Estado_Municipios_2024.shp')

  #selecionando a cidade por seu código
cidade = shp_cidade[shp_cidade['CD_MUN'] == 'cod da cidade desejada']


#---------------------CRIANDO A FIGURA---------------------------------
fig= plt.figure(figsize=(8,6.8)) #largura (horizontal), comprimento (vertical)

plt.rcParams['font.family'] = 'DejaVu Sans'  # escolha da fonte padrão


  #montando o mapa PRINCIPAL no eixo à esquerda-----------------------------------
ax = fig.add_axes([0.06, 0.10, 0.50, 0.88])
                #os valores representam, respectivamente: left, bottom, width, height

ax.set_aspect('auto')

ax.set_facecolor('lightblue') #cor para ficar no fundo, e que servirá de base para o Oceano

xmin, ymin, xmax, ymax = cidade.total_bounds #delimitando de acordo com as fronteiras da cidade
municipios_recorte = shp_cidade[shp_cidade.intersects(cidade.buffer(0.15).unary_union)] #fazendo um buffer para manter as cidades unidas e evitar a perda de alguma geometria

municipios_recorte.plot(ax=ax, edgecolor='black', facecolor='gainsboro') #plotando os municípios do estado com determinada cor
cidade.plot(ax=ax,edgecolor='black',linewidth=1,facecolor='#dfc37d') #plotando a cidade desejada em destaque com determinada cor

  #Definindo limites pra manter a cidade bem ao centro
ax.set_xlim(xmin-0.06, xmax+0.06)
ax.set_ylim(ymin-0.04, ymax+0.04)

  #Exemplo para adicionar os nomes das cidades vizinhas: lat, lon, texto, tamanho da fonte
ax.text(-43.10,-22.60, 'Magé', fontsize=10)

ax.locator_params(axis='x', nbins=5) # O nbins é para a qtd aproximada de divisões para a grade em tal eixo
ax.locator_params(axis='y', nbins=5)

  #Formatando as coordenadas para W e S usando graus e minutos
     #Para Longitude com 2 decimais
ax.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60):02d}'W"))

     #Para Latitude com 2 decimais
ax.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60):02d}'S"))

ax.tick_params(axis='y', labelrotation=90) #inclinação em 90° da latitude (eixo y)

ax.tick_params(axis='both', labelsize=9)  # reduz tamanho dos números de longitude e latitude


#Barra de escala automática
scalebar = ScaleBar(111000,location='lower right', #posição
    length_fraction=0.18, #se estiver pegando na borda
    width_fraction=0.008, #espessura da barra
    box_alpha=0,color='black', #cor
    scale_loc='bottom',font_properties={'size': 8})

ax.add_artist(scalebar) #adicionando a barra

'''
Trecho para criar uma rosa dos ventos simples e manualmente
#Criando Rosa dos Ventos simples------------------------------------------------------------
  # dx e dy controlam o deslocamento dentro do eixo
dx, dy = 0.02, 0.00

triangulo_preto = Polygon([[1.03+dx,0.93-dy], [1.00+dx,0.80-dy], [1.06+dx,0.80-dy]],transform=ax.transAxes,facecolor='black',clip_on=False)

triangulo_branco = Polygon([[1.03+dx,0.68-dy], [1.00+dx,0.80-dy], [1.06+dx,0.80-dy]],transform=ax.transAxes,facecolor='white',edgecolor='black',clip_on=False)

ax.add_patch(triangulo_preto) #adicionando no mapa principal
ax.add_patch(triangulo_branco)

  #Adicionando letra N
ax.text(1.03+dx, 0.97-dy,'N',transform=ax.transAxes,ha='center',fontsize=12)

'''
#MAPAS NO EIXO À DIREITA------------------------------------------
  #Colocando o Brasil-----------------------
ax_br = fig.add_axes([0.69, 0.57, 0.30, 0.30],projection=ccrs.PlateCarree())
                #os valores representam, respectivamente: left, bottom, width, height

ax_br.set_facecolor('lightblue') #colorindo o fundo com azul claro para fazer o oceano

ax_br.coastlines(linewidth=0.5) #adicionando as linhas de costa, o que só é possível em razão do uso do ccrs ali em cima

ax_br.add_feature(cfeature.LAND, facecolor='white') #colorindo o continente de branco, possível apenas com o uso do cfeature

ax_br.add_feature(cfeature.BORDERS,linewidth=0.5) #adicionando as fronteiras, o que só é possível em razão do uso do ccrs ali em cima

shp_estados.plot(ax=ax_br, edgecolor='black',linewidth=0.8, facecolor='gainsboro') #plotando os estados brasileiros com determinada cor

estado.plot(ax=ax_br, color='#red') #plota o estado em vermelho no mapa do Brasil

ax_br.set_title('Título apropriado') #se quisesse em Negrito: weight='bold'

#Formatando as coordenadas
ax_br.locator_params(axis='x', nbins=5) #O nbins é para a qtd aproximada de divisões para a grade no eixo
ax_br.locator_params(axis='y', nbins=4)

ax_br.set_xticks([-70, -55, -40], crs=ccrs.PlateCarree()) #controlando as divisões da grade do eixo x
ax_br.set_yticks([-30, -20,-10, 0], crs=ccrs.PlateCarree()) #controlando as divisões da grade do eixo y

  #Coordenadas para W e S usando graus e minutos
     #Para Longitude
ax_br.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60)}'W"))

     #Para latitude
ax_br.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60)}'S"))

ax_br.tick_params(axis='y', labelrotation=90) #inclinação em 90°

ax_br.tick_params(axis='both', labelsize=8)  # tamanho dos números de longitude e latitude

  #Adicionando o nome do oceano na lateral direita
ax_br.text(0.75, 0.1, 'oceano', #com coordenadas para posicionar o texto e qual texto quer adicionar
        transform=ax_br.transAxes,fontsize=8.7, #tamanho da fonte
        style='italic', #estilo da fonte
        alpha=0.7,color='black',rotation=26, #rotação do texto, se quiser alinhado é só tirar esse parâmetro
        ha='center') #posição central

#MAPA DO estado------------------------------
ax_estado = fig.add_axes([0.69, 0.20, 0.30, 0.30]) #posicionamento do mapa na figura
                #os valores representam, respectivamente: left, bottom, width, height

ax_estado.set_facecolor('lightblue') #cor que vai ficar no fundo

  #Trecho para controlar o tamanho do estado ainda que as fronteiras apareçam
xmin, ymin, xmax, ymax = rj.total_bounds
ax_rj.set_xlim(xmin-0.3, xmax+0.3) #limites no eixo x
ax_rj.set_ylim(ymin-0.2, ymax+0.2) #limites no eixo y

shp_estados.plot(ax=ax_rj, edgecolor='black', linewidth=0.8,facecolor='white') #para aparecer os estados que fazem fronteira

  #Para adicionar os nomes dos estados: lat, lon, texto, tamanho da fonte
ax_estado.text(-44.5, -21.5, 'MG', fontsize=10)
ax_estado.text(-41.5, -21.0, 'ES', fontsize=10)
ax_estado.text(-45, -22.8, 'SP', fontsize=10)


shp_cidade.plot(ax=ax_estado, edgecolor='black',linewidth=0.8, facecolor='gainsboro')
cidade.plot(ax=ax_estado, color='blue') #plota a cidade em azul no mapa do estado

#Formatando coordenadas
ax_estado.locator_params(axis='x', nbins=5) #O nbins é para a qtd aproximada de divisões para a grade no eixo x
ax_estado.locator_params(axis='y', nbins=3)
 
  #Formatando as coordenadas para W e S usando graus e minutos
     #Para Longitude sem decimais
ax_estado.xaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60)}'W"))

     #Para latitude sem decimais
ax_estado.yaxis.set_major_formatter(FuncFormatter(lambda valor, pos: f"{int(abs(valor))}°{int((abs(valor)-int(abs(valor)))*60)}'S"))

ax_estado.tick_params(axis='y', labelrotation=90) #inclinação em 90°
ax_estado.tick_params(axis='both', labelsize=8)

ax_estado.set_title('Título apropriado')

  #Adicionando o nome do oceano na lateral direita do mapa do estado
ax_estado.text(0.7, 0.1, 'Oceano', #com coordenadas para posicionar o texto e qual texto quer adicionar
        transform=ax_rj.transAxes,fontsize=9, #tamanho da fonte
        style='italic', #estilo da fonte
        alpha=0.7,rotation=0, #rotação do texto, se quiser alinhado é só tirar esse parâmetro
        ha='center') #posição central


#Título no mapa------------------------------------
fig.suptitle('Município de .... - sigla do estado', fontsize=16, weight= 'bold', y=0.98)


#Legenda de autoria e referência-----------------------------
caixa_legenda= mpatches.Patch(color='white', edgecolor='black')

fig.text(0.04, 0.03, #posição no eixo x, e posição no eixo y. Quanto menor o número no 1º argumento, mais perto do canto esquerdo a legenda fica
         'Fonte: órgão (ano).\nElaborado por nome do(a) autor(a) (ano).\nSistema: .',fontsize=10,
         multialignment='left', #para alinhar todo o texto da legenda à esquerda
         bbox=dict(facecolor='white',edgecolor='black',linewidth=1,boxstyle='square,pad=0.6'))


#Para moldura em volta da figura toda
fig.patches.append(Rectangle((0,0),1,1, fill=False, transform=fig.transFigure,edgecolor='black', linewidth=1.5, zorder=10))


#Legenda para os mapas
caixa_cidade= mpatches.Patch(color='#dfc37d',  edgecolor='black', label='título apropriado')
caixa_br = mpatches.Patch(color='red', edgecolor='black', label='título apropriado')
caixa_estado = mpatches.Patch(color='blue', edgecolor='black', label='título apropriado')

fig.legend(handles=[caixa_cidade, caixa_estado,caixa_br],
    title='Legenda',title_fontsize=13, #tamanho da fonte do título da legenda
    fontsize=11, #tamanho da fonte dos nomes das caixinhas
    loc='lower right', #posição de referência da legenda
    bbox_to_anchor=(1, 0.005), #posição certinha para controlar o afastamento da moldura
    borderpad=0.3, #controla espaço entre a borda da caixa e o conteúdo
    edgecolor='black', #contorno preto
    labelspacing=0.5, #espaço entre o conteúdo
    handlelength=1.2, #comprimento das caixinhas
    handleheight=1.2)  #altura das caixinhas


# Para colocar a grade por cima do mapa principal
ax.grid(True, linestyle='--',linewidth=0.4,color='black',alpha=0.4)

#Criando Rosa dos Ventos a partir de uma imagem própria
  #Carregando a imagem
img_rosa = mpimg.imread('/caminho/sua-rosa-dos-ventos.png')

# Criar OffsetImage e controlar tamanho
imagebox = OffsetImage(img_rosa, alpha=1, zoom=0.03,resample=True)  # zoom ajusta o tamanho na figura e resample=True mantém a qualidade

# Posicionar na figura
rosa_final = AnnotationBbox(imagebox, (0.63, 0.85), frameon=False, xycoords='figure fraction')

#Adicionando a rosa dos ventos em relação ao eixo do mapa principal
ax.add_artist(rosa_final)

plt.savefig('/caminho/Nome-da-Figura.png', dpi=300, bbox_inches= 'tight')

plt.show()
