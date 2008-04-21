#  ICE Revision: $Id: /local/openfoam/Python/PyFoam/PyFoam/Basics/GnuplotTimelines.py 2846 2008-03-03T22:57:45.744826Z bgschaid  $ 
"""Plots a collection of timelines"""

from PyFoam.ThirdParty.Gnuplot import Gnuplot,Data
    
from os import uname

class GnuplotTimelines(Gnuplot):
    """This class opens a gnuplot window and plots a timelines-collection in it"""
    
    terminalNr=1
    
    def __init__(self,timelines,persist=None,raiseit=True,with="lines",alternateAxis=[],forbidden=[],start=None,end=None,logscale=False):
        """@param timelines: The timelines object
        @type timelines: TimeLineCollection
        @param persist: Gnuplot window persistst after run
        @param raiseit: Raise the window at every plot
        @param with: how to plot the data (lines, points, steps)
        @param alternateAxis: list with names that ought to appear on the alternate y-axis
        @param forbidden: A list with strings. If one of those strings is found in a name, it is not plotted
        @param start: First time that should be plotted. If undefined everything from the start is plotted
        @param end: Last time that should be plotted. If undefined data is plotted indefinitly
        @param logscale: Scale the y-axis logarithmic
        """

        Gnuplot.__init__(self,persist=persist)
        self.alternate=alternateAxis
        self.forbidden=forbidden

        if start or end:
            rng="["
            if start:
                rng+=str(start)
            rng+=":"
            if end:
                rng+=str(end)
            rng+="]"
            self.set_string("xrange "+rng)
            
        if len(self.alternate)>0:
            self.set_string("y2tics")

        if logscale:
            self.set_string("logscale y")
            
        if raiseit:
            x11addition=" raise"
        else:
            x11addition=" noraise"
            
        if uname()[0]=="Darwin":
            self.set_string("terminal x11"+x11addition)
            # self.set_string("terminal aqua "+str(GnuplotTimelines.terminalNr))
            GnuplotTimelines.terminalNr+=1
        else:
            self.set_string("terminal x11"+x11addition)
            
        self.data=timelines
        self.with=with
        
        self.redo()
        
    def redo(self):
        """Replot the timelines"""
        times=self.data.getTimes()
        if len(times)<=0:
            return
        
        tmp=self.data.getValueNames()
        names=[]
        for n in tmp:
            addIt=True
            for f in self.forbidden:
                if n.find(f)>=0:
                    addIt=False
                    break
            if addIt:
                names.append(n)
                
        self.itemlist=[]
        for n in names:
            it=Data(times,self.data.getValues(n),title=n,with=self.with)
            if n in self.alternate:
                it.set_option(axes="x1y2")
                
            self.itemlist.append(it)

        if len(names)>0 and len(times)>0:
            self.replot()
       