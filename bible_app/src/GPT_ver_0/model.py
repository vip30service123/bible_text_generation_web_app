from typing import Dict, List, Optional


import torch
from torch import nn
import torch.nn.functional as F




class Head(nn.Module):
    def __init__(self, dim: int, head_dim: int, device: str) -> None:
        super().__init__()

        self.device = device

        self.query = nn.Linear(dim, head_dim)
        self.key = nn.Linear(dim, head_dim)
        self.value = nn.Linear(dim, head_dim)

    def forward(self, x) -> torch.Tensor:
        query = self.query(x)
        key = self.key(x)
        value = self.value(x)

        w = query @ key.transpose(-2, -1) # head_dim * head_dim
        w = torch.tril(w).to(self.device)
        w = F.softmax(w, dim=-1)
        out = w @ value
        return out


class MultiHead(nn.Module):
    def __init__(
            self, 
            dim: int, 
            head_dim: int, 
            n_heads: int, 
            dropout: float, 
            device: str): # head_dim % n_heads == 0
        
        super().__init__()

        self.multihead = nn.ModuleList(
            [Head(dim, head_dim//n_heads, device) for _ in range(n_heads)]
        )
        self.proj = nn.Linear(head_dim, dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x) -> torch.Tensor:
        a = [h(x) for h in self.multihead]
        return self.proj(torch.cat(a, dim=-1))


class FeedForward(nn.Module):
    def __init__(self, dim: int, dropout: float):
        super().__init__()

        self.ffw = nn.Sequential(
            nn.Linear(dim, 4 * dim),
            nn.ReLU(),
            nn.Linear(4 * dim, dim), # projection, dunno why
            nn.Dropout(dropout)
        )

    def forward(self, x) -> torch.Tensor:
        return self.ffw(x)


class GPTBlock(nn.Module):
    def __init__(self, dim: int, head_dim: int, n_heads: int, dropout: float, device: str):
        super().__init__()

        self.multihead = MultiHead(dim, head_dim, n_heads, dropout, device)
        self.ffw = FeedForward(dim, dropout)
        self.n1 = nn.LayerNorm(dim)
        self.n2 = nn.LayerNorm(dim)

    def forward(self, x) -> torch.Tensor:
        x = x + self.multihead(self.n1(x))
        x = x + self.ffw(self.n2(x))
        return x


class GPT(nn.Module):
    def __init__(self):
        super().__init__()

        self.device = 'cpu'
        self.vocab_sz = 31405


        self.word_embedding = nn.Embedding(31405, 256)
        self.position = nn.Embedding(128, 256)
        self.blocks = nn.Sequential(
            *[GPTBlock(256, 128, 32, 0.2, 'cpu') for _ in range(6)]
        )
        self.n = nn.LayerNorm(256)
        self.lout = nn.Linear(256, 31405)


    def forward(
        self,
        input, # B, T
        target=None # B, T
        ) -> Dict[str, torch.Tensor]:
        B, T = input.shape

        x = self.word_embedding(input) 
        pos = self.position(torch.arange(T).type(torch.int64).to(self.device))   # B, T, dim
        x += pos
        x = self.blocks(x)
        x = self.n(x)
        logits = self.lout(x) # B, T, vocab_sz

        if target == None:
            return {
                'logits': logits,
                'last_hidden_layer': x,
            }


        loss = F.cross_entropy(logits.view(B*T, self.vocab_sz), target.view(-1))

        return {
            'logits': logits,
            'last_hidden_layer': x,
            'loss': loss
        }


    def generate(self, x, max_length: int = 50) -> str:
        input = torch.clone(x)

        for _ in range(max_length):
            logits = self(x)['logits'][:,-1,:]
            prob = F.softmax(logits, dim=-1)
            out = torch.multinomial(prob, 1)
            x = torch.cat((x, out), dim=-1)

        return {
            'input': input,
            'generate': x[:, input.shape[1]:],
            'full': x
        }
    