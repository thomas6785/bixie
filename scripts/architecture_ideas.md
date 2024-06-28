Architectural idea:
- Store a lookup table of nodes (nodes or clusters) near to the solved state
- As we branch further from the solved state, the lookup table grows more sparse
- When solving, search to a specified depth (say 5), then find all the lookup states you've encountered and restart the search from the best one
- This means you don't actually have to store the solution, just the states, and the more states you encounter, the closer you are to being solved
- This seems like a bad system tbh


Another idea: Tendrils
    Starting from the solved position, extend 'tendrils' outward into the node space
    Do this either by repeating a single manoeuvre (this will build a ring) or maybe picking random moves (?)
        As much as possible, we want to make sure the route we take is the shortest route to wherever we go (though this algorithm is already not a God's algorithm so it's not a huge problem if this requirement isn't fulfilled)
    As you extend deeper into the cube, maybe let tendrils fork to cover more ground

    So how big does the lookup table have to be?
        There are 2.6875 quintillion clusters of 16 states
        From our starting state, say we can analyse 1 million nearby clusters (this may be ambitious :/ )
        So we'd need 2.6 trillion lookup table entries
        This is at *least* 10 terabytes
    
    What if we do tendrils on both ends?
    Have a database of a bunch of clusters with known solutions
    and keep moving around from our unsolved state in 'tendrils'
    Wait until a collision occurs
    Problem: if we leave gaps in the lookup table, the tendrils may 'miss'
    Solution: widen the tendrils to be 'thick' enough that they will hit any lookup tendril they may come across

    For example, if we only store every 5th cluster in the lookup tendrils, we would move out from our unsolved state in tendrils, and search two clusters on each side of the tendril to ensure we don't miss the stored one

    This idea could be more powerful if we could identify some commonalities of broader clusters than just the 16