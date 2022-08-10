from NPAsolver2 import NpaHierarchy
b=NpaHierarchy(3,level=2)
b.addObjective("pabc(000|000)")
b.addConstraints(["pab(00|10)=0","pac(00|01)=0","pbc(00|10)=0","pab(00|11)+pbc(00|11)+pac(00|11)-pa(0|1)-pb(0|1)-pc(0|1)-pabc(000|111)=-1"])
print("Maximum CHSH Value is",b.solve())
