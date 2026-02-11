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

#moves
moves = {
    'U':(-1,0),
    'D':(1,0),
    'R':(0,1),
    'L':(0,-1)
}

#represents the state of the puzzle, lower cost in priority queue
class Node:
    def __init__(self,state,parent=None, action=None, cost=0, depth=0, heuristic=0):
        self.state=state
        self.parent=parent,
        self.action=action,
        self.cost=cost, #g(n)
        self.heuristic=heuristic, #h(n)
        self.depth=depth
        
        def f(self):
            return self.cost + self.heuristic
        
        def __lt__(self,other):
            return self.f() < other.f()
        
#goal test   
def __init__(self,initial_state):
    self.initial_state=initial_state
    self.goal_state=eight_goal_state 
        
def goal_test(self, state):
    return state == self.goal_state


def main():
    puzzle_mode= input("Welcome to the 8 puzzle! Select '1' for a default puzzle. Select '2' to create your own." 
                       + '\n')
    if puzzle_mode == '1':
        choose_algorithm(default_puzzle_mode())
        # select...
    # if puzzle_mode == '2':
        #do tmr
    
        return

if __name__ == "__main__":
    main()
    
#puzzles to test already embedded in the system
def default_puzzle_mode():
    difficulty_level= input("Select the difficulty level from 0-3" + '\n')
    if difficulty_level=="0":
        print("difficulty [easy] selected")
        return easy
    if difficulty_level=="1":
        print("difficulty [medium] selected")
        return medium
    if difficulty_level=="3":
        print("difficulty [hard] selected")
        return hard
        

#bfs depending on which prio queue you want
#computing prio = g(n) + h(n)
def choose_algorithm(puzzle):
    algorithm= input("Select an algorithm:\n"
                     "[1] Uniform Cost\n"
                     "[2] Misplaced Tile Heuristic\n"
                     "[3] Manhattan Distance Heuristic\n"
                    )
    if algorithm == "1":
        a_star(puzzle,0)
    if algorithm == "2":
        a_star(puzzle,1)
    if algorithm == "3":
        a_star(puzzle,2)
    

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
        
        #goal test
        if problem.is_goal(current.state):
            print("Number of nodes expanded: ", node_expanded)
            print("Max queue size: ",max_queue_size)
            return current
        
        visited.add(tuple(current.state))
        
        #use the expand function
        for child in expand(current,problem,heuristic_fn):
            if tuple(child.state) not in visited:
                heapq.heappush(open_queue,child)
                
        node_expanded+=1
    return None
    
        
        