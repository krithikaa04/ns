import csv
import math
import os

# Load documents from CSV
def load_documents(folder_path):
    docs = {}
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            docs[file] = f.read().lower().split()
    return docs

def load_documents_from_csv(file_path):
    docs = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            doc_id, text = row
            docs[doc_id] = text.lower().split()
    return docs

# Compute RSV for BIM
def compute_rsv(docs, query, relevant_docs):
    N = len(docs)
    query_terms = query.lower().split()
    R = len(relevant_docs)
    # Document frequency
    df = {t: sum(1 for words in docs.values() if t in words) for t in query_terms}
    # Relevant frequency
    r_count = {t: sum(1 for d in relevant_docs if t in docs[d]) for t in query_terms}
    scores = {}
    for doc_id, words in docs.items():
        score = 0
        for t in query_terms:
            if t in words:
                r = r_count[t]
                n = df[t]
                # Compute p and u
                p = (r + 0.5) / (R + 1)
                u = (n - r + 0.5) / (N - R + 1)
                score += math.log((p * (1 - u)) / (u * (1 - p)), 10)
        scores[doc_id] = score
    return scores

# Main
if __name__ == "__main__":
    docs = load_documents_from_csv("ca1\docs\docs.csv")
    query = input("Enter query: ")
    relevant_docs = input("Enter relevant doc IDs (comma separated): ").split(",")
    scores = compute_rsv(docs, query, relevant_docs)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nDocument Rankings:")
    for d, s in ranked:
        print(f"{d}: {round(s, 4)}")
