# IMPLEMENTATION OF GROUNDED SEMANTICS

# start by assigning IN to all unattacked arguments
# then, iteratively OUT is assigned to arguments that is attacked
# by arguments labelled IN
# then, labelling IN to arguments whose all attackers are OUT
# arguments on each iteration are reinstated by IN arguments on the previous iteration.
# Iteration continues:
# until no new arguments are made IN or OUT
# then, arguments remain unlabelled are assigned UNDEC.

label_in = set()
label_out = set()
label_undec = set()
dict = {}

def grounded(nodes, links):
    for node in nodes:
        counter = True
        for search_node, attack in enumerate(links):
            if (node == attack[1]):
                #if the node is attacked by itself or another node
                counter = False
                break
        if (counter == True):
            label_in.add(node)

    while (True):
        last_label_in = label_in.copy()
        last_label_out = label_out.copy()

        for node in nodes:
            if node not in label_in and node not in label_out:
                ans = True
                attackers = [search_node[0] for iterate, search_node in enumerate(links) if node == search_node[1]]
                # print(attackers)
                for attacker in attackers:
                    if attacker not in label_out:
                        ans = False
                        break
                if ans == True:
                    label_in.add(node)

        for node in nodes:
            if node not in label_out and node not in label_in:
                ans = False
                attackers = [search_node[0] for iterate, search_node in enumerate(links) if node == search_node[1]]
                # print(attackers)
                for attacker in attackers:
                    if attacker in label_in:
                        ans = True
                        break
                if ans == True:
                    label_out.add(node)

        if (last_label_in == label_in and last_label_out == label_out):
            break

    # Labelling unlabelled nodes as UNDEC
    for node in nodes:
        if node not in label_in and node not in label_out:
            label_undec.add(node)

    dict['label_in'] = list(label_in)
    dict['label_out'] = list(label_out)
    dict['label_undec'] = list(label_undec)
    return dict

