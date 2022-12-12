"""
Course: CSE 251, week 14
File: common.py
Author: Jaxon Hamm

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

Describe how to speed up part 1

The speed up comes from adding more threads as more operations become available.
Because the server takes time to respond to our request for informtion, the more
threads we have the faster the process becomes. Adding these threads flat out
brings the runtime to about 4.5 seconds on my computer. I was able to further speed
up the process by adding operations in between the starts and joins. This way,
while the server was sleeping (.25 seconds per request) other tasks were able to be performed.


Describe how to speed up part 2

<Add your comments here>


10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # Exit
    if family_id is None:
        return

    # Get the family and add it to the tree.
    fam_request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    fam_request.start()
    fam_request.join()
    family = Family(family_id, fam_request.response)
    tree.add_family(family)

    #  Get each person
    husband_request = Request_thread(f'{TOP_API_URL}/person/{family.husband}')
    husband_request.start()
    
    wife_request = Request_thread(f'{TOP_API_URL}/person/{family.wife}')
    wife_request.start()
    
    children_requests = [Request_thread(f'{TOP_API_URL}/person/{child_id}') for child_id in family.children]
    for thread in children_requests:
        thread.start()
    
    husband_request.join()
    wife_request.join()
    
    # Avoid race between recursion call trying to add person as child and this call trying to add.
    # Race condition is now impossible.
    husband = Person(husband_request.response)
    wife = Person(wife_request.response)
    tree.add_person(husband)
    tree.add_person(wife)

    for thread in children_requests:
        thread.join()

    husband_fam = threading.Thread(target=depth_fs_pedigree, args=(husband.parents, tree))
    wife_fam = threading.Thread(target=depth_fs_pedigree, args=(wife.parents, tree))
    husband_fam.start()
    wife_fam.start()

    # Add Family to tree while the threads are working
    kidos = []
    for child in children_requests:
        kidos.append(Person(child.response))
    for kid in kidos:
        if not tree.does_person_exist(kid.id):
            tree.add_person(kid)

    # Join the threads and exit
    husband_fam.join()
    wife_fam.join()

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # TODO - implement breadth first retrieval
    # This is done by doing each 
    print('WARNING: BFS function not written')

    pass


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')

    pass
