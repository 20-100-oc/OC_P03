import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd




def display_circles(pcs, n_comp, pca, axis_ranks, labels=None, label_rotation=0, lims=None, scale_factor=1):
    fig_size = [7,6]
    fig_size = list(np.array(fig_size) * scale_factor)

    for d1, d2 in axis_ranks: # On affiche les 3 premiers plans factoriels, donc les 6 premières composantes
        if d2 < n_comp:

            # initialisation de la figure
            fig, ax = plt.subplots(figsize=fig_size)

            # détermination des limites du graphique
            if lims is not None :
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30 :
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else :
                xmin, xmax, ymin, ymax = min(pcs[d1,:]), max(pcs[d1,:]), min(pcs[d2,:]), max(pcs[d2,:])

            # affichage des flèches
            # s'il y a plus de 30 flèches, on n'affiche pas le triangle à leur extrémité
            if pcs.shape[1] < 30 :
                plt.quiver(np.zeros(pcs.shape[1]), np.zeros(pcs.shape[1]),
                   pcs[d1,:], pcs[d2,:], 
                   angles='xy', scale_units='xy', scale=1, color="grey")
                # (voir la doc : https://matplotlib.org/api/_as_gen/matplotlib.pyplot.quiver.html)
            else:
                lines = [[[0,0],[x,y]] for x,y in pcs[[d1,d2]].T]
                ax.add_collection(LineCollection(lines, axes=ax, alpha=.1, color='black'))
            
            # affichage des noms des variables  
            if labels is not None:  
                for i,(x, y) in enumerate(pcs[[d1,d2]].T):
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax :
                        plt.text(x, y, labels[i], fontsize='14', ha='center', va='center', rotation=label_rotation, color="blue", alpha=0.5)
            
            # affichage du cercle
            circle = plt.Circle((0,0), 1, facecolor='none', edgecolor='b')
            plt.gca().add_artist(circle)

            # définition des limites du graphique
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        
            # affichage des lignes horizontales et verticales
            plt.plot([-1, 1], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-1, 1], color='grey', ls='--')

            # nom des axes, avec le pourcentage d'inertie expliqué
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Cercle des corrélations (F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)






def display_factorial_planes(X_projected, n_comp, pca, axis_ranks, df, alpha=1, scale_factor=1):
    fig_size = [7,6]
    fig_size = list(np.array(fig_size) * scale_factor)
    
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # initialisation de la figure       
            fig = plt.figure(figsize=fig_size)
        
            # affichage des points
            legend_column = 'additives_n'
            legend_title = 'nb additives'
            scatter = plt.scatter(X_projected[:, d1], 
                                  X_projected[:, d2], 
                                  c=df[legend_column].astype('category').cat.codes, 
                                  alpha=alpha)
            plt.legend(handles=scatter.legend_elements()[0], 
                       labels=range(df['additives_n'].shape[0]),
                       title=legend_title)
            
            # détermination des limites du graphique
            
            #old boundary:
            #boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            
            quantile = 0.99
            margin = 2
            boundary = np.quantile(np.abs(X_projected[:, [d1,d2]]), quantile) * margin
            
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])
        
            # affichage des lignes horizontales et verticales
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # nom des axes avec le pourcentage d'inertie
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Projection des individus (sur F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)

            
            
            
            
def display_factorial_planes_2(X_projected, n_comp, pca, axis_ranks, df, alpha=1, scale_factor=1):
    
    X_projected_df = pd.DataFrame(X_projected)
    X_projected_df.columns =['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
    
    fig_size = [7,6]
    fig_size = list(np.array(fig_size) * scale_factor)
    
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # initialisation de la figure       
            fig = plt.figure(figsize=fig_size)
        
            # affichage des points
            legend_column = 'additives_n'
            legend_title = 'nb additives'
            scatter = plt.scatter(X_projected[:, d1], 
                                  X_projected[:, d2], 
                                  c=df[legend_column].astype('category').cat.codes, 
                                  alpha=alpha)
            
            # détermination des limites du graphique
            #original boudary:
            #boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            
            #test boundary:
            quantile = 0.99
            margin = 2
            boundary = np.quantile(np.abs(X_projected[:, [d1,d2]]), quantile) * margin
            
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])
        
            # affichage des lignes horizontales et verticales
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # nom des axes avec le pourcentage d'inertie
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Projection des individus (sur F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)
            
            
            
            import altair as alt
            from altair import pipe, limit_rows, to_values
            
            point_size = 60

            
            # to be able to plot more than 5000 rows
            nb_rows = data_pca.shape[0]
            t = lambda data: pipe(data, limit_rows(max_rows=nb_rows), to_values)
            alt.data_transformers.register('custom', t)
            alt.data_transformers.enable('custom')

            tooltip = ['product_name', 
                       'nutrition_grade_fr'
                      ]

            alt.Chart(X_projected_df).mark_circle(size=point_size).encode(
                x='F1',
                y='F2',
                tooltip=tooltip
               )
            
            
            
            
            
def display_factorial_planes_old(X_projected, n_comp, pca, axis_ranks, labels=None, alpha=1, illustrative_var=None, scale_factor=1):
    fig_size = [7,6]
    fig_size = list(np.array(fig_size) * scale_factor)
    
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # initialisation de la figure       
            fig = plt.figure(figsize=fig_size)
        
            # affichage des points
            if illustrative_var is None:
                plt.scatter(X_projected[:, d1], X_projected[:, d2], alpha=alpha)
            else:
                illustrative_var = np.array(illustrative_var)
                for value in np.unique(illustrative_var):
                    selected = np.where(illustrative_var == value)
                    plt.scatter(X_projected[selected, d1], X_projected[selected, d2], alpha=alpha, label=value)
                plt.legend()

            # affichage des labels des points
            if labels is not None:
                for i,(x,y) in enumerate(X_projected[:,[d1,d2]]):
                    plt.text(x, y, labels[i],
                              fontsize='14', ha='center',va='center') 
                
            # détermination des limites du graphique
            boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])
        
            # affichage des lignes horizontales et verticales
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # nom des axes, avec le pourcentage d'inertie expliqué
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Projection des individus (sur F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)
            
            
            
            
            
            
def display_scree_plot(pca, scale_factor=1):
    fig_size = [7,6]
    fig_size = list(np.array(fig_size) * scale_factor)
    plt.rcParams['figure.figsize'] = fig_size
    
    scree = pca.explained_variance_ratio_*100
    plt.bar(np.arange(len(scree))+1, scree)
    plt.plot(np.arange(len(scree))+1, scree.cumsum(),c="red",marker='o')
    plt.xlabel("rang de l'axe d'inertie")
    plt.ylabel("pourcentage d'inertie")
    plt.title("Eboulis des valeurs propres")
    plt.show(block=False)
