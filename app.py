from jina import Document, DocumentArray, Flow
from jina.types.document.generators import from_csv

with open("medium_data.csv") as file:
    docs = DocumentArray(from_csv(file, field_resolver={"title": "text"}))

# step 1 done 
print("created doc array")

flow = (
    Flow()
    .add(
        uses="jinahub://SpacyTextEncoder",
        uses_with={"model_name": "en_core_web_md"},
        name="encoder",
        install_requirements=True
    )
    .add(
        uses="jinahub://SimpleIndexer",
        uses_metas={"workspace": "workspace"},
        volumes="./workspace:/workspace/workspace",
        name="indexer",
        install_requirements=True
    )
)

with flow:
    flow.index(inputs=docs)
    query = Document(text=input("Please enter your search term: "))
    response = flow.search(inputs=query, return_results=True)

matches = response[0].data.docs[0].matches
print("\nYour search results")
print("-------------------\n")

for match in matches:
    print(f"- {match.text}")
