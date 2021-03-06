# qtools
## Library to implement various quantum tools like state discrimination, non local games etc

- ![#f03c15](https://via.placeholder.com/15/f03c15/f03c15.png) `This is in development mode`

### My first addition is NPA hierarchy unlike available libraries this implementation is general for any Bell Scenario and any array of cosntraints.
### You just need to input the Bell Scenario, NPA level and add the non-trivial constraints and the code will take care of the rest.
### If you want to just loop through a list of constraints say in case like you want a plot, you just need to call the add constraints with new constraints.

## Brief Documnetation for NPA module
### Import *NpaHierarchy* class from *NPAsolver.py*
### Instantiate a *NpaHierarchy* object by passing in Bell Scenario and NPA level to class constructor.
### The constructor method takes in *oprArray*, *inputs*, *outputs* and *level* as input
### You can pass in the bell scenario as array like [\<Alice>,\<Bob>,\<Charlie>,...]
#### In \<Alice> or \<Bob> or ..., you need to enter [\<Measurement 1>,\<Measurement 2>,...]
#### In \<Measurement i> for i in (1,2,...),.. you need to enter number of outcomes: this should be non-negative integer
### You can also input in *oprArray* just the number of measurements in <Alice>, <Bob> ,... and  input the number of outcomes for all measurements of Alice bob and charlie using the *outputs* parameter
### In *oprArray* you can also just specifiy the number of parties, and specify the number of inputs and outputs for all parties using *inputs* and *outputs* parameter.
### If *inputs* and *outputs* parameter are left blank and it is required to calculate Bell Scenario, it will default to 2.
### If level is left blank it will do intermediate NPA.

### You can then specify the non-trivial constraints by calling *addConstraints* and passing in array of cosntraints as strings of format:
#### 0.8pab(o_1o_2|i_1i_2)+pabc(o_1o_2o_3|i_1i_2i_3)<=2.5, where i_1,i_2 are first and second inputs and o_1,o_2 are first and second outputs.
### You can similarly pass in objective function as above just without using as equality or inequality.
### For now only <= and = is supported. You can frame in this format if possible. We will be adding more types.
### You can use python fstring to update values in your constraints
