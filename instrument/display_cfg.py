import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from collections import deque

from cfg import *

class Graph(pg.GraphItem):
    def __init__(self):
        self.dragPoint = None
        self.dragOffset = None
        self.textItems = []
        pg.GraphItem.__init__(self)
        self.scatter.sigClicked.connect(self.clicked)
        
    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.data = kwds
        if 'pos' in self.data:
            npts = self.data['pos'].shape[0]
            self.data['data'] = np.empty(npts, dtype=[('index', int)])
            self.data['data']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.updateGraph()
        
    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)
        
    def updateGraph(self):
        pg.GraphItem.setData(self, **self.data)
        for i,item in enumerate(self.textItems):
            item.setPos(*self.data['pos'][i])
        
        
    def mouseDragEvent(self, ev):
        if ev.button() != QtCore.Qt.LeftButton:
            ev.ignore()
            return
        
        if ev.isStart():
            # We are already one step into the drag.
            # Find the point(s) at the mouse cursor when the button was first 
            # pressed:
            pos = ev.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if len(pts) == 0:
                ev.ignore()
                return
            self.dragPoint = pts[0]
            ind = pts[0].data()[0]
            self.dragOffset = self.data['pos'][ind] - pos
        elif ev.isFinish():
            self.dragPoint = None
            return
        else:
            if self.dragPoint is None:
                ev.ignore()
                return
        
        ind = self.dragPoint.data()[0]
        self.data['pos'][ind] = ev.pos() + self.dragOffset
        self.updateGraph()
        ev.accept()
        
    def clicked(self, pts):
        print("clicked: %s" % pts)
            
verticalGap = 5
horizontalGap = 15

def display_cfgs(app, cfg1, cfg2, windowTitle):
    # Initialization of Qt
    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)
    w = pg.GraphicsWindow()
    w.setWindowTitle(windowTitle)
    
    
    v1 = w.addViewBox()
    v1.setAspectLocked()
    g1 = Graph()
    v1.addItem(g1)
    (pos, adj, texts, symbols) = draw_cfg(cfg1)
    
    g1.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts, symbol=symbols)
    
    v2 = w.addViewBox()
    v2.setAspectLocked()
    g2 = Graph()
    v2.addItem(g2)
    (pos, adj, texts, symbols) = draw_cfg(cfg2)
    
    print adj
    g2.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts, symbol=symbols)
                
    app.exec_();
    
    

def draw_cfg(cfg1):
    logging.debug ("Inside Function draw_cfg()")
    '''
    Breadth first search for all blocks in the Control Flow Graph to print them
    on screen.
    '''
    posOfBlock = {}
    posOfBlock[0] = 0
    
    symbols = ['+']
    pos = np.array([[0, 0]])
    adj = None
    texts = ["%s" % cfg1.listBlocks[0].name]
    
    # Queue for BFS
    q = deque([0])
    while q:
        
        # Extract entry from queue, will be 0 for the first iteration.
        blockInd = q.popleft()
        logging.debug ("Block %d" % blockInd)
        # Find all children of the
        succBlocks = cfg1.successorBlocks(blockInd)
        print "\t successors = ",
        print succBlocks
        spaceForChildren = (len(succBlocks) - 1) * horizontalGap
        logging.debug ("\t has %d children, space = %d" % (len(succBlocks), spaceForChildren))
        
        if len(succBlocks) > 1:
            i = 0
            for succBlock in succBlocks:
                if succBlock == blockInd:
                    # Self Edge!!
                    continue
                logging.debug ("\t Successor Block %d" % succBlock)
                if succBlock in posOfBlock:
                    logging.debug ("\t\t Already drawn at %d, %d" % (pos[posOfBlock[succBlock]][0], pos[posOfBlock[succBlock]][1]))
                    if adj == None:
                        adj = np.array([[posOfBlock[blockInd], posOfBlock[succBlock]]])
                    else:
                        adj = np.insert(adj, len(adj), [posOfBlock[blockInd], posOfBlock[succBlock]], axis = 0)
                else:
                    parent = None
                    for predBlock in cfg1.predecessorBlocks(succBlock):
                        if predBlock in posOfBlock:
                            parent = predBlock
                            break;
                    if parent == None:
                        # should never occur
                        logging.error ("Parent of a child does not exist, which should never happen!")
                        exit(1)
                    parentPos = pos[posOfBlock[parent]]
                    posSuccBlock = [parentPos[0] - (spaceForChildren/2) + (i*horizontalGap), parentPos[1] - verticalGap]
                    posOfBlock[succBlock] = len(pos)
                    pos = np.insert(pos, len(pos), posSuccBlock, axis = 0)
                    if adj == None:
                        adj = np.array([[posOfBlock[blockInd], posOfBlock[succBlock]]])
                    else:
                        adj = np.insert(adj, len(adj), [posOfBlock[blockInd], posOfBlock[succBlock]], axis = 0)
                    logging.debug ("\t\t Drawn at %d, %d" % (posSuccBlock[0], posSuccBlock[1]))
                    texts.append("%s" % cfg1.listBlocks[succBlock].name)
                    if cfg1.listBlocks[succBlock].isReturning == 1:
                        symbols.append('x')
                    else:
                        symbols.append('o')
                    if succBlock not in q:
                        q.append(succBlock)
                    i = i + 1
                
        elif len(succBlocks) == 1:
            succBlock = succBlocks[0]
            logging.debug ("\t Successor Block %d" % succBlock)
            if succBlock in posOfBlock:
                logging.debug ("\t\t Already drawn at %d, %d" % (pos[posOfBlock[succBlock]][0], pos[posOfBlock[succBlock]][1]))
                if adj == None:
                    adj = np.array([[posOfBlock[blockInd], posOfBlock[succBlock]]])
                else:
                    adj = np.insert(adj, len(adj), [posOfBlock[blockInd], posOfBlock[succBlock]], axis = 0)
            else:
                predBlocks = cfg1.predecessorBlocksWOBackEdges(succBlock) 
                if len(predBlocks) > 1:
                    posSuccBlockX = 0
                    posSuccBlockY = 0
                    for predBlock in predBlocks:
                        posSuccBlockX = pos[posOfBlock[predBlock]][0] + posSuccBlockX
                        if posSuccBlockY > pos[posOfBlock[predBlock]][1] - verticalGap:
                            posSuccBlockY = pos[posOfBlock[predBlock]][1] - verticalGap
                    posSuccBlockX = posSuccBlockX / len(predBlocks)
                    posSuccBlock = [posSuccBlockX, posSuccBlockY]
                    posOfBlock[succBlock] = len(pos)
                    pos = np.insert(pos, len(pos), posSuccBlock, axis = 0)
                    if adj == None:
                        adj = np.array([[posOfBlock[blockInd], posOfBlock[succBlock]]])
                    else:
                        adj = np.insert(adj, len(adj), [posOfBlock[blockInd], posOfBlock[succBlock]], axis = 0)
                    logging.debug ("\t\t Drawn at %d, %d" % (posSuccBlock[0], posSuccBlock[1]))
                    texts.append("%s" % cfg1.listBlocks[succBlock].name)
                    if cfg1.listBlocks[succBlock].isReturning == 1:
                        symbols.append('x')
                    else:
                        symbols.append('o')
                    if succBlock not in q:
                        q.append(succBlock)
                        
                else:
                    parent = predBlocks[0]
                    parentPos = pos[posOfBlock[parent]]
                    posSuccBlock = [parentPos[0], parentPos[1] - verticalGap]
                    posOfBlock[succBlock] = len(pos)
                    pos = np.insert(pos, len(pos), posSuccBlock, axis = 0)
                    if adj == None:
                        adj = np.array([[posOfBlock[blockInd], posOfBlock[succBlock]]])
                    else:
                        adj = np.insert(adj, len(adj), [posOfBlock[blockInd], posOfBlock[succBlock]], axis = 0)
                    logging.debug ("\t\t Drawn at %d, %d" % (posSuccBlock[0], posSuccBlock[1]))
                    texts.append("%s" % cfg1.listBlocks[succBlock].name)
                    if cfg1.listBlocks[succBlock].isReturning == 1:
                        symbols.append('x')
                    else:
                        symbols.append('o')
                    if succBlock not in q:
                        q.append(succBlock)
                    
        else:
            continue
    
    return pos, adj, texts, symbols
    