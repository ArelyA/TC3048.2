# Data Structures

* [Stack](#Stack)

* [Queue](#Queue)

* [Dictionary](#Dictionary)

Repository with implementations available [here](https://github.com/ArelyA/TC3048.2/tree/main/Tarea1).

## Stack
### Basic Methods
* empty() --> None
	Returns whether the stack is empty.
```python
stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
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
>>['Eric', 'John','Michael','Sophia']
stack.push(["Anna","Arthur","Tom"])
print(stack)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']
```

* pop() --> None
	Removes the last item of the stack and returns it.
```python
name = stack.pop()
print(name)
>>Tom
print(stack)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur']
```

* clear() --> None
	Removes all the items from the stack.
```python
stack.clear()
print(stack)
>>[]
```

### [Implementation](https://github.com/ArelyA/TC3048.2/blob/main/Tarea1/Stack.py)
Stack implementation using list container.
## Queue
### Basic Methods
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
>>['Eric', 'John','Michael','Sophia']
queue.push(["Anna","Arthur","Tom"])
print(queue)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']
```

* pop() --> None
	Removes the first item of the stack and returns it.
```python
name = queue.pop()
print(name)
>>Eric
print(queue)
>>['John','Michael','Sophia','Anna','Arthur','Tom']
```

* clear() --> None
	Removes all the items from the stack.
```python
queue.clear()
print(queue)
>>[]
```

### [Implementation](https://github.com/ArelyA/TC3048.2/blob/main/Tarea1/Queue.py)
Queue implementation using deque container from the collections module.

## Dictionary