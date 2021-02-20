<div style="text-align: right"> by Arely Aceves Compean </div>

# Data Structures

* [Stack](#Stack)

* [Queue](#Queue)

* [Dictionary](#Dictionary)

Repository with implementations available [here](https://github.com/ArelyA/TC3048.2/tree/main/Tarea1).

File with all the sample code available [here](https://github.com/ArelyA/TC3048.2/blob/main/Tarea1/main.py)

## Stack
### Basic Methods
* Stack(element) --> Stack
	
	Creates a new stack. If element is not iterable, the stack will not be created and a TypeError will be thrown. If there are no elements specified, then an empty Stack will be created.
```python
stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
print(stack)
>> ['Eric', 'John','Michael']
print(empty_stack)
>> []
```

* empty() --> None
	
	Returns whether the stack is empty.
```python
print(stack.empty())
>> True
print(empty_stack.empty())
>> False
```

* size() --> int
	
	Returns the length of the stack.
```python
print(stack.size())
>> 3
```

* push(element) --> None
	
	Appends the element or elements to the end of the stack.
```python
stack.push("Sophia")
print(stack)
>> ['Eric', 'John','Michael','Sophia']
stack.push(["Anna","Arthur","Tom"])
print(stack)
>> ['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']
```

* pop() --> Object
	
	Removes the last item of the stack and returns it.
```python
name = stack.pop()
print(name)
>>Tom
print(stack)
>> ['Eric', 'John','Michael','Sophia','Anna','Arthur']
```

* copy() --> Stack

  Returns a copy of the stack.
```python
stack_copy = stack.copy()
print(stack_copy)
>> ['Eric', 'John','Michael','Sophia','Anna','Arthur']
```

* clear() --> None
	
	Removes all the items from the stack.
```python
stack.clear()
print(stack)
>>[]
```

### Implementation
Stack implementation using list container available [here](https://github.com/ArelyA/TC3048.2/blob/main/Tarea1/Stack.py).
## Queue
### Basic Methods
* Queue(element) --> Queue
	
	Creates a new queue. If element is not iterable, the queue will not be created and a TypeError is raised. If there are no elements specified, then an empty queue will be created.
```python
queue = Queue(["Eric", "John", "Michael"])
empty_queue = Stack()
print(queue)
>> Queue(['Eric', 'John','Michael'])
print(empty_queue)
>> Queue([])
```

* empty() --> None
	
	Returns whether the stack is empty.
```python
queue = Queue(["Eric", "John", "Michael"])
empty_queue = Stack()
print(queue.empty())
>> True
print(empty_queue.empty())
>> False
```

* size() --> int
	
	Returns the length of the stack.
```python
print(queue.size())
>> 3
```

* push(element) --> None
	
	Appends the element or elements to the end of the stack.
```python
queue.push("Sophia")
print(queue)
>> Queue(['Eric', 'John','Michael','Sophia'])
queue.push(["Anna","Arthur","Tom"])
print(queue)
>> Queue(['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom'])
```

* pop() --> Object
	
	Removes the first item of the stack and returns it.
```python
name = queue.pop()
print(name)
>> Eric
print(queue)
>> Queue(['John','Michael','Sophia','Anna','Arthur','Tom'])
```

* copy() --> Queue

  Returns a copy of the queue.
```python
queue_copy = queue.copy()
print(queue_copy)
>> Queue(['John','Michael','Sophia','Anna','Arthur','Tom'])
```

* clear() --> None
	
	Removes all the items from the stack.
```python
queue.clear()
print(queue)
>> Queue([])
```

### Implementation
Queue implementation using deque container from the collections module available [here](https://github.com/ArelyA/TC3048.2/blob/main/Tarea1/Queue.py).

## Dictionary

* Creation through comma-separated list of key: value pairs
```python
dictionary = {'one': 1, 'two': 2, 'three': 3}
print(dictionary)
>> {'one': 1, 'two': 2, 'three': 3}
```

* Creation through dict comprehension

```python
dictionary_compr = dict(one=1, two=2, three=3)
print(dictionary_compr)
>> {'one': 1, 'two': 2, 'three': 3}
```

* Creation through type constructor dict() 
```python
dictionary_constr = dict(one=1, two=2, three=3)
print(dictionary_constr)
>> {'one': 1, 'two': 2, 'three': 3}
```
* d[key] --> Object

  Returns dictionary value of item at key.
```python
print(dictionary['one'])
>> 1
```

* d[key] = value

  Sets value of item at key.
```python
dictionary['one'] = 11
print(dictionary['one'])
>> 11
```

* setsefault(key, default) --> Object

  Returns the value of the item with the specified key, if it does not exists, this item is added with the specified default value. If there is no default,  its value is set to None.
```python
element = dictionary.setdefault('four', 4)
print(element)
>> 4
element = dictionary.setdefault('five')
print(element)
>> None
```

* key in d --> bool

  Returns whether a key exists in the dictionary.
```python
print('six' in dictionary)
>> False
print('two' in dictionary)
>> True
```

* key not in d --> bool

  Returns whether a key does not exist in the dictionary. Equivalent to not key in d.
```python
print('six' not in dictionary)
>> True
print(not 'six' in dictionary)
>> True
print('two' not in dictionary)
>> False
print(not 'two' in dictionary)
>> False
```

* keys() --> dict view

  Returns a view of all the keys in the dictionary.
```python
print(dictionary.keys())
>> dict_keys(['one', 'two', 'three', 'four', 'five'])
```

* list(d) --> list

  Returns a list of
```python
print(list(dictionary))
>> ['one', 'two', 'three', 'four', 'five']
```
* values() --> dict view

  Returns a view of all the values in the dictionary.
```python
print(dictionary.values())
>> dict_values([1, 2, 3, 4, None])
```

* get(key, default) --> Object

  Returns the value of the item with the specified key, if it does not exists the specified default value is returned. If there is no default value it returns None.
```python
element = dictionary.get('four', 6)
print(element)
>> 4
element = dictionary.get('six', 6)
print(element)
>> 6
element = dictionary.get('six')
print(element)
>> None
```

* pop(key) --> Object

  Removes and returns the value of the item with the specified key, if it does not exists the specified default value is returned. If there is no default value, a KeyError is raised.
```python
element = dictionary.pop('four', 6)
print(element)
>> 4
print(dictionary)
>> {'one': 1, 'two': 2, 'three': 3, 'five': None}
element = dictionary.pop('six', 6)
print(element)
>> 6
try:
    element = dictionary.pop('six')
except KeyError:
    print(KeyError)
>> <class 'KeyError'>
```

* del d[key] --> None

  Removes item at key. Raises a KeyError if key does not exist.
```python
del dictionary['five']
print(dictionary)
>> {'one': 1, 'two': 2, 'three': 3}
try:
    del dictionary['five']
except KeyError:
    print(KeyError)
>> <class 'KeyError'>
```

* update(d2) --> None

  Updates the dictionary with the keys and values of d2, giving priority to d2.
```python
dictionary.update({'four': 1, 'five': 2, 'six': 3})
print(dictionary)
>> {'one': 1, 'two': 2, 'three': 3, 'four': 1, 'five': 2, 'six': 3}
```
* len(d) --> int

  Returns number of elements in the dictionary.
```python
print(len(dictionary))
>> 6
```

* clear() --> None
	
	Removes all the items from the dictionary.
```python
dictionary.clear()
print(dictionary)
>> {}
```

### Implementation
Dictionary implementation using dict container shown in previous code examples.