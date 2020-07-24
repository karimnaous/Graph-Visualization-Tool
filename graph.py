#Sources:
#1. https://towardsdatascience.com/catching-that-flight-visualizing-social-network-with-networkx-and-basemap-ce4a0d2eaea6
#2. https://stackoverflow.com/questions/54412983/color-nodes-by-networkx
#3. https://github.com/tuangauss/DataScienceProjects/blob/master/Python/flights_networkx.py

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.lines as mlines
import argparse
import copy

# Global Variables
opo_centers = []    # list of all opo_centers by center code
transplant_centers = []     # list of all transplant_centers by center code

#####
def createGraph(data_folder: str):

    distances = pd.read_csv("./{}/distances.csv".format(data_folder))
    G = nx.Graph()  # create an empty graph

    # add opo centers to graph and add to opo_centers list
    for center in distances["Unnamed: 0"]:
        opo_centers.append(center[:4] + '-OPO')
        # Take 4-letter code and add -OPO suffix
        G.add_node(center[:4] + '-OPO', type='source')

    # add tranplant centers to graph and add to transplant_centers list
    for center in distances.columns[1:]:
        transplant_centers.append(center[:4] + '-TPC')
        # Take 4-letter code and add -TPC suffix
        G.add_node(center[:4] + '-TPC', type='target')

    # find all edges and add to graph
    for ind in range(len(distances["Unnamed: 0"])):
        # for each OPO in distances list
        for center in distances.columns[1:]:
            # check distance to each transplant center
            if (distances[center][ind] != 'Too far'):
                if (float(distances[center][ind]) <= 500):
                    # Edge created and added to list if distance <= 500 mi
                    G.add_edge(distances["Unnamed: 0"][ind][:4] + '-OPO',
                                                            center[:4] + '-TPC')

    return G;
#####

#####
def plot_figure(G, opo_info, tpc_info, opo_attribute: list, tpc_attribute: list,
                                            marker: str, color: str, label:str):

    plt.figure(figsize = (14, 9))

    m = Basemap(projection='merc', llcrnrlon=-130, llcrnrlat=23, urcrnrlon=-63,
                    urcrnrlat=50, lat_ts=0, resolution='l', suppress_ticks=True)

    # Get coordinates for opo centers and store in dictionary
    mx, my = m(opo_info['Long'].values, opo_info['Lat'].values)
    opo_positions = {}
    for count, elem in enumerate (opo_centers):
         opo_positions[elem] = (mx[count], my[count])

    # Get coordinates for transplant centers and store in dictionary
    mx, my = m(tpc_info['Long'].values, tpc_info['Lat'].values)
    tpc_positions = {}
    for count, elem in enumerate (transplant_centers):
         tpc_positions[elem] = (mx[count], my[count])

    nx.draw_networkx_nodes(G=G, pos=opo_positions, nodelist=opo_centers,
                node_color='royalblue', alpha=0.9, node_shape='o', linewidths=0,
                                                node_size=opo_attribute)

    nx.draw_networkx_nodes(G=G, pos=tpc_positions, nodelist=transplant_centers,
                    node_color=color, alpha=0.8, node_shape=marker, linewidths=0,
                                                    node_size=tpc_attribute)

    # dict of all position (merge opo and tpc lists)
    all_pos = copy.deepcopy(opo_positions)
    all_pos.update(tpc_positions)

    nx.draw_networkx_edges(G=G, pos=all_pos, edge_color='g', alpha=0.2, arrows=False)

    m.drawcountries(linewidth = 2.5)
    m.drawstates(linewidth = 0.2)
    m.drawcoastlines(linewidth=1)
    m.fillcontinents(alpha = 0.3)
    line1 = mlines.Line2D([], [], color="blue", marker='.', linestyle='None',
                                                        markersize=15, alpha=0.8)
    line2 = mlines.Line2D([], [], color=color, marker=marker, linestyle='None',
                                                        markersize=15, alpha=0.6)
    line3 = mlines.Line2D([], [], color="green", label='Reachable', alpha=0.35)

    plt.legend((line1, line2, line3), ('OPO Center (size: number of donations processed)',
                            label, 'Reachable'), loc=3, fontsize = 'xx-large')

    plt.title("Transplant and OPO Centers in the United States", fontsize = 30)

    plt.tight_layout()

    plt.savefig("./map.png", format = "png", dpi = 300)

    plt.show()
#####

#####
def main():

    # inputs:
    #   data_folder: directory which includes required .csv files
    #   tpc_attribute_selector: which of the four attributes to determine
    #       size of transplant center nodes
    parser = argparse.ArgumentParser()
    parser.add_argument("data_folder", help="name of directory with input data")
    parser.add_argument("tpc_attribute_selector", help=
                        "either: Liver_Arrival_Rate, Registerer_Arrival_Rate,"
                                       + " Total_on_Waitlist, Deaths_per_Year")
    args = parser.parse_args()

    # Options: Liver_Arrival_Rate, Registerer_Arrival_Rate, Total_on_Waitlist,
    #           Deaths_per_Year
    tpc_attribute_selector = args.tpc_attribute_selector

    # Loading info on each center for use in visualization of nodes / edges
    opo_info = pd.read_csv("./{}/opo_info.csv".format(args.data_folder))
    tpc_info = pd.read_csv("./{}/tpc_info.csv".format(args.data_folder))

    G = createGraph(args.data_folder)

    # opo_attribute is the number of donated livers processed by each center
    opo_attribute = opo_info['Arrival Rate']

    if (tpc_attribute_selector == 'Liver_Arrival_Rate'):
        tpc_attribute = tpc_info['Liver Arrival Rate']
        plot_figure(G, opo_info, tpc_info, opo_attribute, tpc_attribute,
           'P', 'red', 'Transplant Center (size: average transplants per year)')

    elif (tpc_attribute_selector == 'Registerer_Arrival_Rate'):
        tpc_attribute = tpc_info['Registerer Arrival Rate']
        plot_figure(G, opo_info, tpc_info, opo_attribute, tpc_attribute,
'>', 'darkorange', 'Transplant Center (size: average addition to waitlist per year)')

    elif (tpc_attribute_selector == 'Total_on_Waitlist'):
        tpc_attribute = tpc_info['Total waitlist']
        plot_figure(G, opo_info, tpc_info, opo_attribute, tpc_attribute,
'D', 'orangered', 'Transplant Center (size: average number of patients on waitlist)')

    elif (tpc_attribute_selector == 'Deaths_per_Year'):
        tpc_attribute = tpc_info['Deaths']
        plot_figure(G, opo_info, tpc_info, opo_attribute, tpc_attribute,
            'X', 'black', 'Transplant Center (size: average deaths per year)')

    else:
        print('Error: Invalid Selection')

#####

if __name__ == "__main__":
        main()
