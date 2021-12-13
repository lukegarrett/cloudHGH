import follows_lookup

def convertToRule():
    username="C77228036"
    followed = follows_lookup.getWhoThisUserFollows(follows_lookup.getUserID(username))

    ruleCollection = []
    thisString = ""

    # early inserting first element, then trimming it off
    # so that the rest of the elements will have OR after them
    # lazy way of bounds-checking so we're not left with a trailing OR in a rule
    thisString += ("from:" + followed[0])
    followed = followed[1:]

    for name in followed:
        thisRule = " OR from:" + name
        #need to keep appending while character limit is under 500
        if(len(thisString) + len(thisRule) <= 500):
            thisString += thisRule
        #if we've already hit 5 strings, return error
        elif len(ruleCollection) == 5:
            print("Buffer overflow. Finished with:")
            print(ruleCollection)
            break
        #if character limit is above 500, make new string
        else:
            ruleCollection.append(thisString)
            thisString = ""
            thisRule = "from:" + name
            thisString += thisRule

    if len(ruleCollection) != 5:
        ruleCollection.append(thisString)

    return ruleCollection