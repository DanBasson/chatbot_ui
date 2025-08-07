import asyncio
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


# Use the MockStreamingLLM from the first example
# (Copy the MockStreamingLLM class here or import it)

def demo_streaming_chain():
    """Demonstrate streaming with Langchain chains."""

    # Initialize mock LLM
    mock_llm = MockStreamingLLM(
        words_per_chunk=3,
        delay_between_chunks=0.2,
        total_chunks=10
    )

    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Please explain {topic} in simple terms:"
    )

    # Create a chain
    chain = prompt | mock_llm | StrOutputParser()

    print("=== Streaming with Chain ===")
    for chunk in chain.stream({"topic": "machine learning"}):
        print(chunk, end="", flush=True)
    print("\n")


def demo_conversation_chain():
    """Demonstrate a more complex conversation chain."""

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain

    # Initialize components
    mock_llm = MockStreamingLLM(
        words_per_chunk=2,
        delay_between_chunks=0.1,
        total_chunks=15
    )

    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=mock_llm,
        memory=memory,
        verbose=True
    )

    print("=== Conversation Chain Streaming ===")

    # Stream the conversation
    for chunk in conversation.stream("Hello, how are you?"):
        print(chunk, end="", flush=True)
    print("\n")


async def demo_async_streaming():
    """Demonstrate async streaming."""

    mock_llm = MockStreamingLLM(
        words_per_chunk=4,
        delay_between_chunks=0.15,
        total_chunks=12
    )

    prompt = PromptTemplate(
        input_variables=["question"],
        template="Answer this question: {question}"
    )

    chain = prompt | mock_llm

    print("=== Async Streaming ===")
    async for chunk in chain.astream({"question": "What is the meaning of life?"}):
        print(chunk.text if hasattr(chunk, 'text') else chunk, end="", flush=True)
    print("\n")


def demo_with_callbacks():
    """Demonstrate streaming with custom callbacks."""

    from langchain.callbacks.base import BaseCallbackHandler

    class StreamingCallback(BaseCallbackHandler):
        def on_llm_new_token(self, token: str, **kwargs) -> None:
            print(f"[TOKEN] {token}", end="", flush=True)

        def on_llm_start(self, *args, **kwargs) -> None:
            print("[STARTING LLM]")

        def on_llm_end(self, *args, **kwargs) -> None:
            print("\n[LLM FINISHED]")

    mock_llm = MockStreamingLLM(
        words_per_chunk=2,
        delay_between_chunks=0.2,
        total_chunks=8
    )

    callback = StreamingCallback()

    print("=== Streaming with Callbacks ===")
    for chunk in mock_llm.stream("Tell me a story", callbacks=[callback]):
        pass  # The callback handles the output
    print()


if __name__ == "__main__":
    # Run all demos
    demo_streaming_chain()
    print("\n" + "=" * 50 + "\n")

    demo_conversation_chain()
    print("\n" + "=" * 50 + "\n")

    asyncio.run(demo_async_streaming())
    print("\n" + "=" * 50 + "\n")

    demo_with_callbacks()