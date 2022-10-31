#!/usr/bin/env python
"""This script is used to analyse the histograms produced by ntCard.
It takes the prefix of the histogram files as input and prints the
estimated number of distinct kmers occurring more than once.
"""
__author__ = "Pierre Peterlongo"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Pierre Peterlongo"
__email__ = "pierre.peterlongo@inria.fr"
__status__ = "Production"


import glob
import matplotlib.pyplot as plt
import argparse



# box plots
def box_plots (data, legends, k, constrain, output_file_name = None):
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    
    # Creating axes instance
    bp = ax.boxplot(data, patch_artist = True,
                    notch ='True', vert = 0)
    
    colors = ['seagreen', 'darkgreen', 
            'firebrick', 'maroon', 
            'royalblue', 'navy',
            'coral', 'darkorange',
            'orchid', 'm', 
            'darkkhaki', 'darkgoldenrod',
            '#0000FF', '#00FF00',
            '#FFFF00', '#FF00FF']
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    # changing color and linewidth of
    # whiskers
    for whisker in bp['whiskers']:
        whisker.set(color ='#8B008B',
                    linewidth = 1.5,
                    linestyle =":")
    
    # changing color and linewidth of
    # caps
    for cap in bp['caps']:
        cap.set(color ='#8B008B',
                linewidth = 2)
    
    # changing color and linewidth of
    # medians
    for median in bp['medians']:
        median.set(color ='red',
                linewidth = 3)
    
    # changing style of fliers
    for flier in bp['fliers']:
        flier.set(marker ='D',
                color ='#e7298a',
                alpha = 0.5)
        
    # x-axis labels
    ax.set_yticklabels(legends)
    
    # Adding title
    plt.title(f"Nb kmers unique and twice or more, k={k} {constrain}")
    
    # Removing top axes and right axes
    # ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
        
    # show plot
    # plt.show()
    
    if not output_file_name:
        if len(constrain) > 0: output_file_name = f"tara_estimations_k{k}_{constrain}.png"
        else: output_file_name = f"tara_estimations_k{k}.png"
    print(f"Saving figure in {output_file_name}")
        
    # save plot if file tara_estimations.png 
    fig.savefig(output_file_name, dpi=300)
    



    
def main():
    
    parser = argparse.ArgumentParser(description=f"Analyse the histograms produced by ntCard.\
                            It takes the prefix of the histogram files as input and prints & plots the\
                            estimated number of distinct kmers occurring more than once.")
    
    parser.add_argument("-p", help="Prefixes of the hist files (separated by a comma). Typically, the prefix is \"integrated,meso,micro,nano,pico,vir\".", 
                        dest='prefixes', type=str, required=True)
    parser.add_argument("-d", help="Directory of hist files (defaut = \"./\")", 
                        dest='directory', type=str, required=False, default="./")
    parser.add_argument("-k", help="kmer size. Warning: for printing only, no check is made for verifying the file name containing kXX corresponds to this value", type=int,
                        required=True)
    parser.add_argument("-c", help="[Constrain]: if specified, only the histogram files containing the given sequence are considered. Typically \"SUR\" for focalizing the anlysis on surface datasets", type=str,
                        dest="constrain", required=False, default="")
    parser.add_argument("-o", help="[Image file name]. If not specified: \"tara_estimations_kXX_constrain_XX.png\" or \"tara_estimations_kXX.png\" if no constrain is specified", type=str,
                        dest="output_file_name", required=False, default=None)
    args = parser.parse_args()
    
    
    if len(args.constrain) == 0:
        print(f"k = {args.k}, no constrain")
    else:
        print(f"k = {args.k}, constrain = {args.constrain}")
    data = []
    legends = []
    for prefix in args.prefixes.split(','):
        unique = []
        twice_or_more = []
        for filename in glob.glob(f"{args.directory}/{prefix}*{args.constrain}*.hist"):
            with open(filename, 'r') as f:
                # 36SUR0BBCC11_count_k20_k20.hist:
                # F1	3519450403
                # F0	836932707
                # 1	518021042
                _ = f.readline()  # this is F1, we don't care
                all_distinct = int(f.readline().strip().split()[1])
                once_distinct = int(f.readline().strip().split()[1])
                unique.append(all_distinct)
                twice_or_more.append(all_distinct - once_distinct)
                # print(f"{all_distinct - once_distinct}")
        # if no data: continue
        if len(unique) == 0:
            continue
            
        legends.append(f"{prefix}\nunique")
        legends.append(f"{prefix}\ntwice_or_more")
        # prints the min, max, average and median of the number of distinct kmers
        print(f"\n **{prefix}**, {args.constrain} nb sets = {len(unique)}")
        print(" unique:")
        print(f"  min: {min(unique)}")
        print(f"  max: {max(unique)}")
        print(f"  average: {sum(unique)//len(unique)}")
        print(f"  median: {sorted(unique)[len(unique)//2]}")
        
        # prints the min, max, average and median of the number of distinct kmers occurring more than once
        print(f" twice or more:")
        print(f"  min: {min(twice_or_more)}")
        print(f"  max: {max(twice_or_more)}")
        print(f"  average: {sum(twice_or_more)//len(twice_or_more)}")
        print(f"  median: {sorted(twice_or_more)[len(twice_or_more)//2]}")
        
        
        data.append(unique)
        data.append(twice_or_more)
        
    box_plots(data, legends, args.k, args.constrain, args.output_file_name)



if __name__ == '__main__':
    main()