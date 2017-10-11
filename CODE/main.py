import sys
import copy
import heapq

filename=sys.argv


num_nodes_expanded=0

#Opening input file for reading and reading the inputs

file=open(filename[1],"r")
line=file.readline()
num_blocks=int(line)
line=file.readline()
line=line.strip()
algorithm=line

line=file.readline()
line=file.readline()
line=line.strip()
i_state=line

line=file.readline()
line=file.readline()
line=line.strip()
g_state=line


ll=i_state.split(") (")
ll[0]=ll[0][1:]
ll[len(ll)-1]=ll[len(ll)-1][:-1]


i_state=ll


state_size=num_blocks**2+3*num_blocks+1

s=[]
g=[]

"""
STATE DESCRIPTION

All the states have been stored in the form of a boolean array of size n^2+3*n+1
The first n^2 entries denote if any of the predicates on(1,1), on(1,2),....., on(n,n) are true in that state
The next n entries denote if any of the predicates ontable(1), ontable(2),...., ontable(n) are true in that state
The next n entries denote if any of the predicates clear(1), clear(2),...., clear(n) are true in that state
The next n entries denote if any of the predicates hold(1), hold(2),...., hold(n) are true in that state
The last entry denotes if predicate <empty> is true in that state or not 
"""

s=[0]*state_size                       
g=[0]*state_size

for i in range(len(ll)):                       # Populating the starting state array
        ele=ll[i]
        ele=ele.split(" ")
        if(ele[0]=="on"):
                num1=int(ele[1])-1
                num2=int(ele[2])-1
                s[num1*num_blocks+num2]=1
        elif(ele[0]=="ontable"):
                num1=int(ele[1])-1
                s[num_blocks*num_blocks+num1]=1
        elif(ele[0]=="clear"):
                num1=int(ele[1])-1
                s[num_blocks*num_blocks+num_blocks+num1]=1
        elif(ele[0]=="hold"):
                num1=int(ele[1])-1
                s[num_blocks*num_blocks+2*num_blocks+num1]=1
        elif(ele[0]=="empty"):
                s[num_blocks*num_blocks+3*num_blocks]=1
                

ll=[]
ll=g_state.split(") (")
ll[0]=ll[0][1:]
ll[len(ll)-1]=ll[len(ll)-1][:-1]

g_state=ll


for i in range(len(ll)):                         # Populating the goal state array
        ele=ll[i]
        ele=ele.split(" ")
        if(ele[0]=="on"):
                num1=int(ele[1])-1
                num2=int(ele[2])-1
                g[num1*num_blocks+num2]=1
        elif(ele[0]=="ontable"):
                num1=int(ele[1])-1
                g[num_blocks*num_blocks+num1]=1
        elif(ele[0]=="clear"):
                num1=int(ele[1])-1
                g[num_blocks*num_blocks+num_blocks+num1]=1
        elif(ele[0]=="hold"):
                num1=int(ele[1])-1
                g[num_blocks*num_blocks+2*num_blocks+num1]=1
        elif(ele[0]=="empty"):
                g[num_blocks*num_blocks+3*num_blocks]=1      


# Defined a queue for using in BFS search

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0


# Defined a priority queue for using in aStar search

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

# Defined a stack for using in 

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0




"""
Finds out the successors of a state and returns them as a list along with the action required to reach them
GIves only the valid actions by matching the preconditions of all the actions
"""
def successors(state):            
        actions=[]
        if(state[num_blocks*num_blocks+3*num_blocks]==1):                           # if empty is true in that state
                for i in range(num_blocks*num_blocks,num_blocks*num_blocks+num_blocks):
                        if(state[i]==1 and state[i+num_blocks]==1):         
                                action=[]
                                newstate=copy.deepcopy(state)
                                newstate[i]=0
                                newstate[i+num_blocks]=0
                                newstate[num_blocks*num_blocks+3*num_blocks]=0
                                newstate[i+2*num_blocks]=1
                                string="pick "+str(i-num_blocks*num_blocks+1)     
                                action.append(newstate)             
                                action.append(string)
                                actions.append(action)                     # Adding pick action to the list of valid actions
                
                for i in range(num_blocks*num_blocks):
                        if(state[i]==1):
                                a=i/num_blocks+1
                                b=i%num_blocks+1
                                
                                if(state[num_blocks*num_blocks+num_blocks-1+a]==1):
                                        action=[]
                                        newstate=copy.deepcopy(state)
                                        newstate[num_blocks*num_blocks+num_blocks-1+a]=0
                                        newstate[num_blocks*num_blocks+3*num_blocks]=0
                                        newstate[i]=0
                                        newstate[num_blocks*num_blocks+num_blocks-1+b]=1
                                        newstate[num_blocks*num_blocks+2*num_blocks-1+a]=1
                                        string="unstack "+str(a)+" "+str(b)
                                        action.append(newstate)
                                        action.append(string)
                                        actions.append(action)               # Adding unstack action to the list of valid actions
                                        
              
        else:                                                                               # is empty is not true in that state
                for i in range(num_blocks*num_blocks,num_blocks*num_blocks+num_blocks):
                        if(state[i+2*num_blocks]==1):
                                action=[]
                                newstate=copy.deepcopy(state)
                                
                                newstate[i]=1
                                newstate[i+num_blocks]=1
                                newstate[i+2*num_blocks]=0
                                
                                newstate[num_blocks*num_blocks+3*num_blocks]=1
                                
                                string="release "+str(i-num_blocks*num_blocks+1)
                                action.append(newstate)
                                action.append(string)
                                actions.append(action)                     # Adding release action to the list of valid actions
                                
                for i in range(num_blocks*num_blocks+2*num_blocks,num_blocks*num_blocks+3*num_blocks):
                        if(state[i]==1):
                                for j in range(num_blocks*num_blocks+num_blocks,num_blocks*num_blocks+2*num_blocks):
                                        if(state[j]==1 and i!=j):
                                                action=[]
                                                newstate=copy.deepcopy(state)
                                                newstate[j]=0
                                                newstate[i]=0
                                                a=i-(num_blocks*num_blocks+2*num_blocks)
                                                b=j-(num_blocks*num_blocks+num_blocks)
                                                newstate[num_blocks*num_blocks+3*num_blocks]=1
                                                newstate[num_blocks*num_blocks+num_blocks+a]=1
                                                newstate[a*num_blocks+b]=1
                                                string="stack "+str(a+1)+" "+str(b+1)
                                                action.append(newstate)
                                                action.append(string)
                                                actions.append(action)                 # Adding stack action to the list of valid actions
                
        return actions

"""
Function which returns true if the current state is a goal state(given in the file) 
or else returns false
"""
def isGoalState(state):
        if(len(state)!=len(g)):
                return 0
        for i in range(len(g)):
                if(state[i]!=g[i]):
                        return 0
        return 1

"""
Heuristic for aStar search
"""
def heuristic(state):
        ans=0
        for i in range(num_blocks*num_blocks):
                if(g[i]!=state[i]):
                        ans=ans+10
                        
        
        for i in range(num_blocks*num_blocks+num_blocks,num_blocks*num_blocks+2*num_blocks):
                if(g[i]!=state[i]):
                        ans=ans+1
        
        return ans

# BFS search

def breadthFirstSearch():

    global num_nodes_expanded    # for counting the total number of nodes expanded in the search
    
    """Search the shallowest nodes in the search tree first."""
    
    
    """
    Initializing the queue and the frontier and explored lists
    Also initializing the list of actions to reach the goal state
    """
    queue=Queue()                     # using queue for bfs because of FIFO priciple     
    state=s
    rev_list_of_actions=[]
    
    parents={}                             # Stores the parent co-ordinates of a given co-ordinate ( key: co-ordinate , value: parent co-ordinate )
    info={}
    
    """ Stores the information of a given co-ordinate in the form of the action taken on its parent co-ordinate to reach it and the 
        length of edge traversed to reach it ( key: co-ordinate , value: (co-ordinate,action,edgelength) ) """
        
    explored={}                     # Explored list
    frontier={}                     # Frontier List
    state=tuple(state)
    parents[state]=None                 # Initializing for the parent node
    info[state]=None                    # Initializing for the parent node
    
    """
    The queue and the frontier list contain the same elements(always)
    Since we cannot check if an element is in the queue or not
    Thats why we are using an addiotional dictionary(frontier list)
    """
    
    frontier[state]=state           # Pushing the starting state onto the queue and frontier list
    queue.push(state)
    
    while(not queue.isEmpty()):
        num_nodes_expanded+=1
        ele=queue.pop()
        del frontier[ele]
        explored[ele]=ele
        state=ele
        
        if(isGoalState(state)):     # is goal state
                cur=ele
                while(info[cur]!=None):
                        rev_list_of_actions.append(info[cur][1])        # adding the actions in the reverse order
                        cur=parents[cur]
                list_of_actions=[]
                while(rev_list_of_actions!=[]):                         # Reversing the list of actions
                        list_of_actions.append(rev_list_of_actions[-1])
                        rev_list_of_actions.pop()
                return list_of_actions
        
        suc=successors(list(state)) 
             
        while(suc!=[]):                                    #  For all successors
                if tuple(suc[-1][0]) in explored.keys():                               # if already explored  
                        suc.pop()
                else:
                        if tuple(suc[-1][0]) in frontier.keys():                       # if in the frontier list
                                suc.pop()
                        else:
                                tup=tuple(suc[-1][0])                  # else saving the information of the co-ordinate and pushing it on the frontier list
                                parents[tup]=ele
                                frontier[tup]=tup
                                info[tup]=suc[-1]
                                queue.push(tup)
                                suc.pop()
                                
    return []                # If no solution found

    
    
    
#aStar Search

def aStarSearch():
    """Search the node that has the lowest combined cost and heuristic first."""

    global num_nodes_expanded             # for counting the total number of nodes expanded in the search
    
    """
    Initializing the priority queue and the frontier and explored lists
    Also initializing the list of actions to reach the goal state
    """
    
    priority_queue=PriorityQueue()       # using priority queue for ucs because we want to get the minimum cost path node at any time
    state=s
    list_of_actions=[]
    
    parents={}                               # Stores the parent co-ordinates of a given co-ordinate ( key: co-ordinate , value: parent co-ordinate )
    info={}
    """ Stores the information of a given co-ordinate in the form of the action taken on its parent co-ordinate to reach it and the 
        length of edge traversed to reach it ( key: co-ordinate , value: (co-ordinate,action,edgelength) ) """
        
    frontier={}          # Frontier List
    explored={}          # Explored List
    state=tuple(state)
    info[state]=None              # Initializing for the parent node
    parents[state]=None           # Initializing for the parent node
    
    """
    The priority queue and the frontier list contain the same elements(always)
    Since we cannot check if an element is in the priority queue or not
    Thats why we are using an addiotional dictionary(frontier list)
    """
    
    frontier[state]=0                       # Pushing the starting state onto the queue and frontier list
    priority_queue.push(state,heuristic(state))

    while(not priority_queue.isEmpty()):
        num_nodes_expanded+=1
        ele=priority_queue.pop()
        explored[ele]=ele
        state=ele
        
        if(isGoalState(ele)):               # is goal state
                cur=ele
                while(info[cur]!=None):
                        list_of_actions.append(info[cur][1])                   # adding the actions in the reverse order
                        cur=parents[cur]
                rev_list_of_actions=[]
                while(list_of_actions!=[]):                                    # Reversing the list of actions
                        rev_list_of_actions.append(list_of_actions[-1])
                        list_of_actions.pop()
                return rev_list_of_actions
                
        suc=successors(list(state))
        while(suc!=[]):                                            # For all successors
                if tuple(suc[-1][0]) in explored.keys():                              # if already explored  
                        suc.pop()
                else:
                        if tuple(suc[-1][0]) in frontier.keys():                      # if in the frontier list update its priority
                                tup=tuple(suc[-1][0])
                                priority_queue.update(tup,1+frontier[ele]+heuristic(tup))
                                # updatig with the value of heuristic plus the cost of reaching that node
                                if(frontier[tup]>1+frontier[ele]):
                                        frontier[tup]=1+frontier[ele]
                                        info[tup]=suc[-1]
                                        parents[tup]=ele
                        else:                                   # else saving the information of the co-ordinate and pushing it on the frontier list
                                tup=tuple(suc[-1][0])
                                priority_queue.update(tup,1+frontier[ele]+heuristic(tup))
                                # updatig with the value of heuristic plus the cost of reaching that node
                                frontier[tup]=1+frontier[ele]
                                info[tup]=suc[-1]
                                parents[tup]=ele
                        suc.pop()
    
        del frontier[ele]
    
    return []           # If no solution found
    

# GoalStackPlanning search

def goalStackPlanning():
        actions_to_take=[]                     # List of actions to take (initially empty)
        stack=Stack()                          # Stack initialized
        new=copy.deepcopy(g)
        stack.push(new)                        # pushing the goal state onto the stack
        cur_state=copy.deepcopy(s)
        p_cond=[0]*(num_blocks*num_blocks+3*num_blocks+1)
        
        for i in range(num_blocks*num_blocks+3*num_blocks+1):              # Pushing the predicates of the goal state individually onto the stack
                if(new[i]==1):
                        stack.push(i+1)    
                        
        while(not stack.isEmpty()):            # While stack not empty
                ele=stack.pop()
                if(type(ele)==list):                                       # if popped element is a conjunct goal
                        passed=1
                        for i in range(num_blocks*num_blocks+3*num_blocks+1):     # Checking if all the predicates are individually true
                                if(ele[i]==1 and cur_state[i]==0):
                                        passed=0
                                        break
                        """
                        If the predicates are not true then pushing the conjunct goal
                        and the individual predicates on the stack again
                        """
                        if(passed==0):                                     
                                stack.push(ele)
                                for i in range(num_blocks*num_blocks+3*num_blocks+1):
                                        if(ele[i]==1):
                                                stack.push(i+1)
                elif(type(ele)==int):                                       # if popped element is a predicate
                        if(cur_state[ele-1]==0):                              # if <empty> present in current state>
                                act=[]
                                ano=ele-1
                                if(ano<num_blocks*num_blocks):               # if predicate is on(x,y), selecting the relevant action to push on the stack
                                        a=ano/num_blocks
                                        b=ano%num_blocks
                                        act="stack "+str(a+1)+" "+str(b+1)
                                        stack.push(act)
                                        precond=copy.deepcopy(p_cond)
                                        precond[num_blocks*num_blocks+num_blocks+b]=1
                                        precond[num_blocks*num_blocks+2*num_blocks+a]=1
                                        stack.push(precond)
                                        stack.push(num_blocks*num_blocks+num_blocks+b+1)
                                        stack.push(num_blocks*num_blocks+2*num_blocks+a+1)
                                elif(ano<num_blocks*num_blocks+num_blocks):  # if predicate is Ontable(x), selecting the relevant action to push on the stack
                                        a=ano-(num_blocks*num_blocks)
                                        act="release "+str(a+1)
                                        stack.push(act)
                                        precond=copy.deepcopy(p_cond)
                                        precond[num_blocks*num_blocks+2*num_blocks+a]=1
                                        stack.push(precond)
                                        stack.push(num_blocks*num_blocks+2*num_blocks+a+1)
                                elif(ano<num_blocks*num_blocks+2*num_blocks):  # if predicate is Clear(x), selecting the relevant action to push on the stack
                                        holdblock=0
                                        b=ano-(num_blocks*num_blocks+num_blocks)
                                        if(cur_state[num_blocks*num_blocks+2*num_blocks+b]==1):
                                                holdblock=1
                                        if(holdblock==1):
                                                a=ano-(num_blocks*num_blocks+num_blocks)
                                                # Release block only
                                                act="release "+str(a+1)
                                                stack.push(act)
                                                precond=copy.deepcopy(p_cond)
                                                precond[num_blocks*num_blocks+2*num_blocks+a]=1
                                                stack.push(precond)
                                                stack.push(num_blocks*num_blocks+2*num_blocks+a+1)
                                        else:
                                                b=ano-(num_blocks*num_blocks+num_blocks)
                                                a=-1
                                                for i in range(num_blocks):
                                                        if(cur_state[i*num_blocks+b]==1):
                                                                a=i
                                                                break
                                                if(a!=-1):
                                                        act="unstack "+str(a+1)+" "+str(b+1)
                                                        stack.push(act)
                                                        precond=copy.deepcopy(p_cond)
                                                        precond[num_blocks*a+b]=1
                                                        precond[num_blocks*num_blocks+3*num_blocks]=1
                                                        precond[num_blocks*num_blocks+num_blocks+a]=1
                                                        stack.push(precond)
                                                        stack.push(num_blocks*num_blocks+num_blocks+a+1)
                                                        stack.push(num_blocks*num_blocks+3*num_blocks+1)
                                                        stack.push(num_blocks*a+b+1)
                                
                                elif(ano<num_blocks*num_blocks+3*num_blocks):  # if predicate is hold(x), selecting the relevant action to push on the stack
                                        a=ano-(num_blocks*num_blocks+2*num_blocks)
                                        ontable=0
                                        if(cur_state[num_blocks*num_blocks+a]==1):
                                                ontable=1
                                        if(ontable==1):
                                                act="pick "+str(a+1)
                                                stack.push(act)
                                                precond=copy.deepcopy(p_cond)
                                                precond[num_blocks*num_blocks+a]=1
                                                precond[num_blocks*num_blocks+num_blocks+a]=1
                                                precond[num_blocks*num_blocks+3*num_blocks]=1
                                                stack.push(precond)
                                                stack.push(num_blocks*num_blocks+3*num_blocks+1)
                                                stack.push(num_blocks*num_blocks+num_blocks+a+1)
                                                stack.push(num_blocks*num_blocks+a+1)
                                        else:
                                                b=-1
                                                for i in range(a*num_blocks,(a+1)*num_blocks):
                                                        if(cur_state[i]==1):
                                                                b=i
                                                                break
                                                if(b!=-1):
                                                        b=b-a*num_blocks
                                                        act="unstack "+str(a+1)+" "+str(b+1)
                                                        stack.push(act)
                                                        precond=copy.deepcopy(p_cond)
                                                        precond[num_blocks*a+b]=1
                                                        precond[num_blocks*num_blocks+3*num_blocks]=1
                                                        precond[num_blocks*num_blocks+num_blocks+a]=1
                                                        stack.push(precond)
                                                        stack.push(num_blocks*num_blocks+num_blocks+a+1)
                                                        stack.push(num_blocks*num_blocks+3*num_blocks+1)
                                                        stack.push(num_blocks*a+b+1)
                                                        s
                                else:
                                        a=-1
                                        for i in range(num_blocks*num_blocks+2*num_blocks,num_blocks*num_blocks+3*num_blocks):
                                                if(cur_state[i]==1):
                                                        a=i-num_blocks*num_blocks-2*num_blocks
                                                        break
                                        if(a!=-1):
                                                act="release "+str(a+1)
                                                stack.push(act)
                                                precond=copy.deepcopy(p_cond)
                                                precond[num_blocks*num_blocks+2*num_blocks+a]=1
                                                stack.push(precond)
                                                stack.push(num_blocks*num_blocks+2*num_blocks+a+1)
                          
                                
                elif(type(ele)==str):                    # if popped element is an action, then applying the action to the current state and storing it
                        actions_to_take.append(ele)
                        elements=ele.split(" ")
                        if(elements[0]=="pick"):
                                num=int(elements[1])
                                cur_state[num_blocks*num_blocks+num-1]=0                  # Not ontable
                                cur_state[num_blocks*num_blocks+num_blocks+num-1]=0       # Not Clear
                                cur_state[num_blocks*num_blocks+2*num_blocks+num-1]=1     # Hold Block
                                cur_state[num_blocks*num_blocks+3*num_blocks]=0           # Not empty
                        elif(elements[0]=="unstack"):
                                num1=int(elements[1])
                                num2=int(elements[2])
                                cur_state[num_blocks*num_blocks+2*num_blocks+num1-1]=1     # Hold(A)
                                cur_state[num_blocks*num_blocks+num_blocks+num2-1]=1       # Clear(B)
                                cur_state[num_blocks*(num1-1)+num2-1]=0                    # not on(A,B)
                                cur_state[num_blocks*num_blocks+3*num_blocks]=0            # not empty
                                cur_state[num_blocks*num_blocks+num_blocks+num1-1]=0       # Not Clear(A)
                        elif(elements[0]=="release"):
                                num=int(elements[1])
                                cur_state[num_blocks*num_blocks+num-1]=1                  # ontable
                                cur_state[num_blocks*num_blocks+num_blocks+num-1]=1       # Clear
                                cur_state[num_blocks*num_blocks+2*num_blocks+num-1]=0     # Not Hold Block
                                cur_state[num_blocks*num_blocks+3*num_blocks]=1           # empty
                        elif(elements[0]=="stack"):
                                num1=int(elements[1])
                                num2=int(elements[2])
                                cur_state[num_blocks*num_blocks+2*num_blocks+num1-1]=0     # Not Hold(A)
                                cur_state[num_blocks*num_blocks+num_blocks+num2-1]=0       # Not Clear(B)
                                cur_state[num_blocks*(num1-1)+num2-1]=1                    # on(A,B)
                                cur_state[num_blocks*num_blocks+3*num_blocks]=1            # empty
                                cur_state[num_blocks*num_blocks+num_blocks+num1-1]=1       # Clear(A)

        return actions_to_take                                # returning the final list of actions
                                  
file.close()        

file=open("output_"+filename[1],"w")
if(algorithm=="f"):                            # if BFS algorithm specified in the input file, writing result to output file
        actions=breadthFirstSearch() 
        print "BFS search used"
        print "Solution Length: ",len(actions)
        file.write(str(len(actions))+"\n")      
        for i in range(len(actions)):
                file.write(actions[i]+"\n")
        print "Number of nodes expanded: ",num_nodes_expanded

elif(algorithm=="a"):                           # if aStar alogrithm specified in the input file, writing result to output file
        actions=aStarSearch()  
        print "AStar search used"
        print "Solution Length: ",len(actions)
        file.write(str(len(actions))+"\n") 
        for i in range(len(actions)):
                file.write(actions[i]+"\n")
        print "Number of nodes expanded: ",num_nodes_expanded
        
elif(algorithm=="g"):                           # if GoalStackPlanning algorithm specified in the input file, writing result to output file
        actions=goalStackPlanning()
        print "Goal Stack Planning used" 
        print "Solution Length: ",len(actions)
        file.write(str(len(actions))+"\n")      
        for i in range(len(actions)):
                file.write(actions[i]+"\n")
                
file.close()




