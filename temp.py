import torch



a = torch.rand(4)

b = torch.clone(a)

a[1] = 4

print(b, a)