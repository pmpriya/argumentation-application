

class Labelling:

    label_in = set()
    label_out = set()
    label_undec = set()

    def __init__(self, label_in, label_out, label_undec):
        self.label_in = label_in
        self.label_out = label_out
        self.label_undec = label_undec

    # checks if node is in IN set of labelling
    def isIn(self, node):
        if (node in self.label_in):
            return True
        else:
            return False

    # checks if node is in OUT set of labelling
    def isOut(self, node):
        if (node in self.label_out):
            return True
        else:
            return False

    # checks if node is in UNDEC set of labelling
    def isUndec(self, node):
        if (node in self.label_undec):
            return True
        else:
            return False

    # checks if a node is labelled in labelling
    def hasLabelling(self,node):
        if (self.isIn(node) or self.isOut(node) or self.isUndec(node)):
            return True
        else:
            return False

    # checks if an argument is legally IN
    def legallyIN(self,node):
        if node in self.label_in:

            attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]
            for attacker in attackers:
                if attacker not in self.label_out:
                    return False

            return True
        return False

    # clears all arguments from a labelling
    def clear(self):
        in_set = self.label_in
        out_set = self.label_out
        undec_set = self.label_undec
        for a in in_set:
            in_set.remove(a)
        for a in out_set:
            out_set.remove(a)
        for a in undec_set:
            undec_set.remove(a)


#list of labellings
#global candidateLabellings

# initial labelling will have sets of label in , label out, label undec
#global initialLabelling
#initialLabelling = Labelling(nodes, [], [])
#global super_illegally_in

#global illegally_in
#illegally_in = set()


counter = 0
candidateLabellings = []
preferredLabellings = Labelling([], [], [])
super_illegally_in = set()
# returns an argument node that is super illegally IN in a labelling

def superIllegallyIn(labelling):
    getInSet = labelling.label_in
    for node in getInSet:
        attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]

        for attacker in attackers:
            # if attacker is legally IN or UNDEC
            if (labelling.legallyIN(attacker) or attacker in labelling.label_undec):
                return node
    return None


def transitionStep(labelling, node):
    labelling.label_in.remove(node)
    labelling.label_out.append(node)

    attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]

    for attacker in attackers:
        if (illegallyOut(labelling, attacker)):
            labelling.label_undec.append(attacker)
            labelling.label_out.remove(attacker)

    if (illegallyOut(labelling, node)):
        labelling.label_undec.append(node)
        labelling.label_out.remove(node)

    return labelling


def illegallyOut(labelling, node):
    if (node in labelling.label_out):
        attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]

        in_attackers = [attacker for attacker in attackers if attacker in labelling.label_in]
        if (len(in_attackers) == 0):
            return True

    return False


def hasNodesIllegallyIn(labelling):
    getInSet = labelling.label_in
    okay = False
    for node in getInSet:
        attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]

        for attacker in attackers:
            # if not all of it's attackers are OUT, return True
            if attacker not in labelling.label_out:
                okay = True
                break
        if (okay == True):
            return okay
    return False


def nodesIllegallyIn(labelling):
    illegally_in = set()
    getInSet = labelling.label_in
    okay = True
    for node in getInSet:
        attackers = [search_node[0] for iterate, search_node in enumerate(links_tuple) if node == search_node[1]]

        for attacker in attackers:
            if attacker not in labelling.label_out:
                # node is illegally in
                illegally_in.add(node)
                break
    return illegally_in


def findPreferredLabellings(labelling):
    # to make sure no strict subsets of labelling can be added
    # to candidateLabellings (list of labellings)

    # initial labelling passed as a parameter

    if (hasStrictSuperset(labelling)):
        return

    # if no nodes are illegally IN
    if (hasNodesIllegallyIn(labelling) == False):
        for lab in candidateLabellings:
            if (isStrictSubset(lab, labelling)):
                candidateLabellings.remove(lab)

        candidateLabellings.append(labelling)
        return

    else:
        if (superIllegallyIn(labelling) != None):
            node = superIllegallyIn(labelling)
            findPreferredLabellings(transitionStep(labelling, node))
        else:
            for node in nodesIllegallyIn(labelling):
                findPreferredLabellings(transitionStep(labelling, node))
    return candidateLabellings

def isStrictSubset(labelling1, labelling2):
    if(labelling1.label_in <= labelling2.label_in):
        if(len(labelling1.label_in) < len(labelling2.label_in)):
            return True
    return False

def hasStrictSuperset(labelling):
    for lab in candidateLabellings:
        if(set(lab.label_in).issuperset(set(labelling.label_in))):
            return True
    return False

def getCandidateLabellings():
    return candidateLabellings

def getNumberOfSteps():
    return counter


def outputPreferredSemantics(candidateLabellings):
    for labelling in candidateLabellings:
        print("Preferred Labelling: IN: {}, OUT: {}, UNDEC:{}".format(labelling.label_in, labelling.label_out,
                                                                      labelling.label_undec))

if __name__=='__main__':
    # initial labelling will have sets of label in , label out, label undec
    nodes = ['a1', 'a2', 'a3', 'a4', 'a5']
    nodes = ['Lockdown is not demanded as wearing masks is sufficient', 'Lockdown should be necessary to control virus', '70% citizens think lockdown is ineffective to control virus','Lockdown should be mandatory to reduce cases', 'New batman movie was dope']
    links_tuple = [('a1', 'a2'), ('a2', 'a3')]
    links_tuple = [('Lockdown is not demanded as wearing masks is sufficient', 'Lockdown should be necessary to control virus'), ('Lockdown should be necessary to control virus', '70% citizens think lockdown is ineffective to control virus')]


    initialLabelling = Labelling(nodes, [], [])
    candidateLabellings = findPreferredLabellings(initialLabelling)
    print(outputPreferredSemantics(candidateLabellings))

