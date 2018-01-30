import re
import csv 
import math

#globals
#index of classification_attribute wihtin csv file
class_attr = 5
examples = []
attributes = []
tree = [[]]
root = 0


def build_tree(examples, classification_attribute, attributes):
    #   for i in attributes:
    #       if  (len(find_unique_classifications(examples, i, attributes)) == 1):
    #   if len(examples) == 0:
    #       return
    # else:
    best_attribute = id3(examples, attributes, classification_attribute)
    Decision_tree = {best: {}}
    for i in find_unique_classifications(examples, best_attribute, attributes):
        next_attributes = attributes[:]
        next_attributes.pop(best_attribute)
        next_examples = find_new_examples(examples, best_attribute, attributes, i)
        next_sub_tree = build_tree(next_examples, classification, next_attributes)
        Decision_tree[best_attribute][i] = next_sub_tree
    return Decision_tree


def find_unique_classifications(examples,attribute, attributes):
    
    x = 0
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


def get_class_list(examples, classification, attribute, attributes):

    index = attributes.index(attribute)
    class_list = []
    for i in examples[index]:
        if i == classification:
            class_list.append(i)

    return class_list


def gain(examples,classification_attribute, attributes, i):

    frequency_dict = get_frequencies(examples, attributes, attributes)
    total_element_gain = 0.0
    set_entropy = get_entropy(examples, classification_attribute, attributes)
    attribute_entropy = 0.0
    total_values = sum(frequency_dict.values())

    for i in frequency_dict.key:
        classification_list = get_class_list(examples, i, attributes, attributes)
        probability = frequency_dict[i]/total_values
        attribute_entropy += probability * get_entropy(classification_list, i, attributes)

    total_element_gain = set_entropy - attribute_entropy

    return total_element_gain


def best_attribute(examples, classification_attribute, attributes):

    max_info_gain = 0.0
    best_attr = attributes[0]
    #calculate the info gain for each attibute and choose the highest
    for attribute in attributes:
        attr_gain = gain(examples, classification_attribute, attributes, 1)
        if attr_gain > max_info_gain:
            max_info_gain = attr_gain
            best_attr = attribute

    return best_attr

                 
def id3(examples, classification_attribute, attributes):

    #If all examples are 'yes': return root w/ 'yes' label; if all examples are 'no': return root w/ 'no' label
    positive = check_labels(examples)[0]
    negative = check_labels(examples)[1]
    if positive == len(examples) - 1:
        tree[root] = 'Yes'
        return tree
    elif negative == len(examples) - 1:
        tree[root] = 'No'
        return tree
    elif len(attributes) == 0:
        tree[root] = 'Yes' if positive > negative else 'No'
        return tree
    else:
        best_attr = best_attribute(examples, classification_attribute, attributes)
        tree[root] = best_attr
        root = root + 1
        # [examples with that value for best_attribute, e.g. sunny/overcast/rain for Outlook
        branch_examples = []
        if len(branch_examples) == 0:
            #add leaf node with most popular classification_attribute label
            positive = check_labels(branch_examples)[0]
            negative = check_labels(branch_examples)[1]
            tree[root] = 'Yes' if positive > negative else 'No'
        else:
            attributes.remove(best_attr)
            tree[root] = id3(branch_examples, classification_attribute, attributes)

def check_labels(examples):
    positive = 0
    negative = 0
    for x in range(1, len(examples)):
        if examples[x][5] == 'Yes ':
            positive = positive + 1
        elif examples[x][5] == 'No ':
            negative = negative + 1

    return [positive, negative]


def main():

    with open('playtennis.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            examples.append(row)

    classification_attr = "play_tennis"
    for attr in examples[0][1:5]:
        attributes.append(attr)
    
    id3(examples, classification_attr, attributes)
    # print(examples)
    # print(len(examples))
    # print("\n")
    # print(attributes)





if __name__ == "__main__":
    main()

    

    
