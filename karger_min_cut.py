import sys
import re
import random
import pprint
from copy import deepcopy
from time import perf_counter as pc

class RowVError( Exception ):
    def __init__( self, value ):
        self.value = value
    def __str__( self ):
        return repr( self.value )

def remove_all( row, val ):
    while True:
        try:
            row.remove( val )

        except ValueError:
            break
    return

def find_row( gr, el ):
    for i in range( len( gr ) ):
        if gr[ i ][ 0 ] == el:
            row_v = gr[ i ]
            return( row_v )
    else:
        raise RowVError( el )

def min_cut( graph ):
    # Pick an edge--
    # randomly choose a row
    row_index = random.randrange( len( graph ) )

    # u is first element
    row_u = graph[ row_index ]
    u = row_u[ 0 ]

    # select index for v
    col_index = random.randrange( 1, len( row_u ) )
    v = row_u[ col_index ]

    # find row_v and get a pointer to it then delete it from graph
    row_v = find_row( graph, v )
    graph.remove( row_v )

    # append row_v on to row_u
    row_u += row_v

    # remove all self-loops:  just not first element, which is node;
    # this also deletes the node, u, so put that back afterwards
    remove_all( row_u, u )
    remove_all( row_u, v )
    row_u.insert( 0, u )

    # references to v in the old row_v's adjacent nodes must change to u
    for adj in row_v[1:]:
        adj_row = find_row( graph, adj )
        for i in range( 1, len( adj_row ) ):
            if adj_row[ i ] == v:
                adj_row[ i ] = u

    if len( graph ) == 2:
        return
    else:
        min_cut( graph )

    return

def usage():
    print( 'Usage:' )
    print( 'my_prompt>  python3 karger_min_cut.py <filename>' )
    print( 'my_prompt>  python3 karger_min_cut.py -nsquared <filename>' )
    print( 'my_prompt>  python3 karger_min_cut.py -<loops> <filename>' )

def main():
    graph_st = []
    graph = []
    run_multiple = 0
    theMinimumCut = 0
    loops = 0

    if len( sys.argv ) < 2:
        usage()
        return

    if re.match( '-h', sys.argv[ 1 ] ):
        usage()
        return

    for switch in sys.argv:
        if re.match( '-nsquared', switch ):
            run_multiple = 1
            sys.argv.remove( '-nsquared' )
            break

    for switch in sys.argv:
        m = re.match( '-(\d+)', switch )
        if m:
            loops = int( m.group(1) )
            sw = '-' + str( loops )
            sys.argv.remove( sw )
            break

    inputFileName = sys.argv[ 1 ]

    # read file into an array directly
    with open( inputFileName, 'rt' ) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            graph_st.append( line )

    # convert string graph into integer graph;
    # first element is node; other elements are adjacent nodes
    for line_st in graph_st:
        adjacents = [ int( i ) for i in line_st.split() ]
        graph.append( adjacents )

    # starting graph
    pprint.pprint( graph, width=200 )

    # call min-cut algorithm
    if  loops:
        trials = loops
    elif run_multiple:
        trials = len( graph ) * len( graph )
    else:
        trials = 1

    # time it
    t0 = pc()

    for i in range( trials ):
        trial_graph = deepcopy( graph )
        min_cut( trial_graph )
        currentMin = len( trial_graph[ 0 ] ) - 1
        if i == 0 or currentMin < theMinimumCut:
            theMinimumCut = currentMin

    t1 = pc()

    # the number of edges between the two remaining end point is the min cut

    if trials == 1:
        print( 'graph = {}; minimum cut = {:d}'.format( graph, theMinimumCut ) )
    else:
        print( 'minimum cut = {:d}; elapsed time = {:f}'.format( theMinimumCut, t1 - t0 ) )

    return

if __name__ == '__main__':
    main()
