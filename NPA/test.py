import numpy as np
import matplotlib.pyplot as plt
import mosek
from NPAsolver import NpaHierarchy
x=np.linspace(2,2*np.sqrt(2),100)
y=[]
b=NpaHierarchy(2)
b.addObjective("pab(00|00)")
for i in x:
    b.addConstraints([f"pab(00|00)-pab(01|00)-pab(10|00)+pab(11|00)+pab(00|01)-pab(01|01)-0.99pab(10|01)+pab(11|01)+pab(00|10)-pab(01|10)-pab(10|10)+pab(11|10)-pab(00|11)+pab(01|11)+pab(10|11)-pab(11|11)={i}"])
    ans=b.solve()
    print(ans)
    y.append(ans)
plt.plot(x,-np.log2(y))
plt.xlabel("CHSH Inequality")
plt.ylabel("min-entropy")
plt.legend(["2nd-hierarchy"])
plt.show()
