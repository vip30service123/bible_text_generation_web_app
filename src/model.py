import torch
from torch import nn
import torch.nn.functional as F


class Head(nn.Module):
    def __init__(self, dim, head_dim, device):
        super().__init__()

        self.device = device

        self.query = nn.Linear(dim, head_dim)
        self.key = nn.Linear(dim, head_dim)
        self.value = nn.Linear(dim, head_dim)

    def forward(self, x):
        query = self.query(x)
        key = self.key(x)
        value = self.value(x)

        w = query @ key.transpose(-2, -1) # head_dim * head_dim
        w = torch.tril(w).to(self.device)
        w = F.softmax(w, dim=-1)
        out = w @ value
        return out


class MultiHead(nn.Module):
    def __init__(self, dim, head_dim, n_heads, dropout, device): # head_dim % n_heads == 0
        super().__init__()

        self.multihead = nn.ModuleList(
            [Head(dim, head_dim//n_heads, device) for _ in range(n_heads)]
        )
        self.proj = nn.Linear(head_dim, dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        a = [h(x) for h in self.multihead]
        return self.proj(torch.cat(a, dim=-1))


class FeedForward(nn.Module):
    def __init__(self, dim, dropout):
        super().__init__()

        self.ffw = nn.Sequential(
            nn.Linear(dim, 4 * dim),
            nn.ReLU(),
            nn.Linear(4 * dim, dim), # projection, dunno why
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.ffw(x)


class GPTBlock(nn.Module):
    def __init__(self, dim, head_dim, n_heads, dropout, device):
        super().__init__()

        self.multihead = MultiHead(dim, head_dim, n_heads, dropout, device)
        self.ffw = FeedForward(dim, dropout)
        self.n1 = nn.LayerNorm(dim)
        self.n2 = nn.LayerNorm(dim)

    def forward(self, x):
        x = x + self.multihead(self.n1(x))
        x = x + self.ffw(self.n2(x))
        return x


class GPT(nn.Module):
    def __init__(self, vocab_sz, window_sz, dim, n_layers, device, head_dim, n_heads, dropout, **kwargs):
        super().__init__()

        self.device = device
        self.vocab_sz = vocab_sz


        self.word_embedding = nn.Embedding(vocab_sz, dim)
        self.position = nn.Embedding(window_sz, dim)
        self.blocks = nn.Sequential(*[GPTBlock(dim, head_dim, n_heads, dropout, device) for _ in range(n_layers)])
        self.n = nn.LayerNorm(dim)
        self.lout = nn.Linear(dim, vocab_sz)


    def forward(
        self,
        input, # B, T
        target=None # B, T
        ):
        B, T = input.shape

        x = self.word_embedding(input) + self.position(torch.arange(T).type(torch.int64).to(self.device))   # B, T, dim
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


    def generate(self, x, max_length=10):
        for _ in range(max_length):
            logits = self(x)['logits'][:,-1,:]
            prob = F.softmax(logits, dim=-1)
            out = torch.multinomial(prob, 1)
            x = torch.cat((x, out), dim=-1)

        return x