#from client import Client
#from request import Request
import queue
from BlockNode import BlockNode
from BlockChain import BlockChain


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
    first_block.add_trans([1, 2, 5])
    first_block.add_trans([1, 4, 8])
    first_block.add_trans([1, 5, 7])
    # a = str(first_block)
    # print(a)
    second_block = BlockNode(2)
    second_block.add_trans([2, 4, 9])
    second_block.add_trans([2, 3, 8])
    second_block.add_trans([2, 1, 6])
    third_block = BlockNode(3)
    third_block.add_trans([3, 1, 2])
    third_block.add_trans([3, 2, 11])
    third_block.add_trans([3, 4, 62])
    #print("0 should be here, the depth is {}".format(block_chain.depth))
    block_chain.insert(first_block)
    #print("after inserting first block, the depth is {}".format(block_chain.depth))
    block_chain.insert(second_block)
    #print("after inserting second block, the depth is {}".format(block_chain.depth))
    #print(block_chain.head.test_int)
    block_chain.discard_last_and_insert_new(third_block)
    #print("Discarded second and inserted the third block, the depth is {}".format(block_chain.depth))
    #print(block_chain.head.test_int)
    #print(block_chain.head.prev.test_int)

    print(block_chain)
    #print(block_chain.head.test_int)