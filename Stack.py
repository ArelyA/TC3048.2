from collections import deque

class Stack(deque):
    """Stack implementation using deque container from the collections module"""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name + " [" + ", ".join(repr(item) for item in self)  + "]"
    def empty(self):
        """
        Returns whether the stack is empty
        """
        return len(self) == 0
    def size(self):
        """
        Returns the length of the stack
        """
        return len(self)
    def push(self, x):
        """
        Appends the element or elements at the end of the stack
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
    def top(self):
        """
        Returns the last element in the stack
        """
        if(self.size() > 1):
            return self[-1]
        else:
            return self[0]
