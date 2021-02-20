from Stack import Stack

stack = Stack(["Eric", "John", "Michael"])
stack_l = Stack(["Eric", "John", "Michael"])
stack_l.push('NO')
print(stack_l)
stack2 = Stack()
stack3 = Stack(["Anna","Arthur","Tom"])
stack.push(stack3)
stack3.push("C")
print(stack.empty())
print(stack2.empty())
print(stack)
print(stack3)
print(stack.size())
name = stack.pop()
print(name)
print(stack)
stack.clear()
print(stack)

from Queue import Queue

queue = Queue(["Eric", "John", "Michael"])
print(queue)
queue.pop()
print(queue)