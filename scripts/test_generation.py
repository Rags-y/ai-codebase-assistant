from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.context import ContextBuilder
from src.generation.generator import AnswerGenerator


query = "How are tasks created and what validates the input?"


pipeline = RetrievalPipeline()

results = pipeline.retrieve(
    query,
    semantic_top_k=3,
    graph_hops=1,
)


builder = ContextBuilder()

context = builder.build(results)


generator = AnswerGenerator()

answer = generator.generate(
    query,
    context,
)


print()
print("=" * 80)
print("GROUNDED ANSWER")
print("=" * 80)
print()

print(answer)