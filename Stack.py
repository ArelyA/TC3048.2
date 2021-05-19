# Stack implementation using list container

class Stack(list):
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

