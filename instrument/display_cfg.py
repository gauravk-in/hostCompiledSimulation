import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from collections import deque
import math

from cfg import *

unmappedColor = "000000"

mappedColors = ["CC4733",
                "BF6600",
                "4C5943",
                "B6EEF2",
                "0000B3",
                "8273E6",
                "592D44",
                "E6B4AC",
                "FFAA00",
                "1D331A",
                "00C2F2",
                "000099",
                "9900E6",
                "FF0044",
                "401D10",
                "593C00",
                "00731F",
                "0D2B33",
                "00008C",
                "75468C",
                "4C0014",     
                "FFA280",
                "B2A700",
                "40FF73",
                "004D73",
                "000080",
                "FF40F2",
                "994D57",
                "4D3E39",
                "6D731D",
                "30BF7C",     
                "368DD9",
                "000066",
                "CC99C2",
                "FF6600",
                "BCBF8F",
                "008C83",
                "003380",
                "101040",
                "FF80D5",
                "FFD9BF",
                "B6F23D",
                "3DF2E6",
                "737899",
                "BFBFFF",
                "E5007A"]

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
        
    def clicked(self, pts):
        print("clicked: %s" % pts)
            
verticalGap = 6
horizontalGap = 16

def display_cfgs(app, cfgISC, cfgObj, windowTitle):
    # Initialization of Qt
    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)
    w = pg.GraphicsWindow()
    w.setWindowTitle(windowTitle)
    
    
    v1 = w.addViewBox()
    v1.setAspectLocked()
    g1 = Graph()
    v1.addItem(g1)
    (pos, adj, texts, symbols, brushes) = draw_cfg(cfg=cfgISC, isISC=1, v=v1)
   
    g1.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts, 
               symbol=symbols, brush=brushes)
    
    v2 = w.addViewBox()
    v2.setAspectLocked()
    g2 = Graph()
    v2.addItem(g2)
    (pos, adj, texts, symbols, brushes) = draw_cfg(cfg=cfgObj, isISC=0, v=v2)
    
    g2.setData(pos=pos, adj=adj, size=1, pxMode=False, text=texts, 
               symbol=symbols, brush=brushes)
                
    app.exec_();


def mk_arrow(pos, adj):
    i = len(adj) - 1
    x1 = pos[adj[i][0]][0]
    y1 = pos[adj[i][0]][1]
    x2 = pos[adj[i][1]][0]
    y2 = pos[adj[i][1]][1]
    if (x2-x1) != 0:
        angle = math.degrees(math.atan(float((y1-y2))/float((x2-x1))))
    else:
        if y1 > y2:
            angle = 270
        else:
            angle = 90
    if x1 < x2:
        angle = angle + 180
    arrow = pg.ArrowItem(angle=angle, headLen=17)
    arrow.setPos((x1+x2)/2, (y1+y2)/2)
    return arrow


def mk_edge(adj, startBlockInd, endBlockInd, posOfBlock):
    if adj == None:
        adj = np.array([[posOfBlock[startBlockInd], posOfBlock[endBlockInd]]])
    else:
        adj = np.insert(adj, len(adj), 
                        [posOfBlock[startBlockInd], posOfBlock[endBlockInd]], 
                        axis = 0)
    return adj


def mk_brush(brushes, cfg, blockInd, isISC):
    if cfg.listBlocks[blockInd].mapsTo:
        if isISC == 1:
            brushes.append(pg.mkBrush(mappedColors[cfg.listBlocks[blockInd].mapsTo[0]]))
        else:
            brushes.append(pg.mkBrush(mappedColors[blockInd]))
    else:
        brushes.append(pg.mkBrush(unmappedColor))


def mk_symbol(symbols, cfg, blockInd):
    if cfg.listBlocks[blockInd].isReturning == 1:
        symbols.append('x')
    else:
        symbols.append('o')


ellipseRadius = 1
def mk_selfEdge(pos, blockInd, posOfBlock, v):
    posBlock = pos[posOfBlock[blockInd]]
    cx = posBlock[0]
    cy = posBlock[1]
    selfEdge = pg.CircleROI([cx, cy-ellipseRadius],
                            [2*ellipseRadius, 2*ellipseRadius],
                            movable=False)
    listHandles = selfEdge.getHandles()
    v.addItem(selfEdge)
    pg.CircleROI.removeHandle(selfEdge, listHandles[0])
    

def draw_cfg(cfg, isISC, v):
    logging.debug ("Inside Function draw_cfg()")
    '''
    Breadth first search for all blocks in the Control Flow Graph to print them
    on screen.
    '''
    posOfBlock = {}
    brushes = []
    texts=[]
    
    posOfBlock[0] = 0
    pos = np.array([[0, 0]])
    mk_brush(brushes, cfg, 0, isISC)
    symbols = ['+']
    texts.append(cfg.listBlocks[0].name)
    adj = None
    
    # Queue for BFS
    q = deque([0])
    while q:
        '''
        Breadth First Traversal of the graph, to generate visualization.
        
        Algorithm:
        0. For each node, we add an entry to the 'pos' array for its position. 
            We add an entry in the 'adj' array for each edge. 'texts' array
            contains the text associated with each node ie. the name of the
            node. Symbols array is the symbol for each node. The root node has
            '+' symbol, and the return node has 'x'. All other nodes have 'o'.
            'brushes' array contains the color for each node, which indicates
            mapping between the ISC and Objdump graphs.
        0.a Global variables 'verticalGap' and 'horizontalGap' are distances
            between nodes.
        0.b 'posOfBlock' is a dictionary mapping between block index and index
            of the block in the 'pos' array.
        1. Outside the loop, the starting node (index 0) is already plotted at
            (0, 0). The block is then added to the queue of pending blocks 'q'
        2. Pop a block index from 'q' in 'blockInd'. 
        3. If current node has more than one successor, for each successor
            a. If it has an edge to itself ie. successor is same as blockInd
                TODO
            b. If successor is in 'posOfBlock' ie. block has already been plot,
                1. create an edge from 'blockInd' to 'succBlock'.
                2. create an arrow for the edge.
                3. continue to next succBlock
            c. else, (if 'succBlock' is not in 'posOfBlock')
                1. Find a parent of the block.
                2. Compute position of successor block from position of its 
                    parent. Add an entry to the 'pos' array.
                3. Add an entry to 'brushes' array for color of the edge.
                4. Add an entry to 'texts' array for name of the edge.
                5. Add an entry to 'symbols' array for symbol of the edge.
                6. Create an edge from 'blockInd' to 'succBlock'.
                7. Create an arrow for the edge.
                8. Add 'succBlock' to 'q', if not already present.
                9. continue to next successor block.
        4. else if, current node has only one successor.
            -> Only one successor should not generally be a self edge, so
                so ignoring check.
            a. If 'succBlock' is in 'posOfBlock'
                1. Create an edge from 'blockInd' to 'succBlock'.
                2. Create an arrow for the edge.
                3. continue to next entry in the queue of pending nodes.
            b. else, if 'succBlock' not in 'posOfBlock'
                1. Find position for succBlock,
                    a. if succBlock has more than one predessors (parents), the
                        position of the block will be between the parents.
                    b. If it has only one parent, the position will be directly
                        below the parent.
                2. Add entry to 'pos' array for position of successor block.
                3. Add entry to 'brushes' array for color of the block.
                4. Add entry to 'texts' array for name of the block.
                5. Add entry to 'symbols' array for symbol of the block.
                6. Create an edge from 'blockInd' to 'succBlock'
                7. Create an arrow for the edge.
                8. Add 'succBlock' to 'q' if not already present.
                9. continue to next entry in the queue of pending blocks
        '''
        
        # Algo 2. Pop next block from the queue
        blockInd = q.popleft()
        logging.debug ("Block %d" % blockInd)
        # Find all children of the blockInd
        succBlocks = cfg.successorBlocks(blockInd)
        spaceForChildren = (len(succBlocks) - 1) * horizontalGap
        logging.debug ("\t has %d children, space = %d" % (len(succBlocks), spaceForChildren))
        
        # Algo 3.
        if len(succBlocks) > 1:
            # Algo 3. number of successors is more than 1
            i = 0 # index for each successor block
            for succBlock in succBlocks:
                
                if succBlock == blockInd:
                    # 3.a. Self Edge
                    mk_selfEdge(pos, blockInd, posOfBlock, v)
                    continue
                
                logging.debug ("\t Successor Block %d" % succBlock)
                if succBlock in posOfBlock:
                    # 3.b. Successor has already been plot
                    logging.debug ("\t\t Already drawn at %d, %d" % (pos[posOfBlock[succBlock]][0], pos[posOfBlock[succBlock]][1]))
                    adj = mk_edge(adj, blockInd, succBlock, posOfBlock)
                    arrow = mk_arrow(pos, adj)
                    v.addItem(arrow)
                    continue
                else:
                    # 3.c. Successor has not yet been plotted
                    parent = None
                    for predBlock in cfg.predecessorBlocks(succBlock):
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
                    mk_brush(brushes, cfg, succBlock, isISC)
                    texts.append("%s" % cfg.listBlocks[succBlock].name)
                    mk_symbol(symbols, cfg, succBlock)
                    adj = mk_edge(adj, blockInd, succBlock, posOfBlock)
                    arrow = mk_arrow(pos, adj)
                    v.addItem(arrow)
                    logging.debug ("\t\t Drawn at %d, %d" % (posSuccBlock[0], posSuccBlock[1]))
                    if succBlock not in q:
                        q.append(succBlock)
                    i = i + 1
                    continue
        
        # 4. Only one successor
        elif len(succBlocks) == 1:
            succBlock = succBlocks[0]
            logging.debug ("\t Successor Block %d" % succBlock)
            if succBlock in posOfBlock:
                # 4.a. Successor has already been plotted
                logging.debug ("\t\t Already drawn at %d, %d" % (pos[posOfBlock[succBlock]][0], pos[posOfBlock[succBlock]][1]))
                adj = mk_edge(adj, blockInd, succBlock, posOfBlock)
                arrow = mk_arrow(pos, adj)
                v.addItem(arrow)
                continue
            else:
                # 4.c. Successor has not yet been plotted
                predBlocks = cfg.predecessorBlocks(succBlock)

                if len(predBlocks) > 1:
                    posSuccBlockX = 0
                    posSuccBlockY = 0
                    for predBlock in predBlocks:
                        if predBlock in posOfBlock:
                            posSuccBlockX = pos[posOfBlock[predBlock]][0] + posSuccBlockX
                            if posSuccBlockY > pos[posOfBlock[predBlock]][1] - verticalGap:
                                posSuccBlockY = pos[posOfBlock[predBlock]][1] - verticalGap
                    posSuccBlockX = posSuccBlockX / len(predBlocks)
                    posSuccBlock = [posSuccBlockX, posSuccBlockY]
                else:
                    parent = predBlocks[0]
                    parentPos = pos[posOfBlock[parent]]
                    posSuccBlock = [parentPos[0], parentPos[1] - verticalGap]
                    
                posOfBlock[succBlock] = len(pos)
                pos = np.insert(pos, len(pos), posSuccBlock, axis = 0)
                mk_brush(brushes, cfg, succBlock, isISC)
                adj = mk_edge(adj, blockInd, succBlock, posOfBlock)
                arrow = mk_arrow(pos, adj)
                v.addItem(arrow)
                logging.debug ("\t\t Drawn at %d, %d" % (posSuccBlock[0], posSuccBlock[1]))
                texts.append("%s" % cfg.listBlocks[succBlock].name)
                mk_symbol(symbols, cfg, succBlock)
                if succBlock not in q:
                    q.append(succBlock)
                    
        else:
            continue
    
    if adj==None:
        adj = np.array([[0, 0]])
    return pos, adj, texts, symbols, brushes
    