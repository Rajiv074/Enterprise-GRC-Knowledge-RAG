
# from MatrixStreamDocRAGApllication.Retriever.Retriever import (
#     retrieve_documents,
# )


# def main():
#     query = "How AI Improves Third-Party Risk Management ?"

#     documents = retrieve_documents(query)

#     print(f"\nFinal reranked documents: {len(documents)}")

#     for rank, doc in enumerate(documents, start=1):
#         print(f"\n--- Result {rank} ---")
#         print(
#             "Pinecone similarity:",
#             doc.metadata.get("pinecone_similarity_score"),
#         )
#         print("Source:", doc.metadata.get("source"))
#         print("Section:", doc.metadata.get("section"))
#         print("Content:", doc.page_content[:500])


# if __name__ == "__main__":
#     main()



from MatrixStreamDocRAGApllication.Workflow.workflow import stream_ask


def test_agentic_rag_workflow():

    question = "How Organizations Encumbered by Complexity?"

    for state in stream_ask(question):

        print("\nCurrent Query:")
        print(state.get("current_query"))

        print("\nEvidence Grade:")
        print(state.get("kb_grade"))

        print("\nRetry Count:")
        print(state.get("retry_count"))

        if state.get("answer"):
            print("\nAnswer:")
            print(state["answer"])

            print("\nCitations:")
            for citation in state.get("citations", []):
                print(citation)


if __name__ == "__main__":
    test_agentic_rag_workflow()

