import c4d

def main():
    doc: c4d.documents.BaseDocument = c4d.documents.GetActiveDocument()  # The currently active document.
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)  # Get selected objects in selection order

    if len(selection) >= 2:
        op1 = selection[-2]  # The second last selected object
        op2 = selection[-1]  # The last selected object

        # Start recording undo
        doc.StartUndo()

        # Add undo for the second object
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, op2)

        # Get the world matrix of the first object
        world_matrix = op1.GetMg()
        
        # Set the world matrix of the second object
        op2.SetMg(world_matrix)
        
        # Update the document to reflect the changes
        c4d.EventAdd()

        # End recording undo
        doc.EndUndo()
        
        print(f"Copied world position from {op1.GetName()} to {op2.GetName()}")
    else:
        print("Please select at least two objects.")

if __name__ == "__main__":
    main()