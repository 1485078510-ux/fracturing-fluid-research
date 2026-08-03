# Semantic Scholar API Complete Reference

## Base URLs
- Academic Graph: `https://api.semanticscholar.org/graph/v1`
- Recommendations: `https://api.semanticscholar.org/recommendations/v1`
- Datasets: `https://api.semanticscholar.org/datasets/v1`

## Authentication
- Header: `x-api-key: YOUR_KEY`
- Register: https://www.semanticscholar.org/product/api#api-key
- Free tier: 1 req/sec with key, 100 req/5min without

## Paper Search

### GET /paper/search
```
GET /graph/v1/paper/search?query={query}&fields={fields}&limit={n}&offset={offset}&year={range}&minCitationCount={n}&venue={venues}&sort={field:order}&openAccessPdf&publicationTypes={types}
```

**Query syntax:**
- `+` or space — AND (default)
- `|` — OR
- `-` — negation
- `"exact phrase"` — phrase match
- `prefix*` — prefix match
- `word~N` — fuzzy match (N edit distance)
- `"word1 word2"~N` — proximity match

**Fields:** `paperId,externalIds,title,abstract,venue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,authors,tldr,embedding,citationStyles`

**Sort options:** `paperId:asc`, `paperId:desc`, `publicationDate:asc`, `publicationDate:desc`, `citationCount:asc`, `citationCount:desc`

### GET /paper/search/bulk
Bulk retrieval up to 10M results, paginated at 1000.
```
GET /graph/v1/paper/search/bulk?query={query}&sort={field:order}&year={range}&...
```
Response includes `token` for next page.

## Paper Details

### GET /paper/{paper_id}
```
GET /graph/v1/paper/{paper_id}?fields={fields}
```

**Supported IDs:**
- S2 Paper ID (40-char hex)
- `CorpusId:NNNN`
- `DOI:10.xxxx/yyyy`
- `ARXIV:NNNN.NNNNN`
- `PMID:NNNNNNNN`
- `PMCID:PMCNNNNNNN`
- `ACL:XXXX`
- `MAG:NNNNNNNNN`
- `URL:https://...`

### POST /paper/batch
Retrieve up to 500 papers:
```
POST /graph/v1/paper/batch?fields={fields}
Body: {"ids": ["DOI:...", "ARXIV:..."]}
```

## Citations & References

### GET /paper/{id}/citations
```
GET /graph/v1/paper/{id}/citations?fields={fields}&limit={n}&offset={n}&publicationDateOrYear={range}
```
Returns papers citing this paper.

### GET /paper/{id}/references
```
GET /graph/v1/paper/{id}/references?fields={fields}&limit={n}&offset={n}
```
Returns papers cited by this paper. Fields include `contexts`, `intents`, `isInfluential`.

## Recommendations

### GET /papers/forpaper/{id}
Single seed paper:
```
GET /recommendations/v1/papers/forpaper/{paper_id}?limit={n}&from={pool}&fields={fields}
```
Pool: `recent` (default) or `all-cs`

### POST /papers/
Multiple seed papers:
```
POST /recommendations/v1/papers/
Body: {
  "positivePaperIds": ["id1", "id2"],
  "negativePaperIds": ["id3"],
  "limit": 100
}
```

## Author Endpoints

### GET /author/search
```
GET /graph/v1/author/search?query={name}&limit={n}
```

### GET /author/{id}
```
GET /graph/v1/author/{id}?fields=name,affiliations,paperCount,citationCount,hIndex
```

### GET /author/{id}/papers
```
GET /graph/v1/author/{id}/papers?fields={fields}&limit={n}&sort={field:order}
```

## TLDR Field
The `tldr` field returns an AI-generated summary:
```json
{
  "tldr": {
    "model": "tldr@v2.0.0",
    "text": "This paper proposes a novel method for..."
  }
}
```

## Error Responses
- `400` — Bad parameters
- `404` — Resource not found
- `429` — Rate limited
- `500` — Server error

## Rate Limits
| Tier | Rate | Cost |
|------|------|------|
| No key | 100/5min | Free |
| With key | 1/sec | Free |
| Tier 1 | 10/sec | Contact S2 |
| Tier 2 | 100/sec | Contact S2 |
