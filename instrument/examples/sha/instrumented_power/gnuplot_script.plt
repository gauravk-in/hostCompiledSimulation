# VoLTE plot script
# Author: Bo Wang

#set terminal windows
set key off outside
#set size 1.0, 1.0


#set terminal png enhanced giant size 800, 600
set terminal pdfcairo enhanced size 4, 3 lw 1 font "Helvetica, 6"
#set terminal pdf enhanced "Helvetica, 12"
#set terminal postscript eps color defaultplex enhanced "Helvetica, 12"
#set terminal postscript eps color defaultplex enhanced font "Times New Roman, 12"


set xlabel   "CPU Cycles (million)" offset 0.0, 0.3
#set ylabel   "Battery Current [mA]" offset 0.0, 0.0
set ylabel   "Power Consumption (mW)" offset 1.0, 0.0
#set yrange [0 : 1.8]
#set yrange [0 : 1]
set rmargin 4
set grid


set output "power_trace.pdf"
#set title "VoLTE Power Consumption"
#set title "Power Consumption"
#plot "C:/Users/bwang33/Documents/Visual Studio 2010/Projects/Maestro/Projects/VoLTE_Integration/Debug/T.PowerMonitor.dat" using ($1/1e6):($2/240) title "VoLTE" with steps
plot "./power_trace_100000.dat" using ($2/1e6):3 with steps
#plot "C:/Users/bwang33/Desktop/VoLTE/Binary_Data/Un-Optimized/T.PowerMonitor_B5_C1_RX2TRX.dat" using ($1/1e6):($2/230) title "VoLTE" with steps

#set output
#unset output
#set terminal wxt

#exit
