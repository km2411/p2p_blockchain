import random
import simpy
import sys
from peer import  Peer
import manager

# No. of peers
n = int(sys.argv[1])
SIM_DURATION = 1/100
Mbits = 1000000
#VISUALIZATION = False
VISUALIZATION = True

def initializePeer(peer_id, peer_type, env):
    return Peer(peer_id, peer_type, env)
    
def createPeers(peer_server, numOfPeers):
    peers = []
    # set z 
    z = 50
    for i in range(numOfPeers):
        if i < int(numOfPeers * (z / 100)):
            p = initializePeer('p%d' % i, 'slow', env)
        else:
            p = initializePeer('p%d' % i, 'fast', env)

        #p.connect(peer_server)
        peers.append(p)
    
    # set DSL bandwidth
    for p in peers:
        for other in peers:
            prob = random.randint(0,1)
            if prob:
                p.connect(other)
        
        #manager = manager(p)
        #manager.simulate()

        #print "peer connections";
        #print p.name;
        #print " "
        #print p.connections
        if p.type == 'slow':
            p.bandwidth_upload = p.bandwidth_download = 5 * Mbits
        else:
            p.bandwidth_upload = p.bandwidth_download = 100 * Mbits

    return peers

env = simpy.Environment()

#make a peer server, a boot node which is slow in nature
pserver = initializePeer('PeerServer', 'slow', env)
pserver.bandwidth_upload = pserver.bandwidth_download = 5 * Mbits

#intilize the distributions
#dist to select number of connections for a peer 
global peers 
peers = createPeers(pserver, n)

peers_gen = []
for p in peers:
    peers_gen.append(p.run())

for i in range(10):
    for p in peers_gen:
        print p

print("Starting Simulator")
if VISUALIZATION:
    from animate import Visualizer
    Visualizer(env, peers)
else:
    env.run(until=SIM_DURATION)
