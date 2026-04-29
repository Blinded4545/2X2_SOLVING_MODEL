def print_face(face):
    return [
        f"{face[0]} {face[1]}",
        f"{face[2]} {face[3]}"
    ]

def print_net(faces):
    f0 = print_face(faces[0])
    f1 = print_face(faces[1])
    f2 = print_face(faces[2])
    f3 = print_face(faces[3])
    f4 = print_face(faces[4])
    f5 = print_face(faces[5])
    
    space = " " * 6
    
    for row in f0:
        print(space + row)
       
    for i in range(2):
        print(f1[i]+"   "+f2[i]+"   "+f3[i])
        
    for row in f4:
        print(space+row)
        
    for row in f5:
        print(space+row)