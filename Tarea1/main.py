from Stack import Stack

stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
stack = Stack(["Eric", "John", "Michael"])
empty_stack = Stack()
print(stack)
#>>['Eric', 'John','Michael']
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
#>>['Eric', 'John','Michael','Sophia']
stack.push(["Anna","Arthur","Tom"])
print(stack)
#>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']

name = stack.pop()
print(name)
#>>Tom
print(stack)
#>>['Eric', 'John','Michael','Sophia','Anna','Arthur']

stack.clear()
print(stack)
#>>[]
from Queue import Queue

queue = Queue(["Eric", "John", "Michael"])
empty_queue = Stack()
print(queue)
#>>['Eric', 'John','Michael']
print(empty_queue)
#>> []

queue = Queue(["Eric", "John", "Michael"])
empty_queue = Stack()
print(queue.empty())
#>> True
print(empty_queue.empty())
#>> False

print(queue.size())
#>> 3

queue.push("Sophia")
print(queue)
#>>['Eric', 'John','Michael','Sophia']
queue.push(["Anna","Arthur","Tom"])
print(queue)
#>>['Eric', 'John','Michael','Sophia','Anna','Arthur','Tom']

name = queue.pop()
print(name)
#>>Eric
print(queue)
#>>['John','Michael','Sophia','Anna','Arthur','Tom']

queue.clear()
print(queue)
#>>[]

a = dict(one=1, two=2, three=3)
print(a)