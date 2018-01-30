from sets import Set
import collections


def find_unique_classifications(examples,attribute, attributes):
    
    x = 0;

    for inst in attributes:

        if inst == attribute:

            values = examples[x]
        x+=1

    final_classifications = list(set(values))

    return final_classfications

def get_frequencies(examples, attribute, attributes):


    frequency_dict = {}

    classifications = find_unique_classifications(examples, attribute, attributes)


    for i in classifications:

        frequency_dict.update({i:0})
        
    for i in examples:
        
        if (frequency_dict.has_key(examples[i])):
            
            frequency_dict[examples[i]] += 1.0

    return frequency_dict

        

def get_entropy(examples, attribute, attributes):

    entropy = 0.0

    frequency_dict = get_frequencies(examples, attribute, attributes)

    for pi in frequency_dict.values():

        entropy += (-pi/len(examples)) * math.log(pi/len(examples), 2)

    return entropy

def get_class_list(examples, classification, attribute, attributes)


    index = attributes.index(attribute)

    class_list = []

    for i in examples[index]:

        if i ==classification:

            class_list.append(i)

    return class_list

    

def gain(examples,classification_attribute, attributes, i):

    frequency_dict = get_frequencies(examples, attribute, attributes)

    total_element_gain = 0.0

    set_entropy = get_entropy(examples, classification_attribute, attributes)

    attribute_entropy = 0.0

    total_values = sum(frequency_dict.values())

    for i in frequency_dict.key():

        classification_list = get_class_list(examples, i, attribute, attributes)
        
        probability = frequency_dict[i]/total_values

        attribute_entropy += probability * entropy(classification_list, i, attributes)


    total_element_gain = set_entropy - attribute_entropy

    return total_element_gain

    
            
                 
def id3(examples, attributes, classification_attribute):

    best_attribute = attributes[0]

    max_info_gain = 0

    for i in attributes:

        tmp_info_gain = entropy_lost(examples, classification_attribute, attributes, i)

        if tmp_info_gain > max_info_gain:

            best_attribute = i
            max_info_gain = tmp_info_gain

    return best_attribute     

def build_tree(examples, classification_attribute, attributes):

    
 #   for i in attributes:

 #       if  (len(find_unique_classifications(examples, i, attributes)) == 1):

            
 #   if len(examples) == 0:

 #       return 

   # else:

    best_attribute = id3(examples, attributes, classification_attribute)

    Decision_tree = {best:{}}


    for i in find_unique_classifications(examples, best_attribute, attributes):
        
        next_attributes = attributes[:]
        next_attributes.pop(best_attribute)
        next_examples = find_new_examples(examples, best_attribute, attributes, i)
        next_sub_tree = build_tree(next_examples, classification, next_attributes)

        Decision_tree[best_attribute][i]= next_sub_tree

    return Decision_tree

                
        
                                
            
            
        
    

    
