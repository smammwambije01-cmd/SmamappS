import math
def duara(pos,dim,axis='y', microbox=0.1):
    bx,by,bz=pos
    up,ur,un=dim
    step=microbox
    micro_dim=(step,step,step)

    vibox=[]
    if axis.upper()=='Y':
        center_x=bx + (up/2)
        center_z=bz + (un/2)
        radius=min(up,ur)/2

        x_steps=int(up/step)
        z_steps=int(un/step)
        y_steps=max(1,int(ur/step))

        for xi in range(x_steps):
            x_pos= bx + (xi * step) + (step /2)
            for zi in range(z_steps):
                z_pos= bz + (zi * step) + (step /2)
                if ((x_pos - center_x) ** 2 + (z_pos - center_z) ** 2)<= (radius ** 2):
                    for yi in range(y_steps):
                        y_pos = by + (yi * step)
                        pos_xyz=(X_pos - step/2,y_pos,z_pos - step/2)
                        vibox.append(micro_dim,pos_xyz)
    return vibox
