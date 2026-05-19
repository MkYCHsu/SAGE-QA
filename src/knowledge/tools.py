from __future__ import annotations

from typing import List, Union
from termcolor import colored

from core import collect_entities, shared_context, debug
from prompts import SYSTEM_PROMPT_GRAPHMAKER


def formulate(query: str = "") -> str:
    """Ingest text into Thought-KG (MindMap). Notebook-faithful behavior."""
    if debug:
        print("FORMULATE")
    if not shared_context.mind:
        return "Context not initialized."
    shared_context.mind.intake(query, system_prompt=SYSTEM_PROMPT_GRAPHMAKER)
    return ""


def graph_source_rag(query: str = "", similarity_threshold: Union[float, str] = 0.95) -> str:
    """Notebook-faithful Graph Source RAG tool."""
    if not shared_context.knowledgebase:
        return "Context not initialized."
    if debug:
        print("GRAPH_SOURCE_RAG")

    max_n = 1
    sim_thr = float(similarity_threshold)

    subgraph = shared_context.knowledgebase.extract_keywords_to_subgraph(query, max_n, sim_thr)
    paths_list = collect_entities(subgraph)
    paths = "\n".join(paths_list)

    if not paths_list:
        return "No relations found. Abort."

    chunks: List[str] = []
    for _, _, data in subgraph.out_edges(data=True):
        cid = data.get("chunk_id")
        if cid:
            docs = shared_context.knowledgebase.chroma.get_docs_by_ids(cid)
            if docs:
                doc = docs[0]
                chunks.append(
                    f'Source chunk: {doc.get("content", doc.get("document"))} | title (DOI): {data.get("DOI", "")} | chunk_id: {cid}'
                )

    chunks_text = "\n".join(chunks)

    formulate(
        f"A group of specialized agents are working on this query: {query}\n\n. "
        f"Here is the information we found and need you to reorganize:\n"
        f"Retrived PATH:\n {paths}\n\nRetrieved Source Text:\n{chunks_text}"
    )

    print(colored(
        f"Aftering formulating, mind graph grows to {len(shared_context.mind.G.nodes)} nodes and "
        f"{len(shared_context.mind.G.edges)} edges {shared_context.mind.G if debug else ''}",
        "green",
    ))

    if debug:
        from datetime import datetime
        import networkx as nx
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        nx.write_graphml(shared_context.mind.G, f"mind_graph_{ts}.graphml")

    return "\n".join(collect_entities(shared_context.mind.G))
