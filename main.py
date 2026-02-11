import heapq 
# as min_heap_esque_queue #for A*

#test cases from the slides
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

eight_goal_state = [[1,2,3],
                    [4,5,6],
                    [7,8,0]]

#problem
# solution = uniform_search(easy)



#represents the state of the puzzle, lower cost in priority queue
class Node:
    def __init__(self,state,parent=None, action=None, cost=0, depth=0, heuristic=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.cost=cost #g(n)
        self.heuristic=heuristic #h(n)
        self.depth=depth
        
    def f(self):
        return self.cost + self.heuristic
        
    def __lt__(self,other):
        return self.f() < other.f()
        
class Eight_Puzzle:
        
#goal test   
    def __init__(self,initial_state):
        self.initial_state=initial_state
        self.goal_state=eight_goal_state 
        
    def is_goal(self, state):
        return state == self.goal_state
    
    def successors(self,state):
        successors=[]
    
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
    
        for action, (dr,dc) in moves.items():
            new_row=zero_row+dr
            new_col=zero_col+dc
            if 0<= new_row < 3 and 0 <= new_col < 3:
                new_state=[row.copy() for row in state]
                # new_state=state.copy()
                
                new_state[zero_row][zero_col],new_state[new_row][new_col]=\
                    new_state[new_row][new_col],new_state[zero_row][zero_col]
                #step cost = 1
                successors.append((action,new_state,1))     
        return successors   

#create child nodes (all possible next moves from curr node)
def expand(node, problem, heuristic_fn=None):
    children=[]
    for action, next_state, step_cost in problem.successors(node.state):
        h = heuristic_fn(next_state) if heuristic_fn else 0
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

#a*
def a_star(problem, heuristic_fn=None):
    open_queue= []
    
    h= heuristic_fn(problem.initial_state) if heuristic_fn else 0
    
    start_node = Node(
        state=problem.initial_state,
        parent=None,
        action=None,
        cost=0,
        heuristic=h,
        depth=0
    )

    heapq.heappush(open_queue,start_node)
    visited= set()
    node_expanded=0
    max_queue_size=0
    
    while open_queue:
        max_queue_size=max(max_queue_size, len(open_queue))
        current = heapq.heappop(open_queue)
        
        #goal test, see if you reached it
        if problem.is_goal(current.state):
            print("Number of nodes expanded: ", node_expanded)
            print("Max queue size: ",max_queue_size)
            print("Depth of solution:",current.depth)
            return current
        
        current_tuple = tuple(tuple(row) for row in current.state)
        visited.add(current_tuple)
        
        #use the expand function
        for child in expand(current,problem,heuristic_fn):
            child_tuple=tuple(tuple(row) for row in child.state)
            if child_tuple not in visited:
                heapq.heappush(open_queue,child)        
        node_expanded+=1
        
    return None
    
    
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
        a_star(problem,None)
    elif algorithm == "2":
        a_star(problem,misplaced_tile)
    elif algorithm == "3":
        a_star(problem,manhattan_distance)
    else:
        print("Invalid choice.")


def main():
    puzzle_mode= input("Welcome to the 8 puzzle! Select '1' for a default puzzle. Select '2' to create your own." 
                       + '\n')
    if puzzle_mode == '1':
        # choose_algorithm(default_puzzle_mode())
        puzzle_list=default_puzzle_mode()
        problem=Eight_Puzzle(puzzle_list)
        choose_algorithm(problem)
        
        # select...
    if puzzle_mode == '2':
        print("Enter your custom puzzle, using zero to represent the blank." +
              "Please only enter whole numbers from 0-8. Add a space in between the numbers." +
              "Press ENTER when done.")
        puzzle_first_row=input("Enter the first row: ")
        puzzle_second_row=input("Enter the second row: ")
        puzzle_third_row=input("Enter the third row: ")
        
        puzzle_first_row=puzzle_first_row.split()
        puzzle_second_row=puzzle_second_row.split()
        puzzle_third_row=puzzle_third_row.split()
        
        for i in range(0,3):
            puzzle_first_row[i]=int(puzzle_first_row[i])
            puzzle_second_row[i]=int(puzzle_second_row[i])
            puzzle_third_row[i]=int(puzzle_third_row[i])
            
        user_puzzle=[puzzle_first_row,puzzle_second_row,puzzle_third_row]
        choose_algorithm(user_puzzle)
    return


if __name__ == "__main__":
    main()
    
#print puzzle in 3x3 form
def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')

# driver
def general_search(problem, queue_function):
    nodes= queue_function.make_queue(Node(problem.initial_state))
    # explored
    best_cost={}
    
    while True:
        if queue_function.is_empty(nodes):
            return "Failed. There are no nodes"
        node= queue_function.remove_front(nodes)
        
        if node.state in best_cost and best_cost[node.state] <= node.cost:
            continue
        best_cost[node.state] = node.cost
        
        if problem.goal_test(node.state):
            return node
        children=expand(node,problem)
        nodes=queue_function.insert_all(nodes,children)
        
        
        