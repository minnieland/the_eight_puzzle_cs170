import heapq as min_heap_esque_queue#for A*

#test cases from the slides
depth_zero = [[1,2,3],
                    [4,5,6],
                    [7,8,0]]
eight_goal_state = [[1,2,3],
                    [4,5,6],
                    [7,8,0]]

#represents the state of the puzzle, lower cost in priority queue
class Node:
    def __init__(self,state,parent=None, action=None, cost=0):
        self.state=state,
        self.parent=parent,
        self.action=action,
        #depth?
        self.cost=cost
        
        def __lt__(self,other):
            return self.cost < other.cost
        
def main():
    puzzle_mode= input("Welcome to the 8 puzzle! Select '1' for a default puzzle. Select '2' to create your own." 
                       + '\n')
    if puzzle_mode == '1':
        # do smt
        # select...
    # if puzzle_mode == '2':
        #do tmr
    
        return

if __name__ == "__main__":
    main()
    
#create child nodes (all possible next moves from curr node)
def expand(node, problem):
    children=[]
    for action, next_state, step_cost in problem.succesors(node.state):
        child = Node(
            state=next_state,
            parent=node,
            action=action,
            cost=node.cost + step_cost #total cost
        )
        children.append(child)
        return children


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
        
        