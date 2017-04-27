def new_split_iter( expr ):
    """divide a character string into individual tokens, which need not be separated by spaces (but can be!)
    also, the results are returned in a manner similar to iterator instead of a new data structure
    """
    expr = expr + ';'
    pos = 0
    while expr[pos] != ';':
        current = ''
        if expr[pos] == " ":
            pos += 1
        if expr[pos].isdigit():
            while expr[pos].isdigit():
                current +=expr[pos]
                pos+=1
        elif expr[pos].isalpha():
            while expr[pos].isalpha():
                current += expr[pos]
                pos +=1
        else:
            if expr[pos+1] == "=":
                current += expr[pos]
                current += expr[pos+1]
                pos+=2
            else:
                current = expr[pos]
                pos+=1
        yield current
if __name__ == "__main__":
     print (list( new_split_iter( "12, deff 33+23444 *    5" )))
     print (list( new_split_iter( "deffn fact(n) = n <= 1 ? 1 : n * fact(n-1)" )))