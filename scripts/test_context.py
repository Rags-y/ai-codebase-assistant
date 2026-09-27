from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.context import ContextBuilder


pipeline = RetrievalPipeline()
builder = ContextBuilder()


query = "How are tasks created and what validates the input?"


results = pipeline.retrieve(
    query,
    semantic_top_k=3,
    graph_hops=1,
)


context = builder.build(results)


print()
print("=" * 80)
print("RETRIEVED CONTEXT")
print("=" * 80)
print()

print(context)