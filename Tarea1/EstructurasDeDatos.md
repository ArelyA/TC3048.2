# Data Structures

* [Stack](#Stack)

* [Queue](#Queue)

* [Dictionary](#Dictionary)

Class repository with implementations available [here](https://github.com/ArelyA/TC3048.2/tree/main/Tarea1)

## Stack
### Basic Methods
* empty() --> None
	Returns whether the stack is empty.
```
stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
print(stack.empty())
>> True
print(empty_stack.empty())
>> False
```
* size() --> int
	Returns the length of the stack.
```
print(stack.size())
>> 3
```
* push(element) --> None
	Appends the element or elements to the end of the stack.
```
stack.push("Sophia")
print(stack)
>>['Eric', 'John','Michael','Sophia']
stack.push(["Anna","Arthur","Tom"])
print(stack)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']
```
* pop() --> None
	Removes the last item of the stack and returns it.
```
name = stack.pop()
print(name)
>>Tom
print(stack)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur']
```
* clear() --> None
	Removes all the items from the stack.
```
stack.clear()
print(stack)
>>[]
```
### [Implementation](Stack.py)
Stack implementation using list container.
## Queue
### Basic Methods
* empty() --> None
	Returns whether the stack is empty.
```
queue = Queue(["Eric", "John", "Michael"])
empty_queue = Stack()
print(queue.empty())
>> True
print(empty_queue.empty())
>> False
```
* size() --> int
	Returns the length of the stack.
```
print(queue.size())
>> 3
```
* push(element) --> None
	Appends the element or elements to the end of the stack.
```
queue.push("Sophia")
print(queue)
>>['Eric', 'John','Michael','Sophia']
queue.push(["Anna","Arthur","Tom"])
print(queue)
>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']
```
* pop() --> None
	Removes the first item of the stack and returns it.
```
name = queue.pop()
print(name)
>>Eric
print(queue)
>>['John','Michael','Sophia','Anna','Arthur','Tom']
```
* clear() --> None
	Removes all the items from the stack.
```
queue.clear()
print(queue)
>>[]
```
### [Implementation](Queue.py)
Queue implementation using deque container from the collections module.

## Dictionary