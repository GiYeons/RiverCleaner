import math as m

# Define Node. key는 total_trash
class Node():
    def __init__(self, num, latitude=0., longitude=0., rubbish=0, plastics=0, cans=0, glass=0, paper=0):
        self.total_trash = rubbish + plastics + cans + glass + paper      # key로 사용
        self.key = self.total_trash

        self.latitude = m.floor(latitude*10)/10    # 원래 내림이 하고 싶었는데 안돼서 임시방편.. 어차피 데이터 전처리에서
        self.longitude = m.floor(longitude*10)/10  # 2자리까지 자를것임

        self.rubbish = rubbish
        self.plastics = plastics
        self.cans = cans
        self.glass = glass
        self.paper = paper

        self.num = num                                   # 노드 구분을 위한 임의의 번호
        self.parent = None                               # Parent of Node
        self.left = None                                 # Left Child of Node
        self.right = None                                # Right Child of Node
        self.color = 1                                   # Red Node as new node is always inserted as Red Node

# Define R-B Tree
class RBTree():
    def __init__(self):
        self.NULL = Node ( 0 )
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL


    # Insert New Node
    def insertNode(self, num, latitude=0., longitude=0., rubbish=0, plastics=0, cans=0, glass=0, paper=0):
        node = Node(num, latitude, longitude, rubbish, plastics, cans, glass, paper)
        node.parent = None
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1                                   # Set root colour as Red

        y = None
        x = self.root

        while x != self.NULL :                           # Find position for new node
            y = x
            if node.key < x.key :
                x = x.left
            else :
                x = x.right

        node.parent = y                                  # Set parent of Node as y
        if y == None :                                   # If parent i.e, is none then it is root node
            self.root = node
        elif node.key < y.key :                          # Check if it is right Node or Left Node by checking the value
            y.left = node
        else :
            y.right = node

        if node.parent == None :                         # Root node is always Black
            node.color = 0
            return

        if node.parent.parent == None :                  # If parent of node is Root Node
            return

        self.fixInsert ( node )                          # Else call for Fix Up


    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.NULL:
            node = node.right
        return node

    # Code for left rotate
    def LR ( self , x ) :
        y = x.right                                      # Y = Right child of x
        x.right = y.left                                 # Change right child of x to left child of y
        if y.left != self.NULL :
            y.left.parent = x

        y.parent = x.parent                              # Change parent of y as parent of x
        if x.parent == None :                            # If parent of x == None ie. root node
            self.root = y                                # Set y as root
        elif x == x.parent.left :
            x.parent.left = y
        else :
            x.parent.right = y
        y.left = x
        x.parent = y


    # Code for right rotate
    def RR ( self , x ) :
        y = x.left                                       # Y = Left child of x
        x.left = y.right                                 # Change left child of x to right child of y
        if y.right != self.NULL :
            y.right.parent = x

        y.parent = x.parent                              # Change parent of y as parent of x
        if x.parent == None :                            # If x is root node
            self.root = y                                # Set y as root
        elif x == x.parent.right :
            x.parent.right = y
        else :
            x.parent.left = y
        y.right = x
        x.parent = y


    # Fix Up Insertion
    def fixInsert(self, k):
        while k.parent.color == 1:                        # While parent is red
            if k.parent == k.parent.parent.right:         # if parent is right child of its parent
                u = k.parent.parent.left                  # Left child of grandparent
                if u.color == 1:                          # if color of left child of grandparent i.e, uncle node is red
                    u.color = 0                           # Set both children of grandparent node as black
                    k.parent.color = 0
                    k.parent.parent.color = 1             # Set grandparent node as Red
                    k = k.parent.parent                   # Repeat the algo with Parent node to check conflicts
                else:
                    if k == k.parent.left:                # If k is left child of it's parent
                        k = k.parent
                        self.RR(k)                        # Call for right rotation
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.LR(k.parent.parent)
            else:                                         # if parent is left child of its parent
                u = k.parent.parent.right                 # Right child of grandparent
                if u.color == 1:                          # if color of right child of grandparent i.e, uncle node is red
                    u.color = 0                           # Set color of childs as black
                    k.parent.color = 0
                    k.parent.parent.color = 1             # set color of grandparent as Red
                    k = k.parent.parent                   # Repeat algo on grandparent to remove conflicts
                else:
                    if k == k.parent.right:               # if k is right child of its parent
                        k = k.parent
                        self.LR(k)                        # Call left rotate on parent of k
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.RR(k.parent.parent)              # Call right rotate on grandparent
            if k == self.root:                            # If k reaches root then break
                break
        self.root.color = 0                               # Set color of root as black


    # Function to fix issues after deletion
    def fixDelete ( self , x ) :
        while x != self.root and x.color == 0 :           # Repeat until x reaches nodes and color of x is black
            if x == x.parent.left :                       # If x is left child of its parent
                s = x.parent.right                        # Sibling of x
                if s.color == 1 :                         # if sibling is red
                    s.color = 0                           # Set its color to black
                    x.parent.color = 1                    # Make its parent red
                    self.LR ( x.parent )                  # Call for left rotate on parent of x
                    s = x.parent.right
                # If both the child are black
                if s.left.color == 0 and s.right.color == 0 :
                    s.color = 1                           # Set color of s as red
                    x = x.parent
                else :
                    if s.right.color == 0 :               # If right child of s is black
                        s.left.color = 0                  # set left child of s as black
                        s.color = 1                       # set color of s as red
                        self.RR ( s )                     # call right rotation on x
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0                    # Set parent of x as black
                    s.right.color = 0
                    self.LR ( x.parent )                  # call left rotation on parent of x
                    x = self.root
            else :                                        # If x is right child of its parent
                s = x.parent.left                         # Sibling of x
                if s.color == 1 :                         # if sibling is red
                    s.color = 0                           # Set its color to black
                    x.parent.color = 1                    # Make its parent red
                    self.RR ( x.parent )                  # Call for right rotate on parent of x
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0 :
                    s.color = 1
                    x = x.parent
                else :
                    if s.left.color == 0 :                # If left child of s is black
                        s.right.color = 0                 # set right child of s as black
                        s.color = 1
                        self.LR ( s )                     # call left rotation on x
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.RR ( x.parent )
                    x = self.root
        x.color = 0


    # Function to transplant nodes
    def __rb_transplant ( self , u , v ) :
        if u.parent == None :
            self.root = v
        elif u == u.parent.left :
            u.parent.left = v
        else :
            u.parent.right = v
        v.parent = u.parent


    # Function to handle deletion
    def delete_node_helper ( self , node , key ) :
        z = self.NULL
        while node != self.NULL :                          # Search for the node having that value/ key and store it in 'z'
            if node.key == key :
                z = node

            if node.key <= key :
                node = node.right
            else :
                node = node.left

        if z == self.NULL :                                # If Kwy is not present then deletion not possible so return
            print ( "Value not present in Tree !!" )
            return

        y = z
        y_original_color = y.color                          # Store the color of z- node
        if z.left == self.NULL :                            # If left child of z is NULL
            x = z.right                                     # Assign right child of z to x
            self.__rb_transplant ( z , z.right )            # Transplant Node to be deleted with x
        elif (z.right == self.NULL) :                       # If right child of z is NULL
            x = z.left                                      # Assign left child of z to x
            self.__rb_transplant ( z , z.left )             # Transplant Node to be deleted with x
        else :                                              # If z has both the child nodes
            y = self.minimum ( z.right )                    # Find minimum of the right sub tree
            y_original_color = y.color                      # Store color of y
            x = y.right
            if y.parent == z :                              # If y is child of z
                x.parent = y                                # Set parent of x as y
            else :
                self.__rb_transplant ( y , y.right )
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant ( z , y )
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0 :                          # If color is black then fixing is needed
            self.fixDelete ( x )


    # Deletion of node
    def delete_node ( self , total_trash ) :
        self.delete_node_helper ( self.root , total_trash )         # Call for deletion


    # Function to print
    def __printCall ( self , node , indent , last ) :
        if node != self.NULL :
            print(indent, end=' ')
            if last :
                print ("R----",end= ' ')
                indent += "     "
            else :
                print("L----",end=' ')
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print ( str ( node.key ) + "(" + s_color + ")" )
            self.__printCall ( node.left , indent , False )
            self.__printCall ( node.right , indent , True )

    # Function to call print
    def print_tree ( self ) :
        self.__printCall ( self.root , "" , True )

    # max node 정보 리턴
    def get_max(self):
        node = self.maximum(self.root)
        return  node.total_trash, node.latitude, node.longitude

    def isEmpty(self):
        return self.root == self.NULL

# TEST
if __name__ == "__main__":
    bst = RBTree()

    bst.insertNode(1, latitude=37.58, longitude=127.01, rubbish=5, plastics=3, cans=1, glass=0, paper=1)
    bst.insertNode(2, latitude=37.58, longitude=127.02, rubbish=2, plastics=1, cans=1, glass=0, paper=3)
    bst.insertNode(3, latitude=37.51, longitude=126.87, rubbish=9, plastics=3, cans=1, glass=0, paper=3)
    bst.insertNode(4, latitude=37.58, longitude=127.04, rubbish=1, plastics=2, cans=1, glass=0, paper=0)

    bst.print_tree()

    print("\nAfter deleting an element")
    bst.delete_node(7)
    bst.print_tree()