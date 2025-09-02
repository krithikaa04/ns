import os
import math
import csv


# ===== Step 1: Read documents =====
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


# ===== Step 2: Build Vocabulary =====
def build_vocabulary(docs):
    vocab = set()
    for words in docs.values():
        vocab.update(words)
    return list(vocab)


# ===== Step 3: Compute Term Frequencies =====
def compute_tf(docs, vocab):
    tf = {}
    for doc, words in docs.items():
        tf[doc] = {}
        for term in vocab:
            tf[doc][term] = words.count(term) / len(words)
    return tf


# ===== Step 4: Compute IDF =====
def compute_idf(docs, vocab):
    N = len(docs)
    idf = {}
    for term in vocab:
        count = sum(1 for words in docs.values() if term in words)
        idf[term] = math.log((N / (count + 1)), 10)  # add 1 to avoid division by zero
    return idf


# ===== Step 5: Compute TF-IDF for documents =====
def compute_tfidf(tf, idf):
    tfidf = {}
    for doc in tf:
        tfidf[doc] = {}
        for term in tf[doc]:
            tfidf[doc][term] = tf[doc][term] * idf[term]
    return tfidf


# ===== Step 6: Compute cosine similarity =====
def cosine_similarity(vec1, vec2):
    dot = sum(vec1[t] * vec2.get(t, 0) for t in vec1)
    mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
    return dot / (mag1 * mag2) if mag1 and mag2 else 0.0


# ===== Step 7: Process query and rank docs =====
def process_query(query, vocab, idf):
    words = query.lower().split()
    tf_query = {}
    for term in vocab:
        tf_query[term] = words.count(term) / len(words)
    tfidf_query = {term: tf_query[term] * idf[term] for term in vocab}
    return tfidf_query


# ===== Step 8: Main Program =====
if __name__ == "__main__":
    # folder_path = "ca1\docs"  # folder with text files
    # docs = load_documents(folder_path)
    file_path = "ca1\docs\docs.csv"  # CSV file path
    docs = load_documents_from_csv(file_path)
    vocab = build_vocabulary(docs)

    tf = compute_tf(docs, vocab)
    idf = compute_idf(docs, vocab)
    tfidf_docs = compute_tfidf(tf, idf)

    query = input("Enter your query: ")
    tfidf_query = process_query(query, vocab, idf)

    # Compute similarity
    scores = {}
    for doc in docs:
        scores[doc] = cosine_similarity(tfidf_docs[doc], tfidf_query)

    # Sort by score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("\nDocument Rankings:")
    for doc, score in ranked:
        print(f"{doc}: {score:.4f}")
