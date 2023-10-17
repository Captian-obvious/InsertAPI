import rbxm

def FormatUnionParts(f):
    # Load the rbxm file
    file = rbxm.load(f)
    #Sort through the objects in the file.
    for object in file.objects:
        #Check if the object is a UnionOperation
        if isinstance(object, rbxm.UnionOperation):
            #Print the current name of the UnionOperation
            parts = object.Parts
        ##endif
    ##end
##end
