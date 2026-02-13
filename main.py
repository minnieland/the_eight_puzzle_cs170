import heapq 
#for A*

#test cases from the slides, 2d list
#depth_zero / intital state
easy =        [[1,2,3],
               [4,5,6],
               [7,8,0]]

#depth_2 
medium =    [[1,2,3],
            [4,5,6],
            [0,7,8]]

#depth_4 
hard =      [[1,2,3],
            [5,0,6],
            [4,7,8]]

#goal state for 8-puzzle
eight_goal_state = [[1,2,3],
                    [4,5,6],
                    [7,8,0]]



#represents the state of the puzzle, lower cost in priority queue
class Node:
    def __init__(self,state,parent=None, action=None, cost=0, depth=0, heuristic=0):
        self.state=state #current puzzle config
        self.parent=parent #keep parent for path tracing
        self.action=action #moves to reach curr state
        self.cost=cost #g(n) cost from start to curr node
        self.heuristic=heuristic #h(n), calculated or hardcoded to 0
        self.depth=depth
    
    #f(n)=g(n)+h(n) is the total cost when using each algo    
    def f(self):
        return self.cost + self.heuristic
    #lower f(n) cost means better path to goal using A*    
    def __lt__(self,other):
        return self.f() < other.f()
        
class Eight_Puzzle:
        
    def __init__(self,initial_state):
        self.initial_state=initial_state
        self.goal_state=eight_goal_state 
        
#goal test, check if curr is equal to goal state
    def is_goal(self, state):
        return state == self.goal_state
    
    #generate all successors from curr
    def successors(self,state):
        successors=[]
        #find blank tile, where tile value = 0
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    zero_row, zero_col = r, c
                    break
        #moves
        moves = {
            'U':(-1,0),
            'D':(1,0),
            'R':(0,1),
            'L':(0,-1)
        }
    
        #try all moves possible
        for action, (dr,dc) in moves.items():
            new_row=zero_row+dr
            new_col=zero_col+dc
            
            #make sure new position is in bounds
            if 0<= new_row < 3 and 0 <= new_col < 3:
                new_state=[row.copy() for row in state] #copy the state
                
                #swap blank with adjacent tile
                new_state[zero_row][zero_col],new_state[new_row][new_col]=\
                    new_state[new_row][new_col],new_state[zero_row][zero_col]
                #step cost = 1, add to sucessory list 
                successors.append((action,new_state,1))   
                  
        return successors   

#create child nodes (all possible next moves from curr node)
def expand(node, problem, heuristic_fn=None):
    children=[]
    #get all possible next states
    for action, next_state, step_cost in problem.successors(node.state):
       #calculate heursitic, if there isnt any, set it to zero / uniform cost
        h = heuristic_fn(next_state) if heuristic_fn else 0
        #make a childnode
        child = Node(
            state=next_state,
            parent=node,
            action=action,
            cost=node.cost + step_cost, #total cost
            heuristic=h,
            depth=node.depth+1
            
            )
        children.append(child)
    return children

# driver
def general_search(problem, queue_function):
    #starting node from starting state
    initial_node=Node(
        state=problem.initial_state,
        parent=None,
        action=None,
        cost=0,
        depth=0,
        heuristic=0
    )    
    #queue is initiated with starting node
    nodes= [initial_node]
    nodes=queue_function(nodes,None,problem)
    
    nodes_expanded = 0
    max_queue_size=1
    visited = set()
    
    while True:
        #if empty nodes, no solution found
        if not nodes:
            return "Failed. There are no nodes"
        
        max_queue_size=max(max_queue_size,len(nodes))
        node=nodes.pop(0) #pop the first node from queue as its sorted by highest prio
        
        #curr state is marked visited
        node_tuple = tuple(tuple(row) for row in node.state)
        if node_tuple in visited: continue
        #skip if state is visited already
        visited.add(node_tuple)
        
        #check if we reached goal state
        if problem.is_goal(node.state):
            print("Numbers of nodes expanded:", nodes_expanded)
            print("Max queue size:", max_queue_size)
            print("Depth of solution:", node.depth)
            return node
        #expand current node and all children     
        nodes=queue_function(nodes, node, problem)
        nodes_expanded+=1

def a_star_queue(heuristic_fn):
    def queue_function(nodes,node,problem):
        if node is None:
            nodes[0].heuristic=heuristic_fn(nodes[0].state)
            return nodes
        children=expand(node,problem,heuristic_fn)
        nodes.extend(children)
        nodes.sort(key=lambda n:n.f())
        
        return nodes
    return queue_function
        
        
def uniform_cost(nodes,node,problem):
    if node is None:
        return nodes
    children = expand(node, problem, heuristic_fn=None)
    
    nodes.extend(children)
    nodes.sort(key=lambda n: n.cost)
    return nodes

#how far away is each tile from its goal pos (sum)
def manhattan_distance(state):
    distance=0
    
    #make goal postitions from eight_goal_state
    goal_positions={}
    for row in range(3):
        for column in range(3):
            tile=eight_goal_state[row][column]
            goal_positions[tile]=(row,column)
            
    #calc manhattan for each tile
    for row in range(3):
        for column in range(3):
            tile=state[row][column]
            if tile !=0: #count all tiles but the blank
                goal_row,goal_column=goal_positions[tile]
                #equation =|x1 - x2| + |y1 - y2|
                distance+=abs(row-goal_row)+abs(column-goal_column)
    return distance

#counts how many tiles are wrong positions
def misplaced_tile(state):
    goal= eight_goal_state
    misplaced=0
    
    #in the 3x3 check the positions of each 
    for row in range(3):
        for column in range(3):
            #count the tile only if its not the blank and in an incorrect position from goal
            if state[row][column] != 0 and state[row][column] != goal[row][column]:
                misplaced +=1
    return misplaced

#a*
# def a_star(problem, heuristic_fn=None):
    open_queue= [] #priorty queue
    #calculate heursitic, if there isnt any, set it to zero / uniform cost
    h= heuristic_fn(problem.initial_state) if heuristic_fn else 0
    #make a start node
    start_node = Node(
        state=problem.initial_state,
        parent=None,
        action=None,
        cost=0,
        heuristic=h,
        depth=0
    )
    #start node goes into prio queue
    heapq.heappush(open_queue,start_node)
    visited= set()  #set of explored
    node_expanded=0
    max_queue_size=0
    
    while open_queue:
        max_queue_size=max(max_queue_size, len(open_queue))
        current = heapq.heappop(open_queue) #get node with lowkey f(n) cost
        
        #goal test, see if you reached it
        if problem.is_goal(current.state):
            print("Number of nodes expanded:", node_expanded)
            print("Max queue size:",max_queue_size)
            print("Depth of solution:",current.depth) #not needed but easier for testing
            return current
        #curr state is marked visited
        current_tuple = tuple(tuple(row) for row in current.state)
        visited.add(current_tuple)
        
        #use the expand function on curr node, children are added to queue
        for child in expand(current,problem,heuristic_fn):
            child_tuple=tuple(tuple(row) for row in child.state)
            if child_tuple not in visited:
                heapq.heappush(open_queue,child)        
        node_expanded+=1
        
    return "No solution is found."
    
    
#puzzles to test already embedded in the system
def default_puzzle_mode():
    difficulty_level= input("Select the difficulty level from 0-2" + '\n')
    if difficulty_level=="0":
        print("difficulty [easy] selected" + "\n")
        return easy
    elif difficulty_level=="1":
        print("difficulty [medium] selected"+ "\n")
        return medium
    elif difficulty_level=="2":
        print("difficulty [hard] selected"+ "\n")
        return hard
    else: 
        print("Difficulty not availiable."+ "\n")
        return None
        


#bfs depending on which prio queue you want
#computing prio = g(n) + h(n)
def choose_algorithm(problem):
    algorithm= input("Select an algorithm:\n"
                     "[1] Uniform Cost\n"
                     "[2] Misplaced Tile Heuristic\n"
                     "[3] Manhattan Distance Heuristic\n"
                    )
    if algorithm == "1":
        # a_star(problem,None)
        general_search(problem,uniform_cost)
    elif algorithm == "2":
        # a_star(problem,misplaced_tile)
        general_search(problem,a_star_queue(misplaced_tile))
    elif algorithm == "3":
        # a_star(problem,manhattan_distance)
        general_search(problem,a_star_queue(manhattan_distance))
    else:
        print("Invalid choice.")
        return

#print puzzle in 3x3 form
def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')


def main():
    puzzle_mode= input("Welcome to the 8 puzzle! Select '1' for a default puzzle. Select '2' to create your own." 
                       + '\n')
    if puzzle_mode == '1':
        # choose_algorithm(default_puzzle_mode())
        puzzle_list=default_puzzle_mode()
        
        print_puzzle(puzzle_list)
        
        problem=Eight_Puzzle(puzzle_list)
        choose_algorithm(problem)
        
        # select and enter own custom puzzle
    if puzzle_mode == '2':
        print("Enter your custom puzzle, using zero to represent the blank." +
              "Please only enter whole numbers from 0-8. Add a space in between the numbers." +
              "Press ENTER when done.")
        
        puzzle_first_row=input("Enter the first row: ")
        puzzle_second_row=input("Enter the second row: ")
        puzzle_third_row=input("Enter the third row: ")
        
        #split input strings into lists
        puzzle_first_row=puzzle_first_row.split()
        puzzle_second_row=puzzle_second_row.split()
        puzzle_third_row=puzzle_third_row.split()
        
        #convert strings to int
        for i in range(0,3):
            puzzle_first_row[i]=int(puzzle_first_row[i])
            puzzle_second_row[i]=int(puzzle_second_row[i])
            puzzle_third_row[i]=int(puzzle_third_row[i])
        
        #turn into 2d list
        user_puzzle=[puzzle_first_row,puzzle_second_row,puzzle_third_row]
        print_puzzle(user_puzzle)
        problem=Eight_Puzzle(user_puzzle)
        choose_algorithm(problem)
        
    return

if __name__ == "__main__":
    main()
    

        
        