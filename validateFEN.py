# Code taken from https://gist.github.com/Dani4kor/e1e8b439115878f8c6dcf127a4ed5d3e
# Thank you @Dani4kor on Github (Dani4kor@gmail.com)
import re

def fenPass(fen):
    """
    """
    regexMatch=re.match('\s*^(((?:[rnbqkpRNBQKP1-8]+\/){7})[rnbqkpRNBQKP1-8]+)\s([b|w])\s([K|Q|k|q|-]{1,4})\s(-|[a-h][1-8])\s(\d+\s\d+)$', fen)
    if  regexMatch:
        regexList = regexMatch.groups()
        fen = regexList[0].split("/")
        if len(fen) != 8:
            print("expected 8 rows in position part of fen: {0}".format(repr(fen)))
            return False
        # End if
            
        for fenPart in fen:
            field_sum = 0
            previous_was_digit, previous_was_piece = False,False

            for c in fenPart:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if previous_was_digit:
                        print("two subsequent digits in position part of fen: {0}".format(repr(fen)))
                        return False
                    # End if

                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_piece = False
                elif c == "~":
                    if not previous_was_piece:
                        print("~ not after piece in position part of fen: {0}".format(repr(fen)))
                        return False
                    # End if

                    previous_was_digit, previous_was_piece = False,False
                elif c.lower() in ["p", "n", "b", "r", "q", "k"]:
                    field_sum += 1
                    previous_was_digit = False
                    previous_was_piece = True
                else:
                    print("invalid character in position part of fen: {0}".format(repr(fen)))
                    return False
                #End if
            #End inner for loop

            if field_sum != 8:
                print("expected 8 columns per row in position part of fen: {0}".format(repr(fen)))
                return False
            #End if
        #End outer for loop
        return True
    else: 
        print("fen doesn`t match follow this example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ")
        return False
    #End if