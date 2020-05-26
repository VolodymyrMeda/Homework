from Queue.linkedqueue import LinkedQueue


def queue_example():
    '''
    Simple example of using LinkedQueue
    '''
    queue = LinkedQueue()

    assert queue.isEmpty() is True
    assert len(queue) == 0  # length of the queue is 0

    for element in range(10):
        queue.add(element)

    assert len(queue) == 10  # length of the queue is 10
    assert queue.isEmpty() is False

    print(queue.pop())  # element 0 is deleted as it was added first

    print(queue.peek())  # as 0 was deleted, 1 is the next element

    assert len(queue) == 9  # length of the queue is 9
    assert queue.isEmpty() is False
