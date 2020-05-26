from client import Client
#from request import Request
import queue
from Util import *


if __name__ == '__main__':
    # p1_ballot = Ballot(0,0,0)
    # p1_ballot.seq_num += 1
    # print(p1_ballot.seq_num)

    # test BlockNode funtionalities
    # init_block = None
    # first_block = BlockNode(init_block,1)
    # second_block = BlockNode(first_block,2)
    # third_block = BlockNode(second_block,3)
    # print("0 test value is: {}".format(first_block.prev.test_int))
    # print("second test value is: {}".format(third_block.prev.test_int))

    # test BlockChain
    block_chain = BlockChain()
    first_block = BlockNode(1)
    second_block = BlockNode(2)
    third_block = BlockNode(3)
    block_chain.insert(first_block)
    block_chain.insert(second_block)
    #print(block_chain.head.test_int)
    block_chain.discard_last_and_insert_new(third_block)
    #print(block_chain.head.test_int)
    #print(block_chain.head.prev.test_int)

    print(block_chain)
    #print(block_chain.head.test_int)