
class Decision_Tree():

    def init_tree(self, root, left, right, attributes):

        self.root = root
        self.left = left
        self.right = right


    def build(instances, classification_attribute, attributes):


        root = id3(instances, classification_attribute, attributes)

        descision_tree = {root:{}}

        for

    def remove_duplicates(

    def counter(instance, attribute, attributes):

        

        if attribute in attributes:

            for i in instance:

                
        

    def entropy_lost(instances, classification_attribute, attributes, best_attribute):

        

        
        



    def id3(instances, classification_attribute, attributes):

        best_attribute = attributes[0]

        max_info_gain = 0

        for i in attributes:

            tmp_info_gain = entropy_lost(instances, classification_attribute, attributes, i)

            if tmp_info_gain > max_info_gain:

                best_attribute = i
                max_info_gain = tmp_info_gain

        return best_attribute                
                
