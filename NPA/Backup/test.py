import numpy as np
# import mosek
from NPAsolver2 import NpaHierarchy

b=NpaHierarchy(2,level=2)

# CHSH Inequality
b.addObjective(
"pab(00|00)+pab(11|00)-pab(01|00)-pab(10|00)+pab(00|01)+pab(11|01)-pab(01|01)-pab(10|01)+pab(00|10)+pab(11|10)-pab(01|10)-pab(10|10)-pab(00|11)-pab(11|11)+pab(01|11)+pab(10|11)")
print(f"CHSH Inequality with matrix dim. {len(b.row)} answer is:",2+b.solve())


# Dimension Witness
b=NpaHierarchy(oprArray=[[2,3],[2,2,2]])
b.addObjective("pa(0|0)+pb(0|0)+pb(0|1)-pab(00|00)-pab(00|01)-pab(00|10)-pab(10|11)-pab(00|02)-pab(00|12)+pab(10|12)")
print(f"Dim. witness: using I_1+AB matrix size {len(b.row)} answer is",b.solve())

b=NpaHierarchy(2,inputs=3,outputs=2,level=3)
b.addObjective("pab(00|00)+pab(00|01)-pa(0|1)-pb(0|0)-2pb(0|1)+pab(00|10)+pab(00|11)-pab(00|02)+pab(00|12)-pab(00|20)+pab(00|21)")
print(f"I3322: using NPA3  and matrix dim. {len(b.row)}  answer is",b.solve())

b=NpaHierarchy(3,level=4)
b.addObjective("pabc(000|000)")
for i in np.linspace(0,0.3,10):
    b.addConstraints([f"pbc(00|10)<={i}",f"pab(00|10)<={i}",f"pac(00|01)<={i}",f"pabc(111|111)<={i}"])
    print(i,b.solve())
