import abc
from typing import *

import torch
from torch import nn
from transformers import AutoModel, DistilBertConfig, DistilBertModel

from .context import ContextHead, ContextTransformerAndWide
from .moe import MOELayer, Top2Gate, ExpertLayer, MoEFFLayer
from .transformer import (ParallelTransformerAEP, TransformerAEP,
                          TransformerHistory)
from .utils import MeanMaxPooling, LayerNorm

    
class PaRS(nn.Module):
    def __init__(self, deep_dims, page_dim, seq_dim, page_embed_dim, item_embed_dim, seq_embed_dim, deep_embed_dims, wad_embed_dim, nlp_embed_dim, seq_hidden_size, nlp_encoder_path, task_type_dim, task_type_embed_dim,
                 num_wide=0, num_shared=0, nlp_dim=0, item_freeze=None, nlp_freeze=None, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 page_embedding_weight=None, item_embedding_weight=None, shared_embeddings_weight=None, moe_kwargs=None):
        super().__init__()
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        
        if page_embedding_weight is None:
            print("not use pretrained embedding")
            self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        else:
            print("use pretrained item embedding")
            self.page_embedding = nn.Embedding.from_pretrained(page_embedding_weight, freeze=False)
        if item_embedding_weight is None:
            print("not use pretrained embedding")
            self.item_embedding = nn.Embedding(seq_dim, item_embed_dim)
        else:
            print("use pretrained item embedding")
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=False)
            
        if item_freeze:
            self.item_embedding.weight.requires_grad = False
            
        if nlp_freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
         
        self.combined_dim = nlp_embed_dim + wad_embed_dim + seq_embed_dim
        self.task_embedding = nn.Embedding(task_type_dim, self.combined_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            shared_embeddings_weight=shared_embeddings_weight,
            wad_embed_dim=wad_embed_dim,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = ParallelTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            dim=item_embed_dim,
            dim_head=item_embed_dim,
            heads=sequence_transformer_kwargs.get("seq_num_heads"),
            num_layers=sequence_transformer_kwargs.get("seq_num_layers"),
            moe_kwargs=moe_kwargs
        )
        self.seq_dense = torch.nn.Linear(
            in_features=item_embed_dim,
            out_features=seq_embed_dim
        )
        self.nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=nlp_embed_dim
        ) 
        self.moe = MoEFFLayer(dim=self.combined_dim, num_experts=moe_kwargs.get("num_experts"), expert_capacity=moe_kwargs.get("expert_capacity"), hidden_size=self.combined_dim, expert_class=ExpertLayer)
        
        
#         self.dense1 = torch.nn.Linear(
#             in_features=self.combined_dim,
#             out_features=self.combined_dim, bias=False)
#         self.gate = Top2Gate(nlp_embed_dim + wad_embed_dim + seq_embed_dim, moe_kwargs.get("num_experts"))
#         self.moe = MOELayer(self.gate, self.dense1, nlp_embed_dim + wad_embed_dim + seq_embed_dim)
#         self.norm = LayerNorm(nlp_embed_dim + wad_embed_dim + seq_embed_dim)
        self.tasks_dense1 = nn.ModuleDict()
        self.tasks_dense2 = nn.ModuleDict()
        self.tasks_dense3 = nn.ModuleDict()
        self.tasks_act1 = self.tasks_act2 = nn.ModuleDict()
        for i in range(task_type_dim):
            self.tasks_dense1[f"task{i}_dense1"] = nn.Linear(
                self.combined_dim, 
                self.combined_dim // 2
            )
            self.tasks_dense2[f"task{i}_dense2"] = nn.Linear(
                self.combined_dim // 2, 
                seq_dim
            )
            self.tasks_act1[f"task{i}_act1"] = self.tasks_act2[f"task{i}_act2"] = nn.LeakyReLU(0.2)
        self.seq_dim = seq_dim
        self.task_type_dim = task_type_dim

    def split_task(self, task_type_dim, task_in, combined_out):
        task_indices = []
        task_outs = []
        task_user_outs = []
        for i in range(task_type_dim):
            task_indice = task_in == i
            task_indice = torch.nonzero(task_indice).flatten()
            task_indices.append(task_indice)
            task_input = combined_out[task_indice]
            task_out = self.tasks_dense1[f"task{i}_dense1"](task_input)
            task_user_out = self.tasks_act1[f"task{i}_act1"](task_out)
            task_out = self.tasks_dense2[f"task{i}_dense2"](task_user_out)
            task_user_outs.append(task_user_out)
            task_outs.append(task_out)
        return task_indices, task_outs, task_user_outs
        
    def forward(self, deep_in, page_in, item_in, vl_in, task_in, wide_in=None, input_ids=None, attention_mask=None, shared_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_out = self.nlp_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:,0,:].to(dtype=torch.float32)
        search_out = self.nlp_dense(search_out)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        seq_out = self.seq_dense(seq_out)
        task_out = self.task_embedding(task_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = torch.mul(outs, task_out)
        outs = outs[:, None, :]
        outs, aux_loss = self.moe(outs)
        outs = outs.reshape(-1, self.combined_dim)
#         outs = self.norm(outs)
#         aux_loss = 0
#         outs = self.dense1(outs)

        task_indices, task_outs, task_user_outs = self.split_task(self.task_type_dim, task_in, outs)
        device = vl_in.device
        out = torch.zeros(outs.shape[0], self.seq_dim).to(device)
        for i in range(self.task_type_dim):
            out[task_indices[i]] = task_outs[i]
        return (out, task_user_outs, task_indices, aux_loss)