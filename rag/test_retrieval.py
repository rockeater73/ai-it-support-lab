from retriever import retrieve_relevant_sops


def main():
    query = (
        "GlobalProtect keeps saying authentication failed, "
        "but I can sign in to Microsoft 365."
    )

    results = retrieve_relevant_sops(query, top_k=3)

    print("QUERY")
    print("=" * 60)
    print(query)

    print("\nRETRIEVAL RESULTS")
    print("=" * 60)

    for number, result in enumerate(results, start=1):
        print(f"\nRESULT {number}")
        print(f"Source: {result['source']}")
        print(f"Similarity: {result['score']:.4f}")
        print("\nText:")
        print(result["text"])
        print("-" * 60)


if __name__ == "__main__":
    main()