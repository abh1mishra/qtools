# qtools
## Library to implement various quantum tools like state discrimination, non local games etc
- ![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png) `Only NPA Hierarchy is implemented for now`

- ![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png) `This is in development mode`
### Overview

- This implementation is general for any Bell Scenario and any array of constraints.
- You just need to input the Bell Scenario, NPA level and add the non-trivial constraints and the code will take care of the rest.
- If you want to just loop through a list of constraints say in case like you want a plot, you just need to call the add constraints with new constraints.

## Methods of Installation
- Start by placing [NPAsolver.py](https://github.com/abh1mishra/qtools/blob/main/NPA/NPAsolver.py) into your project directory along side your driver codes.
- MOSEK and CVXPY are prerequisites.
- Refer the file structure in [NPA Folder](https://github.com/abh1mishra/qtools/tree/main/NPA) where [check.py](https://github.com/abh1mishra/qtools/blob/main/NPA/check.py) is the driver code.

## Instantaiting NpaHierarchy Class
- Import *NpaHierarchy* class from *NPAsolver.py*
```
from NPAsolver import NpaHierarchy
```
- Instantiate a *NpaHierarchy* object by passing in Bell Scenario and NPA level to class constructor. For eg.
```
b=NpaHierarchy(2,level=2)
```
- The constructor method takes in *oprArray*, *inputs*, *outputs* and *level* as input
- You can pass in the bell scenario as array like [\<Alice>,\<Bob>,\<Charlie>,...]
  - In \<Alice> or \<Bob> or ..., you need to enter [\<Measurement 1>,\<Measurement 2>,...]
  - In \<Measurement i> for i in (1,2,...),.. you need to enter number of outcomes: this should be non-negative integer
- You can also input in *oprArray* just the number of measurements in <Alice>, <Bob> ,... and  input the number of outcomes for all measurements of Alice bob and charlie using the *outputs* parameter
- In *oprArray* you can also just specifiy the number of parties, and specify the number of inputs and outputs for all parties using *inputs* and *outputs* parameter.
- If *inputs* and *outputs* parameter are left blank and it is required to calculate Bell Scenario, it will default to 2.
- If level is left blank it will do intermediate NPA.
## Examples of NpaHierarchy object.
- Bipartite Scenario with two input and two outcomes per input and 2nd NPA hierarchy
```
b=NpaHierarchy(2,level=2)
```
- Bipartite Scenario where Alice has 2 inputs with one input with two comes and other input with three outcomes and Bob having three inputs with two outcomes each. The level being intermediate NPA.
```
b=NpaHierarchy(oprArray=[[2,3],[2,2,2]])
```
- Bipartite Bell scenario where each Alice and Bob has three inputs with two outcomes per input(dichotomic) and 3rd NPA hierarchy.
```
b=NpaHierarchy(2,inputs=3,outputs=2,level=3)
```
## Adding Constraints and Objective function:
- You can then specify the non-trivial constraints by calling *addConstraints* and passing in array of constraints as strings of format:
  - 0.8pab(o_1o_2|i_1i_2)+pabc(o_1o_2o_3|i_1i_2i_3)<=2.5, where i_1,i_2 are first and second inputs and o_1,o_2 are first and second outputs. For eg.
```
b.addConstraints([f"pbc(00|10)<=0.25",f"pab(00|10)<=0.25",f"pac(00|01)<=0.25"])
```
- You can similarly pass in objective function as above just without using as equality or inequality.
```
b.addObjective("pa(0|0)-pab(00|00)-pab(00|01)-pab(00|02)+pab(00|10)+pab(10|11)+pb(0|2)-pab(00|12)-pab(10|12)")
```
## Note:
- Now the code suppots a particular form of probability vectors inside addconstraints and addObjective functions.
  - The Probabilties cannot have the last outcome for any input, instead it needs to be written in particular format.
  - The banned probabilties can be expanded by thinking prob. as moments of projectors ($\langle \Pi_a^x \Pi_b^y \rangle$)
  - The prob. with last projector for a given input can then be written as $I(\textrm{identity})-\sum(\textrm{other outcomes of the inputs})$
  - For eg, in CHSH case, pab(10|11)= $\langle (I-\Pi_0^1)_A (\Pi_0^1)_B \rangle = $ pb(0|1)-pab(00|11) 
- For now only <= and = is supported. You can frame in this format if possible. We will be adding more types.
- You can use python fstring to update values in your constraints
