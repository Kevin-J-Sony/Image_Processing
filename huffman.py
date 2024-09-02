'''
Given the number of symbols of a certain size and the symbols itself, derive the huffman tree for the symbols.
The Huffman code stored is of canonical form in JPEGS, so the tree that can be generated is determined and not ambiguous.
'''

class Node:
    
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        
    def __str__(self):
        
        tree_str = "["
        tree_str += "" if self.left is None else str(self.left)
        tree_str += "" if self.data is None else str(self.data)
        tree_str += "" if self.right is None else str(self.right)
        tree_str += "]"
        
        return tree_str
    
    def __repr__(self):
        return str(self)
    
    def add_new_nodes(self, i):
        if i == 0 and self.data is None:
            self.left = Node()
            self.right = Node()
            return
        if self.left is not None and self.right is not None:
            self.left.add_new_nodes(i - 1)
            self.right.add_new_nodes(i - 1)
    
    '''
    Return the furthest left leaf on the tree
    '''
    def get_free_left_leaf(self):
        if self.left is None and self.right is None and self.data is None:
            return self

        if self.left.is_tree_free():
            return self.left.get_free_left_leaf()
        if self.right.is_tree_free():
            return self.right.get_free_left_leaf()
        

        '''
        # If the left child does not exist, or is occupied by a symbol, it cannot be within the left subtree
        if self.left is None or self.left.data is not None: 
            # If the right child does not exist or is occupied by a symbol, it cannot be within the right subtree
            if self.right is None:
                return self
            else:
                return self.right.get_free_left_leaf()
        # Otherwise, search the left subtree
        else:
            return self.left.get_free_left_leaf()
        '''

    '''
    Auxillary function to the get_free_left_leaf function which determines if the tree has any leaves to fill
    '''
    def is_tree_free(self):
        found = False
        if self.left is None and self.right is None and self.data is None:
            return True

        if self.left is not None:
            found = self.left.is_tree_free()

        if self.right is not None and not found:
            found = found or self.right.is_tree_free()

        return found


class Huffman:
    
    def __init__(self, number_of_codes_of_size, symbols):
        self.nocos = number_of_codes_of_size
        self.symbols = symbols
        
        self.root = Node()
        self.root.left = Node()
        self.root.right = Node()
                
        self.generate_huffman_tree()
        #self.generate_huffman_code()
        self.state = self.root
        
    def __str__(self):
        huffman_tree_str = "huffman tree: " + str(self.root) + "\n"
        return huffman_tree_str

    def generate_huffman_tree(self):
        symbols_processed = 0
        symbol_idx = 0
        for idx in range(1, len(self.nocos)):
            if symbols_processed >= len(self.symbols):
                break
            self.create_new_layer(idx)
            number_of_codes = self.nocos[idx]
            for i in range(number_of_codes):
                left_most_leaf = self.root.get_free_left_leaf()
                left_most_leaf.data = self.symbols[symbol_idx]
                symbol_idx += 1
            symbols_processed += number_of_codes        
    
    def create_new_layer(self, i):
        self.root.add_new_nodes(i)
        ...
    
    def read_code(self, coded_info):
        
        ...
        

if __name__ == "__main__":
    #huff = Huffman([0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    #               ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'])
    huff2 = Huffman([0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    print(huff2)
    #print(huff)
    ...
