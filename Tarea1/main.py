"""
Stack
"""
from Stack import Stack

print("\nStack\n")

stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
print(stack)
#>> ['Eric', 'John','Michael']
print(empty_stack)
#>> []

print(stack.empty())
#>> True
print(empty_stack.empty())
#>> False

print(stack.size())
#>> 3

stack.push("Sophia")
print(stack)
#>> ['Eric', 'John','Michael','Sophia']
stack.push(["Anna","Arthur","Tom"])
print(stack)
#>> ['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']

name = stack.pop()
print(name)
#>>Tom
print(stack)
#>> ['Eric', 'John','Michael','Sophia','Anna','Arthur']

stack_copy = stack.copy()
print(stack_copy)
#>> ['Eric', 'John','Michael','Sophia','Anna','Arthur']

stack.clear()
print(stack)
#>>[]

"""
Queue
"""

from Queue import Queue

print("\nQueue\n")

queue = Queue(["Eric", "John", "Michael"])
empty_queue = Queue()
print(queue)
#>> ['Eric', 'John','Michael']
print(empty_queue)
#>> []

print(queue.empty())
#>> True
print(empty_queue.empty())
#>> False

print(queue.size())
#>> 3

queue.push("Sophia")
print(queue)
#>> ['Eric', 'John','Michael','Sophia']
queue.push(["Anna","Arthur","Tom"])
print(queue)
#>> ['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']

name = queue.pop()
print(name)
#>>Eric
print(queue)
#>> ['John','Michael','Sophia','Anna','Arthur','Tom']

queue_copy = queue.copy()
print(queue_copy)
#>> Queue(['John','Michael','Sophia','Anna','Arthur','Tom'])

queue.clear()
print(queue)
#>>[]

"""
Dictionary
"""

print("\nDictionary\n")

dictionary = {'one': 1, 'two': 2, 'three': 3}
print(dictionary)
#>> {'one': 1, 'two': 2, 'three': 3}

dictionary_compr = dict(one=1, two=2, three=3)
print(dictionary_compr)
#>> {'one': 1, 'two': 2, 'three': 3}

dictionary_constr = dict(one=1, two=2, three=3)
print(dictionary_constr)
#>> {'one': 1, 'two': 2, 'three': 3}

element = dictionary.setdefault('four', 4)
print(element)
#>> 4
element = dictionary.setdefault('five')
print(element)
#>> None

print('six' in dictionary)
#>> False
print('two' in dictionary)
#>> True

print('six' not in dictionary)
#>> True
print(not 'six' in dictionary)
#>> True
print('two' not in dictionary)
#>> False
print(not 'two' in dictionary)
#>> False

print(dictionary.keys())
#>> dict_keys(['one', 'two', 'three', 'four', 'five'])

print(list(dictionary))
#>> ['one', 'two', 'three', 'four', 'five']

print(dictionary.values())
#>> dict_values([1, 2, 3, 4, None])

element = dictionary.get('four', 6)
print(element)
#>> 4
element = dictionary.get('six', 6)
print(element)
#>> 6
element = dictionary.get('six')
print(element)
#>> None

element = dictionary.pop('four', 6)
print(element)
#>> 4
print(dictionary)
#>> {'one': 1, 'two': 2, 'three': 3, 'five': None}
element = dictionary.pop('six', 6)
print(element)
#>> 6
print(dictionary)
#>> {'one': 1, 'two': 2, 'three': 3, 'five': None}
try:
    element = dictionary.pop('six')
except KeyError:
    print(KeyError)

del dictionary['five']
print(dictionary)
#>> {'one': 1, 'two': 2, 'three': 3}
try:
    del dictionary['five']
except KeyError:
    print(KeyError)
#>> <class 'KeyError'>

dictionary.update({'four': 1, 'five': 2, 'six': 3})
print(dictionary)
#>> {'one': 1, 'two': 2, 'three': 3, 'four': 1, 'five': 2, 'six': 3}

print(len(dictionary))
#>> 6

dictionary.clear()
print(dictionary)
#>> {}