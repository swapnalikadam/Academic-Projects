import random
import string 
import sys
import matplotlib.pyplot as plt
import networkx as nx
import os

# This program generates a drill for the DFS and BFS algorithm
# In each question, the student is given directed graph and vertex as options
# and needs to select all vertices which DFS visits before BFS.

###################
#general parameters 
###################

#number of questions: the first command-line argument 
if len(sys.argv) >1:
    num_questions = int(sys.argv[1])
else: 
    num_questions = 5

num_answers = 8  #number of answer options, usually at least 8, 10 is common, larger is OK for some questions.  
maxchecked = 4   #maximum number of options for which correct is to be selected (checked), in the range 1..num_answers
minchecked = 1   #minimal number of options for which correct is to be selected (checked), in the range 1..maxchecked
                 #note that D2L requires at least one option to be set as "checked" to submit a question 
points = num_answers  #leave as is. 
html = "HTML"      # whether the question and answers are in html (preferred) or plain text. If html, set html = "HTML"  if plain, set html = ""

###################
# parameters specific to this drill 
###################

n = 5  #array size

###################
# fixed text for the question statement, feedbacks, and drill description in the file header  
###################

# Description of the drill, in particular answer choices/feedbacks types, for the output file header as plain text 
# start all subsequent lines with no indentation, and use triple double-quote marks at the start and end 
# if you need to use quotes in your text, write \"; same for \/ for /  

drillheader = """(Note: The images folder is assumed to be in the \/content\/<course path>\/ directory) 
Question Text is always a required field

DFS vs BFS: select all vertices that DFS visits before BFS: 
Given directed graph, select all  vertices start from vertex A; 8 answer choices. 
Variants of answers to be covered in every question: see feedback, there are 2 choices, Incorrect: Vertex that DFS does not visits before BFS, Correct: Vertex that DFS visits before BFS. 
"""

# include drill description in the csv file as well. 
# It will contain the text that will go into the D2L quiz intro/description, 
# in particular a solved example.  
drilldescription = """
<p>This is a drill about Depth First Search(DFS) Vs Breadth First Search(BFS), in particular, exploring the definition of what it means by Depth First Search algorithm visits vertices before Breadth First Search algorith in graph traversal. 
Both Depth First Search(DFS) and Breadth First Search(BFS) algorithms break ties in alphabetical order.
To answer it, you need to find all vertices which Depth First Search(DFS) traverse in given directed graph as well as all vertices which Breadth First Search(BFS) traverse in given directed graph and make sure you are traversing in an alphabetical order. 
Then check which vertex Depth First Search(DFS) visits before Breadth First Search(BFS) and mark(check checboxes at front of options) such vertices from given vertices options.
Note. When you are at root node A, from A if there are 2 outgoing edges, one for B and other for I, since from A you can go to either of them,  You need to check the alphabetical order of B and I. 
As B is the 2nd letter of the alphabet and I is 9th, and 2<9, then Depth First Search(DFS) and Breadth First Search(BFS) algorithms will visit B first, and then after backtracking back to A, try to visit I if it did not explore it yet.

<br><br>
For example, suppose that the question is as follows:  
Consider given directed graph, From vertex A, select all vertices that Depth First Search(DFS) visits before Breadth First Search(BFS). 
Both Depth First Search(DFS) and Breadth First Search(BFS) algorithms break ties in alphabetical order. 
Suppose that the vertices which Depth First Search(DFS) visits before Breadth First Search(BFS) are 'C', 'F', 'H', 'G'. 
Select these vertices from given multiple choice option list.</p><br>

given directed graph in a form of edges and vertices<br>
<img src='images/DFSvsBFS_description.png' /><br>

dfs_list:  ['A', 'B', 'C', 'F', 'H', 'G', 'E']</br>
bfs_list:  ['A', 'B', 'E', 'C', 'F', 'H', 'G']
</br><br>
After comparing above dfs_list with bfs_list, the <strong> Vertices that DFS visits Before BFS are ['C', 'F', 'H', 'G']</strong> 

<br><br>And suppose the option choices are:  A, B, C, D, E, F, G, H.

<br><br>First of all, Implement Depth First Search(DFS) and Breadth First Search(BFS) to find vertices for both the algorithms by traversing the given directed graph. 
Then compare vertices which DFS visits before BFS and mark those vertices from options as correct answers.<br>
A - DFS does not visits vertex before BFS, because A is a start vertex and both DFS as well as BFS will visit A in a same order i.e 1st vertex, Leave unselected/unchecked<br>
B - DFS does not visits vertex before BFS, Leave unselected/unchecked<br>
C - DFS visits vertex before BFS, Select this option.<br>
D - DFS does not visits vertex before BFS, Leave unselected/unchecked<br>
E - DFS visits vertex before BFS, Select this option too.<br>
F - DFS visits vertex before BFS, Select this option too.<br>
G - DFS does not visits vertex before BFS, Leave unselected/unchecked<br>
H - DFS visits vertex before BFS, Select this option too.<br>
"""

# an array of feedbacks corresponding to different types of answers (classified by this array index) 
#avoid using commas in feedbacks 

feedbacks = ["Incorrect: DFS does not visit this vertex before BFS",
            "Correct: DFS visits this vertex before BFS" ]


# Function to generate the text of the statement of the question.

def get_statement():
    
#The statement needs to be one cell in a csv file, no newlines, \" at the beginning and end, and get it all into one line 
# (use \ at the end of lines to split text for readability), and put """ before and after. 
#If using html (like here), make sure to set html = True above

    statement = """\"<p>Consider given directed graph for starting from root vertex A. Find<strong> all</strong> Vertices that Depth First Search(DFS) algorithm visits before Breadth First Search(BFS).</p>\" """
    
    return statement 
  

###################
# Formatting/printing functions. 
###################  

#print csv file header, erasing file content. Also put feedback list in the header. 
# uses drillheader and feedbacks variables 

def print_header():

    # prepend every line with  the comment // and put 4 commas at the end to preserve the format. 
    # the first part is the content of drillheader, then a line with the word "Feedbacks", then a numbered list of feedbacks (answer choice types)
    
    csvheader = '\n'.join(["//"+x+",,,," for x in drillheader.split('\n')+\
                           ["Description: "]+drilldescription.split('\n')+\
                           ["Feedbacks:"]+[str(i)+": "+s for i,s in enumerate(feedbacks)]+[""] ])

    f = open(filename, "w", encoding="utf-8")
    f.write(csvheader)
    f.close()

    
# text is a string of the answer choice
# checked is a Boolean (True if correct answer is to check this option)
# feedback_index is an int indexing into feedbacks array (in [0..length(feedbacks)-1]) 

def print_answer(text,checked,feedback_index):
    if html=="HTML":
        answer_row=",".join(["Option",str(int(checked)),text,"HTML",feedbacks[feedback_index],"HTML"]) 
    else:
        answer_row=",".join(["Option",str(int(checked)),text,feedbacks[feedback_index]])
    return answer_row

    
# depending on whether the question and/or answers use html, and whether there is an image in the question     
# returns a formatting of a question ready to be dumped into a csv file. 
# Here, "num" is enumerating question variants 
# statement is the body of the question as a string 
# answers is a list of answer strings, each obtained with print_answer. 
# see get_statement and get_answers for the respective formats

# no html 

def print_question(num,statement,answers):
    
    question = """,,,,
//variant """ + str(num) + """,,,,
NewQuestion,MS,,,
Title,,,,
QuestionText,""" + statement + ","+html+""",,
Points,"""+ str(points) +""",,,
Difficulty,1,,,
Scoring,RightAnswers,,, 
""" + answers+"""
"""

    return question


def print_image_question(num,statement,answers,image):

    question = """,,,,
//variant """ + str(num) + """,,,,
NewQuestion,MS,,,
Title,,,,
QuestionText,""" + statement + ","+html+""",,
Points,"""+ str(points) +""",,,
Difficulty,1,,,
Image,images/"""+ image + """,,,
Scoring,RightAnswers,,, 
""" + answers+"""
"""
    return question 


###################
# generating answer choices 
###################

# print valid and invalid vertices in csv

def get_invalid_vertex(ans_text):

    return print_answer(ans_text, False, 0)  # feedback 0 is for invalid vertex


def get_valid_vertex(ans_text):

    return print_answer(ans_text, True, 1)  # feedback 1 is for valid vertex

# get all the answers in proper format
def getanswers(correct_ans,vertex_list):

    extract_invalid_ans_text = [item for item in vertex_list if item not in correct_ans]

    ans_list = list()
    # wrong answers
    for i in range(len(extract_invalid_ans_text)):
        ans_list.append(get_invalid_vertex(extract_invalid_ans_text[i]))

    #right answers
    for i in range(len(correct_ans)):
        ans_list.append(get_valid_vertex(correct_ans[i]))

    random.shuffle(ans_list)

    # return a string containing all answers in csv format
    return "\n".join(ans_list)

"""
    MAIN CODE STARTS HERE
    
"""

def bfs(visited, graph, node, queue, bfs_list):
  visited.append(node)
  queue.append(node)

  while queue:
    s = queue.pop(0)
    bfs_list.append(s) # added for view
    # print (s, end = " ")

    for neighbour in graph[s]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
  return bfs_list


def dfs(visited, graph, node, dfs_list):
    if node not in visited:
        # print (node)
        visited.add(node)
        dfs_list.append(node) # added for view
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour, dfs_list)
    return dfs_list


def visit_order_dfs_befr_bfs(dfs_list, bfs_list):
    dfs_dict = {x: i for i, x in enumerate(dfs_list)}
    bfs_dict = {x: i for i, x in enumerate(bfs_list)}

    visited_dfs_before_bfs = []
    for k, v in dfs_dict.items():
        if dfs_dict[k] < bfs_dict[k]:
            visited_dfs_before_bfs.append(k)
    return visited_dfs_before_bfs


def graph_make_pairs(graph):
    pairs = []
    for k,v in graph.items():
        for nodes in v:
            pairs.append((k,nodes))
    return pairs


def generate_graph(pairs, variant, is_descrption=False):
    """
    :param pairs:
    :param i: pass image version
    :return:
    """
    G = nx.DiGraph() # MultiGraph

    G.add_edges_from(pair for pair in pairs)

    nx.draw_shell(G, arrows=True, with_labels=True, **options)
    image_dir = 'images/'
    if not is_descrption:
        image_name = 'DFSvsBFS' + str(variant) + '.png'
    else:
        image_name = 'DFSvsBFS-description.png'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    plt.savefig(image_dir + image_name)
    plt.clf()
    return [image_dir, image_name]


def random_graph_logic():
    nodes = 8
    keys = list(string.ascii_uppercase[:nodes])
    min_length = 1
    max_length = 2

    graph = {
        key: random.sample(keys, k=random.randint(min_length,max_length)) for key in keys
    }
    pairs=[]
    for key, value in graph.items():
        if key in value:
            value.remove(key)
        for node in value:
            if (key, node) not in pairs:
                pairs.append((key, node))
            if (node, key) in pairs:
                graph[key].remove(node)
    ## Sorted graph
    for k, v in graph.items():
        graph[k] = sorted(graph[k])
    return graph


def create_graph_instance(variant):
    ans_len = 0
    while ans_len < 4:
        dfs_list = []
        bfs_list = []
        visited = []  # List to keep track of visited nodes.
        queue = []  # Initialize a queue
        dfs_visit = set()

        graph = random_graph_logic()
        # queue, bfs_list
        bfs(visited, graph, 'A', queue, bfs_list)
        dfs(dfs_visit, graph, 'A', dfs_list)
        pairs = graph_make_pairs(graph)
        ans = visit_order_dfs_befr_bfs(dfs_list, bfs_list)
        ans_len = len(ans)

    return {
        "graph": graph, "pairs": pairs, "dfs_list": dfs_list,
        "bfs_list": bfs_list, "ans_list": ans,
        "img_dir": generate_graph(pairs,variant)[0],
        "img_name": generate_graph(pairs, variant)[1]
    }


if __name__ == "__main__":
    # filename to be changed
    filename = "C:/Swapnali/MUN/Winter 2021-2022/Applied Algorithms/Drill Code/MUN_AppliedAlgo/DFSvsBFS.csv"

    # options for networksx Nodes
    options = {
        'node_color': 'yellow',
        'node_size': 700,
        'width': 3,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }

    nodes = 8
    node_list = list(string.ascii_uppercase[:nodes])

    print_header()

    f = open(filename, "a")

    for num in range(0,num_questions):
        res = create_graph_instance(num)
        dfs_list=[]
        vertices_dfs_visit_bfr_bfs = res["ans_list"]
        statement = get_statement()
        answers = getanswers(vertices_dfs_visit_bfr_bfs , node_list)
        f.write(print_image_question(num,statement,answers, res['img_name']))
    f.close()


    desc_graph = {
        'A': ['B', 'E'],
         'B': ['C', 'F'],
         'C': ['F', 'H'],
         'D': ['G', 'H'],
         'E': ['F', 'H'],
         'F': [],
         'G': ['A', 'E'],
         'H': ['G']
    }

    desc_pairs = graph_make_pairs(desc_graph)
    desc_img_dir, desc_img_name = generate_graph(desc_pairs, 1, True)

    print("code executed...")
    
