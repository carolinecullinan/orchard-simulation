# import necessary libraries
import turtle as t
import numpy as np
import random
import pandas as pd



# generation of the orchard

def orchard(orchard_size = 5, gprob_apple=0.7, gprob_pear=0.7, gprob_plum=0.7):
        """This function randomly assigns a percentage (0-100%) of orchard land for each tree type of apple, pear, and plum trees.
        
        orchard_size: the number of acres to be assigned to the orchard.
        gprob_apple: the growth probability that an apple tree seed has, expressed as a number within [0,100]
        gprob_pear: the growth probability that an pear tree seed has
        gprob_plum: the growth probability that an plum tree seed has."""
        
        # the land proportion to be assigned to apple trees is defined
        lpercent_apples = random.randint(2, 100)
        left_over = 100 - lpercent_apples
        
        if left_over > 0:
            # the land proportion to be assigned to pear trees is defined
            lpercent_pears = random.randint(1, left_over)
                
            # the land proportion to be assigned to plum trees is defined
            lpercent_plums = 100 - (lpercent_apples + lpercent_pears)
            
            # all land proportions are stored in a dictionary
            global land_dict
            land_dict = {'apples': lpercent_apples, 'pears': lpercent_pears, 'plums': lpercent_plums}

        apple_land = orchard_size * (.01 * land_dict['apples']) # amount of acres dedicated to growing apples
        apple_seeds = random.uniform(1.5, 1.8) # number of apple tree seeds sown per acre
        base_apple = apple_land * apple_seeds # base number of apple trees in the original orchard, that theoretically could grow
        base_apple = round(base_apple) + 2 # base number of apple trees in the original orchard rounded to a whole number + 2 to ensure that we have at least multiple trees for each tree type
        apple_trees = round(gprob_apple*base_apple) #actual number of apple trees that have grown from the sown seeds
        
        pear_land = orchard_size * (.01 * land_dict['pears']) # amount of acres dedicated to growing pears
        pear_seeds = 1.09 # number of pear tree seeds sown per acre
        base_pear = pear_land * pear_seeds # base number of pear trees in the original orchard, that theoretically could grow
        base_pear = round(base_pear) + 2 # base number of pear trees in the original orchard rounded to a whole number + 2 to ensure that we have at least multiple trees for each tree type
        pear_trees = round(gprob_pear*base_pear) #actual number of apple trees that have grown from the sown seeds
        
        plum_land = orchard_size * (.01 * land_dict['plums']) # amount of acres dedicated to growing plums
        plum_seeds = random.uniform(0.70, 1.09) # number of plum tree seeds sown per acre
        base_plum = plum_land * plum_seeds # base number of plum trees in the original orchard, that theoretically could grow
        base_plum = round(base_plum) + 2 # base number of plum trees in the original orchard rounded to a whole number + 2 to ensure that we have at least multiple trees for each tree type
        plum_trees = round(gprob_plum*base_plum) # actual number of apple trees that have grown from the sown seeds
        
        return apple_trees, pear_trees, plum_trees

    
    
# a more general superclass Tree, common to all species of trees, is defined

class Tree():
    # every tree, regardless of the species has the same L-System scheme of growth
    # this means, that all species share the following attributes and funcions
    all_apple_trees, all_pear_trees, all_plum_trees = orchard()
    time_line =list(range(0,14)) # consider the orchard over 15 years for now 
   

    def rules_setup(constants, rules):
        """This function adds all constants' associated rules to the rules dictionary"""
    
        for c in constants:
            if c not in rules:
                rules[c] = c
        return rules
    
    
    def input_check(constants, variables, rules, axiom=None):
        """This function checks whether each variable and constant has an associated rule to it.
        The check is performed in three steps so to allow a more precise error message, when
        an error is raised."""
    
        # check for Axiom
        if axiom != None and axiom not in rules:
            raise ValueError("the axiom does not have an associated rule")

        # check for Constants 
        for c in constants:
            if c not in rules:
                raise ValueError("some constants do not have an associated rule")

        # check for Variables        
        for v in variables:
            if v not in rules:
                raise ValueError("some variables do not have an associated rule")
                
        # check for Rules: whether rules' output values each has a rule that takes them as input values
        for new_string in rules.values():
            for c in new_string:
                if c not in rules:
                    raise ValueError("some rules' output values are not associated to any input of a rule")
            
            
    def first_iteration(start, constants, variables, rules):
        """This function computes the first iteration for the generation of an L-system:
        start: has to be the Axiom of the tree
        it retuns the first new string, the Axiom's corresponding value, according to the Rules dictionary"""

        Tree.input_check(constants, variables, rules, axiom=start)
        return rules[start]
    
    
    def ith_iteration(start, constants, variables, rules):
        """This function computes one iteration for the generation of an L-system:
        start: an initial string, representative of the tree state
        end: the new returned string, where each character was changed using the Rules dictionary"""

        Tree.input_check(constants, variables, rules)

        end = "" # because any character can be stored in a string, unlike lists, sets...
        for c in start:   # start will always have to be a string after the first iteration
            end += rules[c]
        return end
    
    
    def tree_string(axiom, constants, variables, rules, years):
        """This function generates the string representing a fractal tree
        at a specified time (years)"""
        Tree.rules_setup(constants, rules)
        newstring = Tree.first_iteration(axiom, constants, variables, rules)
        if years == 0:
            return axiom
        if years == 1:
            return newstring

        year = 1
        while year < years:
            newstring = Tree.ith_iteration(newstring, constants, variables, rules)
            year += 1

        return newstring
    
 
    def iterate_years(year_n): 
        iterate_years=str('Year '+ str(year_n))
        return iterate_years
        
    
    def species_harvest(species):
        """This takes as input a species name, and returns a dataframe containing on each row one tree's fruits that
        were produced across all the orchard's timeline."""
        
        if species == "AppleTree":
            # the total number of trees to generate is determined
            # this number is calculated based on the land proportion allocated to apple trees
            tot_n_trees = Tree.all_apple_trees
            
            # the apple_tree dataframe is generated having the fruits produced by each tree across multiple years as the dataframe's rows
            # years of the orchard are represented as columns, instead
            apple_orchard_df = pd.DataFrame(index = list(range(tot_n_trees)) )
            for year_n in range(len(Tree.time_line)):
                AppleTree.generate_trees( tot_n_trees, year_n)

                for tree_n in range(len(AppleTree.instances)):
                    apple_orchard_df.loc[ tree_n, Tree.iterate_years(year_n) ] = AppleTree.instances[tree_n].fruits
            
            # a column totals returns for each tree its total number of apples yielded over its whole life
            apple_orchard_df['Total'] = apple_orchard_df.sum(axis=1)
            return apple_orchard_df

        elif species == "PearTree":
            tot_n_trees = Tree.all_pear_trees
            pear_orchard_df = pd.DataFrame(index = list(range(tot_n_trees)) )

            for year_n in range(len(Tree.time_line)):
                PearTree.generate_trees( tot_n_trees, year_n)

                for tree_n in range(len(PearTree.instances)):
                    pear_orchard_df.loc[ tree_n, Tree.iterate_years(year_n) ] = PearTree.instances[tree_n].fruits

            pear_orchard_df['Total'] = pear_orchard_df.sum(axis=1)
            return pear_orchard_df

        else:
            tot_n_trees = Tree.all_plum_trees
            plum_orchard_df = pd.DataFrame(index = list(range(tot_n_trees)) )

            for year_n in range(len(Tree.time_line)):
                PlumTree.generate_trees( tot_n_trees, year_n)

                for tree_n in range(len(PlumTree.instances)):
                    plum_orchard_df.loc[ tree_n, Tree.iterate_years(year_n) ] = PlumTree.instances[tree_n].fruits

            plum_orchard_df['Total'] = plum_orchard_df.sum(axis=1)
            return plum_orchard_df
    
    
    
# Apple Tree is a specific species of tree, subclasses of Tree, and is defined here
# they inherit all methods and attributes of Tree

class AppleTree(Tree):
    # the AppleTree's specific production rule is specifed below
    axiom = "0"
    constants = ["[","]"]                       # a list because it's mutable
    variables = ["0","1"]
    rules = {"1":"11", "0":"1[0]0"}
    maturation_threshold = random.uniform(4, 5) # apple trees start to bear fruit 4-5 years after planting (https://hortnews.extension.iastate.edu/faq/how-soon-will-newly-planted-fruit-tree-begin-bear-fruit#:~:text=Rootstocks%20have%20little%20effect%20on,plum%20%2D%203%20to%205%20years.)
    disease_threshold = 9                       # the year number at which a disease starts affecting some tree branches
    disease_severity = 6                         # this number, within the [1,10] range, represents the severity level of the disease - highest for apples, then plums, then pairs based on literature (https://ptes.org/campaigns/traditional-orchard-project/orchard-practical-guides/fruit-tree-health/orchard-fruit-tree-diseases/)
                                                # it can be an integer or float, the higher it is, the more branches are affected
    apple_form = random.randrange(30,45)        # determine the form of the apple tree based off literature (https://douglas.extension.wisc.edu/files/2015/05/Training-and-Pruning-Apple-Trees.pdf)
    
    # the "instances" list below keeps track of all instances that will be generated
    instances = []
    
    
    def __init__(self, idnr, string, fruits=None):
        """This initializes any instance of an AppleTree, namely, we define the
        attributes of each specific and unique apple tree; It also registers it in the "instances" list"""
        self.id = idnr
        self.string = string
        self.fruits = fruits
        AppleTree.instances.append(self)
       
    
    def __str__(self):
        return "AppleTree nr.: "+ str(self.id) +" with tree string: "+ self.string + "and nr. of fruits: "+ str(self.fruits)
    
    
    # (https://harvesttotable.com/how_to_grow_apples/#:~:text=Apples%20can%20grow%20from%2010,harvest%20depending%20upon%20the%20variety.)
    # (https://hortnews.extension.iastate.edu/2000/9-15-2000/apples.html)
    # (https://wikifarmer.com/apple-tree-harvest-yields/#:~:text=A%20very%20good%20yield%20for,80%2D150%20fruits%20per%20season.)

    # apples are harvested once per year 
    # fruit produced in one harvest per year of 100-200 days long is 80-150 apples

    # function to generate the number of apples harvest per year on a single apple tree over the given time line. 
    # the number is in accordance with the relevant literature
    # this number is also consistent with the assignment requirements: it is assumed that apples are located at the tip of the branches, but at each tip more (or less) than one apple can exist 
    # conversely, if one and one only apple were present at each tip, as the tree grows over time, apples would increase exponentially and more unrealistically
   

    def apples_per_year(year, t_string):
        """calculate how many apples per year are generated on a single tree over the given time line"""

        if year < AppleTree.maturation_threshold:
            harvest = 0

        else:
            harvest = random.randint(80,150)
            
            #count the number of branches (where we define a branch as a part of the tree that starts from the first bifurcation
            #and terminate in its own unique tip). This definition is operational rather than conceptual, because it allows to 
            #univoquely identify each branch by their unique tip, which is characterized by a "0" in the tree string.
            branch_count = 0
            for c in t_string:
                if c =="0":
                    branch_count += 1
            avg_harvest_per_branch = round(harvest/branch_count)
            
            if year >= AppleTree.disease_threshold:
                n_affected_trees = round(branch_count/(11-AppleTree.disease_severity))
                harvest = round(harvest - n_affected_trees * avg_harvest_per_branch)
            
        return harvest
    
    
    def generate_trees(tree_n, tree_age):
        """This function generates multiple apple tree instances of a desired age.
        tree_n: number of apple tree instances to generate
        tree_age: age of each apple tree instance generated
        apple tree variable names: at0, at1, ..., atN where N = tree_n-1"""
        
        # empty the Apple Tree instances list from possible previous instantiations
        AppleTree.instances = []

        for i in range(tree_n):
            # generate each tree's string, at the specified age
            at_string = Tree.tree_string(AppleTree.axiom, AppleTree.constants, AppleTree.variables, AppleTree.rules, tree_age)             
            
            # calculate for each tree, the number of apples it has, at the specified age
            at_fruits = AppleTree.apples_per_year(tree_age, at_string)
            
            # generate each tree instance with their (1) idnr, (2) tree string and (3) nr of fruits, and store it in a variable 
            # note: their names will be at0, at1, ..., atN where N is the specified tree_n-1
            globals()["at" + str(i)] = AppleTree(i, at_string, at_fruits)
    
    
    def plot_one_tree(t_string):
        """This function plots the tree corresponding to a specific tree string"""
        # positions and heading angles are stored in a list of tuples
        locations = []
        
        # for the axiom, a short upright stick is drawn as default
        t.setheading(90)
        t.forward(random.randrange(10,90))

        for c in t_string:
            if c == "0":
                t.color("red")
                t.forward(random.randrange(20,140))
            elif c == "1":
                t.color("brown")
                t.forward(random.randrange(5,60))
            elif c == "[":
                locations.append( ( t.pos(),t.heading() ) ) # push position and heading angle
                t.left(AppleTree.apple_form)
                t.color("brown")
            elif c == "]":
                # move to the last location's stored and retake the same heading angle,
                # without drawing while moving
                t.penup()
                t.goto(locations[-1][0])
                t.setheading(locations[-1][1])
                del locations[-1]
                t.pendown()

                t.right(AppleTree.apple_form)
            else:
                print("a character in the tree string does not have an associated drawing operation")

                
    def plot_all_trees():
        # set the world coordinates, based on how many trees need to fit in it
        llx=-4000
        lly=-4000
        urx=4000
        ury=4000

        xdist = 500
        for varname in AppleTree.instances:
            t.setworldcoordinates(llx, lly, urx, ury)

            t.penup()
            t.setpos(llx + xdist, lly)
            t.pendown()
            AppleTree.plot_one_tree(varname.string)

            # the horizontal distance between apple tree drawings
            xdist += 1200 

            
            
# Pear Tree is a specific species of tree, subclasses of Tree, and is defined here
# they inherit all methods and attributes of Tree

class PearTree(Tree):
    # the PearTree's specific production rule is specifed below
    axiom = "0"
    constants = ["[","]"]                       # a list because it's mutable
    variables = ["0","1"]
    rules = {"1":"11", "0":"1[0]10"}
    maturation_threshold = random.uniform(4, 6) # pear trees start to bear fruit 4-6 years after planting (https://hortnews.extension.iastate.edu/faq/how-soon-will-newly-planted-fruit-tree-begin-bear-fruit#:~:text=Rootstocks%20have%20little%20effect%20on,plum%20%2D%203%20to%205%20years.)
    disease_threshold = 9                       # the year number at which a disease starts affecting some tree branches
    disease_severity = 4                        # this number, within the [1,10] range, represents the severity level of the disease
                                                # it can be an integer or float, the higher it is, the more branches are affected -  highest for apples, then plums, then pairs based on literature (https://ptes.org/campaigns/traditional-orchard-project/orchard-practical-guides/fruit-tree-health/orchard-fruit-tree-diseases/)
    pear_form = random.randrange(30,35)        # determine the form of the pear tree based off literature (https://www.ehow.com/facts_7173569_difference-between-apple-pear-tree.html)
    
    # the "instances" list below keeps track of all instances that will be generated
    instances = []
    
    
    def __init__(self, idnr, string, fruits=None):
        """This initializes any instance of a PearTree, namely, we define the
        attributes of each specific and unique pear tree; It also registers it in the "instances" list"""
        self.id = idnr
        self.string = string
        self.fruits = fruits
        PearTree.instances.append(self)
       
    
    def __str__(self):
        return "PearTree nr.: "+ str(self.id) +" with tree string: "+ self.string + "and nr. of fruits: "+ str(self.fruits)
    
 
    # (https://homeguides.sfgate.com/long-grow-pears-79479.html#:~:text=Time%20Frame&text=Once%20pear%20trees%20become%20established,for%2075%20years%20or%20longer.)
    # (https://wikifarmer.com/pear-tree-harvest-and-yield/#:~:text=Pear%20Tree%20Yield,pear%20tree%20is%20200%20lbs.)
    # (http://www.taglianivivai.it/en/pears/#:~:text=FRUIT%3A%20The%20fruits%20have%20a,g)%20with%20good%20taste%20qualities.)

    # pears  are harvest once per year 
    # fruit produced in one harvest per year of 115-165 days long is 45-90 kg of pears
    # average pear weighs 190 g
    # thus, average number of pears grown per harvest:
    # 45 kg: [(45 kg) * (1000 g/kg)] / 190 g = 236.84 ~ 237
    # 90 kg: [(90 kg) * (1000 g/kg)] / 190 g = 473.68 ~ 474

    # function to generate the number of pears harvest per year on a single pear tree over the given time line
    # the number is in accordance with the relevant literature
    # this number is also consistent with the assignment requirements: it is assumed that pears are located at the tip of the branches, but at each tip more (or less) than one pear can exist 
    # conversely, if one and one only pear were present at each tip, as the tree grows over time, pears would increase exponentially and more unrealistically
    
    
    def pears_per_year(year, t_string):
        """calculate how many pears per year are generated on a single tree over the given time line"""

        if year < PearTree.maturation_threshold:
            harvest = 0

        else:
            harvest = random.randint(237,474)
            
            #count the number of branches (where we define a branch as a part of the tree that starts from the first bifurcation
            #and terminate in its own unique tip). This definition is operational rather than conceptual, because it allows to 
            #univoquely identify each branch by their unique tip, which is characterized by a "0" in the tree string.
            branch_count = 0
            for c in t_string:
                if c =="0":
                    branch_count += 1
            avg_harvest_per_branch = round(harvest/branch_count)
            
            if year >= PearTree.disease_threshold:
                n_affected_trees = round(branch_count/(11-PearTree.disease_severity))
                harvest = round(harvest - n_affected_trees * avg_harvest_per_branch)
            
        return harvest

    
    def generate_trees(tree_n, tree_age):
        """This function generates multiple pear tree instances of a desired age.
        tree_n: number of pear tree instances to generate
        tree_age: age of each pear tree instance generated
        pear tree variable names: at0, at1, ..., atN where N = tree_n-1"""
        
        # empty the Pear Tree instances list from possible previous instantiations
        PearTree.instances = []

        for i in range(tree_n):
            # generate each tree's string, at the specified age
            at_string = Tree.tree_string(PearTree.axiom, PearTree.constants, PearTree.variables, PearTree.rules, tree_age)             
            
            # calculate for each tree, the number of pears it has, at the specified age
            at_fruits = PearTree.pears_per_year(tree_age, at_string)
            
            # generate each tree instance with their (1) idnr, (2) tree string and (3) nr of fruits, and store it in a variable 
            # note: their names will be at0, at1, ..., atN where N is the specified tree_n-1
            globals()["at" + str(i)] = PearTree(i, at_string, at_fruits)
    
    
    def plot_one_tree(t_string):
        """This function plots the tree corresponding to a specific tree string"""
        # positions and heading angles are stored in a list of tuples
        locations = []
        
        # for the axiom, a short upright stick is drawn as default
        t.setheading(90)
        t.forward(random.randrange(50,130))

        for c in t_string:
            if c == "0":
                t.color("green")
                t.forward(random.randrange(20,140))
            elif c == "1":
                t.color("brown")
                t.forward(random.randrange(5,60))
            elif c == "[":
                locations.append( ( t.pos(),t.heading() ) ) # push position and heading angle
                t.left(PearTree.pear_form)
                t.color("brown")
            elif c == "]":
                # move to the last location's stored and retake the same heading angle,
                # without drawing while moving
                t.penup()
                t.goto(locations[-1][0])
                t.setheading(locations[-1][1])
                del locations[-1]
                t.pendown()

                t.right(PearTree.pear_form)
            else:
                print("a character in the tree string does not have an associated drawing operation")

        
    def plot_all_trees():
        # set the world coordinates, based on how many trees need to fit in it
        llx=-4000
        lly=-4000
        urx=4000
        ury=4000

        xdist = 500
        for varname in PearTree.instances:
            t.setworldcoordinates(llx, lly, urx, ury)

            t.penup()
            t.setpos(llx + xdist, lly + 2000)
            t.pendown()
            PearTree.plot_one_tree(varname.string)

            # the horizontal distance between pear tree drawings
            xdist += 1700 

            
            
# Plum Tree is a specific species of tree, subclasses of Tree,and is defined here
# they inherit all methods and attributes of Tree

class PlumTree(Tree):
    
    # the PlumTree's specific production rule is specifed below
    axiom = "0"
    constants = ["[","]"]                       # a list because it's mutable
    variables = ["0","1"]
    rules = {"1":"11", "0":"1[0][0]0"}
    maturation_threshold = random.uniform(3, 5) # plum trees start to bear fruit 3-5 years after planting (https://hortnews.extension.iastate.edu/faq/how-soon-will-newly-planted-fruit-tree-begin-bear-fruit#:~:text=Rootstocks%20have%20little%20effect%20on,plum%20%2D%203%20to%205%20years.)
    disease_threshold = 9                       # the year number at which a disease starts affecting some tree branches
    disease_severity = 5                        # this number, within the [1,10] range, represents the severity level of the disease
                                                # it can be an integer or float, the higher it is, the more branches are affected -  highest for apples, then plums, then pairs based on literature (https://ptes.org/campaigns/traditional-orchard-project/orchard-practical-guides/fruit-tree-health/orchard-fruit-tree-diseases/)
    plum_form = random.randrange(20,30)        # determine the form of the plum tree based off literature (https://www.starkbros.com/growing-guide/article/fruit-tree-sizes)
    
    # the "instances" list below keeps track of all instances that will be generated
    instances = []
    
    
    def __init__(self, idnr, string, fruits=None):
        """This initializes any instance of a PlumrTree, namely, we define the
        attributes of each specific and unique plum tree; It also registers it in the "instances" list"""
        self.id = idnr
        self.string = string
        self.fruits = fruits
        PlumTree.instances.append(self)
       
    
    def __str__(self):
        return "PlumTree nr.: "+ str(self.id) +" with tree string: "+ self.string + "and nr. of fruits: "+ str(self.fruits)
    
    
    # (https://greenupside.com/when-does-a-plum-tree-produce-fruit/) harvest once per year;  kgs of plum per year
    # (https://hannaone.com/Recipe/weightplums.html) weight of plum
    
    # plums are harvested once per year
    # fruit produced in one harvest per year is 68-136 kg of plums
    # average plum weighs 225 g
    # thus, average number of plums grown per harvest:
    # 68 kg: [(68 kg) * (1000 g/kg)] / 225 g = 302.22 ~ 302
    # 136 kg: [(136 kg) * (1000 g/kg)] / 225 g = 604.44 ~ 604
    

    # function to generate the number of plums harvest per year on a single plums tree over the given time line 
    # the number is in accordance with the relevant literature
    # this number is also consistent with the assignment requirements: it is assumed that plums are located at the tip of the branches, but at each tip more (or less) than one plum can exist 
    # conversely, if one and one only plum were present at each tip, as the tree grows over time, plums would increase exponentially and more unrealistically.
    
    
    def plums_per_year(year, t_string):
        """calculate how many plums per year are generated on a single tree over the given time line"""

        if year < PlumTree.maturation_threshold:
            harvest = 0

        else:
            harvest = random.randint(302,604)
            
            # count the number of branches (where we define a branch as a part of the tree that starts from the first bifurcation
            # and terminate in its own unique tip). This definition is operational rather than conceptual, because it allows to 
            # univoquely identify each branch by their unique tip, which is characterized by a "0" in the tree string.
            branch_count = 0
            for c in t_string:
                if c =="0":
                    branch_count += 1
            avg_harvest_per_branch = round(harvest/branch_count)
            
            if year >= PlumTree.disease_threshold:
                n_affected_trees = round(branch_count/(11-PlumTree.disease_severity))
                harvest = round(harvest - n_affected_trees * avg_harvest_per_branch)
            
        return harvest

    
    def generate_trees(tree_n, tree_age):
        """This function generates multiple plum tree instances of a desired age.
        tree_n: number of plum tree instances to generate
        tree_age: age of each plum tree instance generated
        plum tree variable names: at0, at1, ..., atN where N = tree_n-1"""
        
        # empty the Plum Tree instances list from possible previous instantiations
        PlumTree.instances = []

        for i in range(tree_n):
            # generate each tree's string, at the specified age
            at_string = Tree.tree_string(PlumTree.axiom, PlumTree.constants, PlumTree.variables, PlumTree.rules, tree_age)             
            
            # calculate for each tree, the number of plums it has, at the specified age
            at_fruits = PlumTree.plums_per_year(tree_age, at_string)
            
            # generate each tree instance with their (1) idnr, (2) tree string and (3) nr of fruits, and store it in a variable 
            # note: their names will be at0, at1, ..., atN where N is the specified tree_n-1
            globals()["at" + str(i)] = PlumTree(i, at_string, at_fruits)
    
    
    def plot_one_tree(t_string):
        """This function plots the tree corresponding to a specific tree string"""
        # positions and heading angles are stored in a list of tuples
        locations = []
        
        # for the axiom, a short upright stick is drawn as default
        t.setheading(90)
        t.forward(random.randrange(30,100))

        for c in t_string:
            if c == "0":
                t.color("purple")
                t.forward(random.randrange(10,100)) #20,140
            elif c == "1":
                t.color("brown")
                t.forward(random.randrange(10,70)) #5,60
            elif c == "[":
                locations.append( ( t.pos(),t.heading() ) ) # push position and heading angle
                t.left(PlumTree.plum_form)
                t.color("brown")
            elif c == "]":
                # move to the last location's stored and retake the same heading angle,
                # without drawing while moving
                t.penup()
                t.goto(locations[-1][0])
                t.setheading(locations[-1][1])
                del locations[-1]
                t.pendown()

                t.right(PlumTree.plum_form)
            else:
                print("a character in the tree string does not have an associated drawing operation")

        
    def plot_all_trees():
        # set the world coordinates, based on how many trees need to fit in it
        llx=-4000
        lly=-4000
        urx=4000
        ury=4000

        xdist = 500 
        for varname in PlumTree.instances:
            t.setworldcoordinates(llx, lly, urx, ury)

            t.penup()
            t.setpos(llx + xdist, lly + 4000)
            t.pendown()
            PlumTree.plot_one_tree(varname.string)

            # the horizontal distance between plum tree drawings
            xdist += 1700 
            
        t.done()
        
        
        
# for analysis: print and plot the polynomial model (from CS4305TU Applied Machine Learning Course: Week 2: Supervised Regression, notebook: 06_polynomial_linear_regression)
def print_model(coef):
    print("-" * 70)
    print(np.poly1d(coef[::-1]))
    print("-" * 70)


def plot_poly(ax, x, coef):
    x_ = np.linspace(min(x), max(x), 100)
    y_ = np.zeros(len(x_))
    for i, c in enumerate(coef):
        y_ += c * x_**i
    ax.plot(x_, y_)