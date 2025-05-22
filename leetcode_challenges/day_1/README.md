You are given:

An array nums of length n.
A list of queries, where each query is a range [li, ri].
Each query allows you to decrement elements in nums from index li to ri (inclusive) by at most 1 , but you can choose which positions within that range to decrement — even just some or none. The goal is not to apply all queries, but to remove as many queries as possible , while still being able to reduce the entire array to zero using the remaining queries.

So your task is:

Return the maximum number of queries you can remove , such that the remaining queries are enough to make nums into a zero array (all zeros). 

If it's impossible to convert nums to a zero array with any subset of queries, return -1.






To solve this efficiently (since both n and number of queries are up to 10^5), we need a way to:

Simulate applying queries to track how many times each index is covered.
Ensure that every index i gets at least nums[i] coverage .
This is similar to the interval covering problem with multiplicity.

💡 Approach:
Use a greedy + line sweep technique :

Sort the queries by their starting index (li) to process them in order.
For each index i in nums, track how many times it has been covered by active queries.
Use a difference array or heap to manage the ongoing ranges efficiently.
As you move through the array, activate new queries and deactivate those that have ended.
At each index i, check if current coverage ≥ nums[i]. If not, we cannot make the array zero , return -1.
Keep track of how many queries are used minimally.
Finally, subtract the minimal queries used from the total number of queries to get the max queries removed .





This problem is about coverage — how many times each index is affected by queries.
Think of it like scheduling shifts where each query covers a time window and you want to use the fewest workers (queries).
Greedy + heap helps simulate the active intervals efficiently.