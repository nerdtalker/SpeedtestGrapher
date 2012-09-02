from numpy import *
from scipy import *
from pylab import *
from datetime import *

###Some Constants
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
ATblue = '#085fb7'
ATorange = '#edac22'

###We only care about these columns, but can do more, lat,long eventually
colNames = {'Date' :0,'ConnType':1,'Download':2,'Upload':3,'Latency':4}
ratNames = {'Unk' :0, 'LTE':1, 'HSPA':2, 'EVDO':3}

###Define the device and network and filename
device_name = "LG Optimus 4X"
network = "AT&T"
datafile2 = 'O4X.csv';

def datesplit(s):
    escaped = ''.join(e for e in s if e.isalnum())
    return datestr2num(escaped)

def conntype(s):
    s = ''.join(e for e in s if e.isalnum()).upper()
    if (s == 'EVDO' or s == 'EHRPD' or s == 'EVDOA'):
        return 3
    if (s == 'HSPA' or s == 'UMTS' or s == 'HSDPA' or s == 'CELL'):
        return 2
    if (s == 'LTE' or s == 'WIFI'):
        return 1
    else:
        return 0

def loaddata():
    return loadtxt(datafile2,delimiter=',',usecols=(0,1,4,5,6),skiprows=1,converters = {0: datesplit, 1: conntype})
    
def filterdata(type):
    data = loaddata()
    filtered = array(filter(lambda x: x[1] == type, data))
    
    return filtered

def makehist(col,rat):
    cla();
    clf();
    
    if(colNames[col]==4):
        scaler=1.0
        color=ATblue
	xname = col +' (ms)'
    else:
        scaler=1000.0
        color=ATorange
	xname = col +' Throughput (Mbps)'
    
    data = filterdata(ratNames[rat])
    
    fig, ax = plt.subplots(1)
    hist(data[:,colNames[col]]/scaler,bins=30,facecolor=color,alpha=0.75);
    title(device_name + ' ' + network + ' ' + 'DC-HSPA+' + ' ' + col + ' - Speedtest.net')
    xlabel(xname)
    ylabel(r'Counts (binned)')
    grid(True)    
    
    #### Print this out in a nice formatted manner, eg
    #### Average, Max, Min, Stanard Deviation
    print('\nStats '+ xname)
    table = {'Avg': average(data[:,colNames[col]]/scaler), 'Max': max(data[:,colNames[col]]/scaler), 'Min': min(data[:,colNames[col]]/scaler), 'StDev':std(data[:,colNames[col]]/scaler)}
    print 'Avg: {Avg:.2f}, Max: {Max:.2f}, Min: {Min:.2f}, StDev: {StDev:.2f}'.format(**table)
    textstr = '$\mu=%.2f$\n$\mathrm{median}=%.2f$\n$\sigma=%.2f$\n$n=%d$'%(average(data[:,colNames[col]]/scaler), median(data[:,colNames[col]]/scaler), std(data[:,colNames[col]]/scaler), data.shape[0])
    
    # these are matplotlib.patch.Patch properies
    props = dict(boxstyle='round', facecolor=color, alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', horizontalalignment='right', bbox=props)
    
    savefig(device_name.replace(' ',"") + "_" + network.replace(' ',"") + rat +'_' + col +'.png', dpi=72)

def makehists(rat):
    makehist('Download',rat);
    makehist('Upload',rat);
    makehist('Latency',rat);


