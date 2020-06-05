# Function Definition
### Overall Format:
In order to define any function in python, user has to say the following format:

    define function {name_of_the_function} parameters {name_of_the_parameters} end of parameters
    
 and also between every parameter, the user has to say `next`. 
 for example:

    define function hello world parameters name end of parameters

and the code which will be generated is:

    def hello_world(name):

and after that, the body of the function should be defined. Finally, when the function is finished, the user has to say
`end of function`.