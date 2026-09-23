import c4d
import random

def create_random_color() -> c4d.Vector:
    """Generates a random color."""
    return c4d.Vector(random.random(), random.random(), random.random())

def main() -> None:
    """Called by Cinema 4D when the script is being executed."""
    doc = c4d.documents.GetActiveDocument()
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    
    if not selected_objects:
        c4d.gui.MessageDialog("No objects selected.")
        return
    
    for obj in selected_objects:
        # Check if the object already has a standard material
        texture_tag = obj.GetTag(c4d.Ttexture)
        if texture_tag:
            mat = texture_tag.GetMaterial()
            if mat and mat.GetType() == c4d.Mmaterial:
                # Change the color of the existing material
                mat[c4d.MATERIAL_COLOR_COLOR] = create_random_color()
            else:
                # Create a new material if the existing one is not a standard material
                mat = c4d.BaseMaterial(c4d.Mmaterial)
                mat.SetName(obj.GetName())
                mat[c4d.MATERIAL_COLOR_COLOR] = create_random_color()
                doc.InsertMaterial(mat)
                texture_tag.SetMaterial(mat)
        else:
            # Create a new material if no material is assigned
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            mat.SetName(obj.GetName())
            mat[c4d.MATERIAL_COLOR_COLOR] = create_random_color()
            doc.InsertMaterial(mat)
            
            # Create a texture tag and assign the material to the object
            texture_tag = c4d.TextureTag()
            texture_tag.SetMaterial(mat)
            obj.InsertTag(texture_tag)
    
    c4d.EventAdd()

if __name__ == '__main__':
    main()