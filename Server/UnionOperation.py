import rbxm

# Load the rbxm file
file = rbxm.load('model.rbxm')

# Iterate over the objects in the file
for object in file.objects:
    #Check if the object is a UnionOperation
    if isinstance(object, rbxm.UnionOperation):
        #Print the current name of the UnionOperation
        print(object.Name)
        #Change the name of the UnionOperation
        object.Name = 'NewUnion'
        #Print the new name of the UnionOperation
        print(object.Name)
    ##endif
##end

rbxm.save(file, 'model.rbxm')
