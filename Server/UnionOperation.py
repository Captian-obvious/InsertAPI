import rbxm

def FormatUnionParts(f):
    # Load the rbxm file
    file = rbxm.load(f)
    #Sort through the objects in the file.
    for object in file.objects:
        if isinstance(object, rbxm.UnionOperation):
            parts = object.Parts
        ##endif
    ##end
##end
