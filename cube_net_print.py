def print_face(face):
    n = len(face)
    return [
        " ".join(str(int(face[i][j])) for j in range(n))
        for i in range(n)
    ]

def print_net(faces, step=None):
    n = len(faces[0])
    cell_width = 2 * n - 1  # ancho de una cara (dígitos + espacios)
    space = " " * (cell_width + 3)  # padding izquierdo para top/down/back
    
    f0 = print_face(faces[0])
    f1 = print_face(faces[1])
    f2 = print_face(faces[2])
    f3 = print_face(faces[3])
    f4 = print_face(faces[4])
    f5 = print_face(faces[5])
    
    if step is not None:
        print(f"Step {step}:")
    
    for row in f0:
        print(space + row)
        
    for i in range(n):
        print(f1[i] + "   " + f2[i] + "   " + f3[i])
        
    for row in f4:
        print(space + row)
        
    for row in f5:
        print(space + row)