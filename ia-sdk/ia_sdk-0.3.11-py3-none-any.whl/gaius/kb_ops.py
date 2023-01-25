"""Provides utilities for higher level operations on KnowledgeBases"""
from ia.gaius.agent_client import AgentClient
import traceback
from collections import Counter

def list_models(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: model_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (list, optional): nodes to list models on

    Returns:
        dict: {node_name: model_list} for each node specified in nodes
        
    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import list_models
            
            agent = AgentClient(agent_info)
            
            #get list of models found on node P1
            models = list_models(agent, nodes=['P1'])
    
    """
    if not agent._connected:
        agent.connect()
    
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        models_dict = {k : list(v['models_kb'].keys()) for k,v in kb.items()}

    except Exception as e:
        print(f'Error in list_models: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return models_dict

def list_symbols(agent: AgentClient, nodes=None):
    """Return a dict of {node_name: symbol_list} found on specified nodes

    Args:
        agent (AgentClient): GAIuS Agent
        nodes (list, optional): nodes to list symbols on

    Returns:
        dict: {node_name: symbol_list} for each node specified in nodes
        
    Example:
        .. code-block:: python

            from ia.gaius.agent_client import AgentClient
            from ia.gaius.kb_ops import list_symbols
            
            agent = AgentClient(agent_info)
            
            #get list of symbols found on node P1
            symbols = list_symbols(agent, nodes=['P1'])
            
                
    """
    if not agent._connected:
        agent.connect()
    
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        symbols_dict = {k : list(v['symbols_kb'].keys()) for k,v in kb.items()}
    except Exception as e:
        print(f'Error in list_symbols: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return symbols_dict

def get_models_containing_symbol(agent: AgentClient, symbol_set:set, nodes=None):
    """Checks for presence of symbols from `symbol_set` in each model on `nodes`, adding to return dict if a symbol is found.
    
    Args:
        agent (AgentClient): GAIuS Agent
        symbol (str): the symbol to search for
        nodes (_type_, optional): nodes to search. Defaults to searching all nodes
    """

    if not agent._connected:
        agent.connect()
    
    sym_dict = {}
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        
        for node, node_kb in kb.items():
            sym_dict[node] = set()
            if 'models_kb' not in node_kb:
                continue
            for model_name, model in node_kb['models_kb'].items():
                for event in model['sequence']:
                    for sym in event:
                        if sym in symbol_set:
                            sym_dict[node].add(model_name)
            
    except Exception as e:
        print(f'Error in identify_models_with_symbol: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return sym_dict

def get_models_containing_symbol_strict(agent: AgentClient, symbol_set:set, nodes=None):
    """Checks for presence of symbols from `symbol_set` in each model on `nodes`. 
    Only adds model to return dict if all symbols in model are from symbol set
    Store as a dict of {node_name : list}
    
    Args:
        agent (AgentClient): GAIuS Agent
        symbol (str): the symbol to search for
        nodes (_type_, optional): nodes to search. Defaults to searching all nodes
    """

    if not agent._connected:
        agent.connect()
    
    sym_dict = {}
    prev_summarize_state = agent.summarize_for_single_node
    try:
        agent.set_summarize_for_single_node(False)
        kb = agent.get_kbs_as_json(nodes=nodes, ids=False, obj=True)
        
        for node, node_kb in kb.items():
            sym_dict[node] = set()
            if 'models_kb' not in node_kb:
                continue
            for model_name, model in node_kb['models_kb'].values():
                unique_symbols_in_model = set()
                for event in model['sequence']:
                    for sym in event:
                        unique_symbols_in_model.add(sym)
                        
                if all([sym in symbol_set for sym in unique_symbols_in_model]):
                    sym_dict[node].add(model_name)
            
    except Exception as e:
        print(f'Error in identify_models_with_symbol: {e}')
        raise e
    finally:    
        agent.set_summarize_for_single_node(prev_summarize_state)
    
    return sym_dict

def get_kb_subset(agent: AgentClient, model_dict: dict):
    """Retrieve a subset of a Knowledgebase based on the provided model_dict. 
    Will only provide used symbols and vectors, all others will be trimmed.

    Args:
        agent (AgentClient): GAIuS Agent
        model_dict (dict): {node_name: model_list}. Expected format is similar to that returned from :func:`list_models`

    Raises:
        e: Exception in subset iteration (e.g. model not found on node, get_kb failed, etc.)

    Returns:
        dict: Subset of Knowledgebases corresponding to provided model_dict
        
    Example:
        .. code-block:: python
            :force:

            from ia.gaius.kb_ops import get_kb_subset, list_models
            from ia.gaius.agent_client import AgentClient
            
            agent = AgentClient(agent_info)
            agent.connect()
            
            models = list_models(agent=agent, nodes=['P1'])
            
            # get a subset of available models
            models = {k: v[:20] for k,v in models.items()}
            
            # get a subset of the entire Knowledgebase
            kb_subset = get_kb_subset(agent=agent, model_dict=models)
            
    """
    
    try:
        reconstructed_kb = {}
        for node, models in model_dict.items():
            
            node_kb = agent.get_kbs_as_json(obj=True, nodes=[node], ids=False)
            node_kb = node_kb[node]
            
            if not all([model in node_kb["models_kb"] for model in models]):
                print(f'Not all models were found on node {node}')
                for model in models:
                    if model not in node_kb["models_kb"]:
                        print(f'model "{model}" not found')
                raise Exception(f'Not all models were found on node {node}')
            
            reconstructed_kb[node] = {'models_kb': {},
                                    'symbols_kb': {},
                                    'vectors_kb': {},
                                    'metadata': {}}
            print(f'original model count: {len(node_kb["models_kb"])}')
            print(f' reduced model count: {len(models)}')
            # will need to recompute symbol frequency and model member frequency counts
            symbol_freq_counter = Counter()
            symbol_model_member_freq_counter = Counter()
            
            # only keep symbols found in the specified models for the kb subset
            symbol_set = set()
            for model in models:
                unique_symbols_in_model = set()
                reconstructed_kb[node]["models_kb"][model] = node_kb["models_kb"][model]
                for event in reconstructed_kb[node]["models_kb"][model]['sequence']:
                    for sym in event:
                        symbol_set.add(sym)
                        unique_symbols_in_model.add(sym)
                    symbol_freq_counter.update(event)
                
                symbol_model_member_freq_counter.update(unique_symbols_in_model)
            
            for sym in symbol_set:
                reconstructed_kb[node]['symbols_kb'][sym] = node_kb['symbols_kb'][sym]
                
                # update frequency and model member frequency to new subset values
                reconstructed_kb[node]['symbols_kb'][sym]['features']['frequency'] = symbol_freq_counter[sym]
                reconstructed_kb[node]['symbols_kb'][sym]['features']['model_member_frequency'] = symbol_model_member_freq_counter[sym]
                
                # if the symbol is a vector, add it to the subset vectors_kb
                if 'VECTOR|' in sym:
                    vectHash = sym.split('|')[-1]
                    reconstructed_kb[node]['vectors_kb'][vectHash] = node_kb['vectors_kb'][vectHash]
                    
        return reconstructed_kb
    except Exception as e:
        print(f'failed to retrieve kb subset: {e}')
        raise e