set encoding iso_8859_1
# Output of plot
#set terminal postscript eps enhanced color font "Arial, 16"
set terminal postscript eps enhanced color "Helvetica"
#set terminal png linewidth 2.0 font "Helvetica" size 2000,1000
set output "histogram_angles.eps"

azul_normal="#1E90FF"
morado="#8000ff"
agua_marina="#3fb9b7"
rojo="#fd1112"
rosa="#fe88d3"

#Title
#set title "Hydration layer of hydrophobic ions: oxygen atom"

#set title "(c)" offset -34 font "Times-Roman, 24"
#show title

#names of data files
file1="histogram.dat"


#size of the page
set size 0.8,0.57
set key top right

#plot colors
set style line 3 linetype 1 pt 2 linecolor 5 lw 2
set style line 4 linetype 1 pt 6 linecolor 1 lw 2

#arrow
#set arrow 1 from 5.25, 1.9 to 5.25, 1.15 lt 1 lw 2 lc rgbcolor morado filled

#set axis
set xtics font ", 10"
set ytics font ", 10"
set xrange[-0.6:10.6]
set xtics out
set xtics 1
set mxtics 1
set xlabel "# PEGs linked to heparin"

set ylabel "# of heparins"
set yrange[0:80]
#set key bottom
#set ytics out
#set ytics 10
#set mytics 2
set style fill solid
set boxwidth 0.9

plot file1 u ($2):($1) with boxes title 'Count'


set terminal x11
replot
