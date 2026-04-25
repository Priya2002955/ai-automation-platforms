from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def load_policy_text():
    file_path = "docs/inventory_policy.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    if not text.strip():
        raise ValueError("inventory_policy.txt is empty. Please add policy text.")

    return text


def build_vector_store():
    text = load_policy_text()

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=20
    )

    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("No chunks created. Check your policy file content.")

    print(f"Number of chunks created: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_texts(chunks, embeddings)

    return vector_store


def ask_question(question):
    vector_store = build_vector_store()

    results = vector_store.similarity_search(question, k=4)

    print("\nQuestion:")
    print(question)

    print("\nRelevant Policy Context:")
    for i, doc in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(doc.page_content)


if __name__ == "__main__":
    ask_question("What should happen when there is stockout risk?")