import os

# ===== Step 1: Build Inverted Index =====
def build_inverted_index(folder_path):
    inverted_index = {}
    documents = os.listdir(folder_path)

    for doc in documents:
        with open(os.path.join(folder_path, doc), 'r', encoding='utf-8') as f:
            words = f.read().lower().split()
            for word in words:
                if word not in inverted_index:
                    inverted_index[word] = set()
                inverted_index[word].add(doc)
    return inverted_index, documents


# ===== Step 2: Process Boolean Query =====
def process_query(query, inverted_index, all_docs):
    query = query.upper().split()
    result = set(all_docs)  # start with all docs for AND logic
    operator = None

    i = 0
    while i < len(query):
        token = query[i]

        if token in ["AND", "OR", "NOT"]:
            operator = token
        else:
            word = token.lower()
            docs_with_word = inverted_index.get(word, set())

            if operator is None:  # first term
                result = docs_with_word
            elif operator == "AND":
                result = result & docs_with_word
            elif operator == "OR":
                result = result | docs_with_word
            elif operator == "NOT":
                result = result - docs_with_word

        i += 1

    return result


# ===== Step 3: Main Program =====
if __name__ == "__main__":
    folder_path = "ca1\docs"  # folder containing text files
    inverted_index, all_docs = build_inverted_index(folder_path)

    print("Inverted Index:", inverted_index)
    query = input("Enter Boolean Query (e.g., apple AND NOT mango): ")
    result_docs = process_query(query, inverted_index, all_docs)

    print("\nRelevant Documents:")
    if result_docs:
        for doc in result_docs:
            print(doc)
    else:
        print("No documents match the query.")
