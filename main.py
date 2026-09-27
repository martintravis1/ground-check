import json
import hashlib
from difflib import SequenceMatcher

def load_corpus(path='corpus.json'):
    with open(path) as f:
        return json.load(f)

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]

def fetch_facts(corpus, query):
    # Deterministic tool: return relevant entries from corpus (simulated retrieval)
    # In real use, replace with DB/API. Here we simply return all facts containing query keywords.
    tokens = query.lower().split()
    return [entry for entry in corpus if any(t in entry['text'].lower() for t in tokens)][:3]

def llm_propose(query, facts):
    # Simulate a hallucination-prone LLM: it may fabricate facts not in corpus.
    # For demo, we hardcode a response that mixes correct and wrong info.
    if 'population' in query.lower():
        return "Paris has a population of 2.1 million."  # wrong, actual ~2.16M but not exact
    else:
        return f"Based on sources: {', '.join(fact['text'] for fact in facts)}"

def verify_claim(claim, facts):
    evidence = []
    for fact in facts:
        # Simple similarity check: if claim is near any fact text, consider grounded.
        ratio = SequenceMatcher(None, claim.lower(), fact['text'].lower()).ratio()
        if ratio > 0.6:
            evidence.append({'fact': fact['text'], 'similarity': round(ratio, 2), 'source': fact['source']})
    return evidence

def main():
    corpus = [
        {'text': 'Paris is the capital of France.', 'source': 'wiki'},
        {'text': 'France has an estimated population of 67 million.', 'source': 'worldbank'},
        {'text': 'The Eiffel Tower is located in Paris.', 'source': 'travel-guide'},
    ]
    query = "What is the population of Paris?"
    facts = fetch_facts(corpus, query)
    claim = llm_propose(query, facts)
    evidence = verify_claim(claim, facts)
    if evidence:
        print(json.dumps({'claim': claim, 'grounded': True, 'evidence': evidence}, indent=2))
    else:
        print(json.dumps({'claim': claim, 'grounded': False, 'evidence': [], 'note': 'LLM hallucination - no source supports this exact claim.'}, indent=2))

if __name__ == '__main__':
    main()