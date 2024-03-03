

# Check Input to see if its an int/float or it has any notations
def checkNumInput(input):
    
    print("Before notation: " + str(input))

    # Check if there's a notation
    if 'e' in input:
        # Get index of e and split array based on 
        try: 
            coefficient, exponent = map(float, input.split("e"))
            input = coefficient * pow(10,exponent)
            print("After notation: " + str(input))
        except ValueError:
            print("Invalid Input")
    else:
        try: 
            input = float(input)
        except ValueError:
            print("Invalid Input")
            
    return input


