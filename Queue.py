from collections import deque

class Queue(deque):
    """Queue implementation using deque container from the collections module"""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name + " [" + ", ".join(repr(item) for item in self)  + "]"
    def empty(self):
        """
        Returns whether the queue is empty
        """
        return len(self) == 0
    def size(self):
        """
        Returns the length of the queue
        """
        return len(self)
    def push(self, x):
        """
        Appends the element or elements at the end of the queue
        """
        if(isinstance(x, str)):
            self.append(x)
        else:
            try:
                iterator = iter(x)
            except TypeError:
                # not iterable
                self.append(x)
            else:
                # iterable
                self.extend(x)
    def pop(self):
        """
        Returns and removes the first element in the queue
        """
        return self.popleft()
    def top(self):
        """
        Returns the first element in the queue
        """
        return self[0]

