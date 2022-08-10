import numpy as np
# import mosek
from NPAsolver3 import NpaHierarchy

b=NpaHierarchy(2,level=2)

# CHSH Inequality
b.addObjective("4pab(00|00)+4pab(00|01)+4pab(00|10)-4pab(00|11)-4pa(0|0)-4pb(0|0)")
print(f"CHSH Inequality with matrix dim. {len(b.row)} answer is:",2+b.solve())

#CH Inequality
b.addObjective("pab(00|00)+pab(00|01)+pab(00|10)-pab(00|11)-pa(0|0)-pb(0|0)")
print("CH Inequality: ",b.solve())

# Dimension Witness
b=NpaHierarchy(oprArray=[[2,3],[2,2,2]])
b.addObjective("pa(0|0)-pab(00|00)-pab(00|01)-pab(00|02)+pab(00|10)+pab(10|11)+pb(0|2)-pab(00|12)-pab(10|12)")
print(f"Dim. witness: using I_1+AB matrix size {len(b.row)} answer is",b.solve()-1)

b=NpaHierarchy(2,inputs=3,outputs=2,level=3)
b.addObjective("pab(00|00)+pab(00|01)-pa(0|1)-pb(0|0)-2pb(0|1)+pab(00|10)+pab(00|11)-pab(00|02)+pab(00|12)-pab(00|20)+pab(00|21)")
print(f"I3322: using NPA3  and matrix dim. {len(b.row)}  answer is",b.solve())

b=NpaHierarchy(3,level=4)
b.addObjective("pabc(000|000)")
for i in np.linspace(0,0.3,10):
    b.addConstraints([f"pbc(00|10)<={i}",f"pab(00|10)<={i}",f"pac(00|01)<={i}",f"pab(00|11)+pbc(00|11)+pac(00|11)-pa(0|1)-pb(0|1)-pc(0|1)-pabc(000|111)<={i-1}"])
    print(i,b.solve())
