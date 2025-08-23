from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever, SearchType
from langchain_community.vectorstores import FAISS
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List
from pydantic import BaseModel, Field

import streamlit as st
import os
import faiss
import pickle
import json
import uuid

from langchain_community.docstore.in_memory import InMemoryDocstore
from unstructured.partition.pdf import partition_pdf

# take environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# load the GROQ API Key and Hugging Face Token
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

groq_model_name = "llama3-70b-8192"
llm = ChatGroq(model=groq_model_name, groq_api_key=groq_api_key)

def run():

    # --- RETRIEVAL STAGE ---

    st.markdown(""" 
    <div style='border: 1px solid #ccc; border-radius: 10px; padding: 20px; background-color: #f9f9f9;'>

    <h4>JEE Docs Chat</h4>

    <p style="font-size:18px; margin-bottom: 10px;">
    This chatbot helps you quickly find answers from the official <strong>JEE Mains</strong> and <strong>JEE Advanced</strong> information bulletins – no more digging through long PDFs!
    </p>

    <p style="font-size:16px;"><strong>What are JEE Mains & Advanced?</strong></p>
    <ul style="font-size:16px; padding-left: 20px; line-height: 1.6;">
    <li><strong>JEE Mains</strong> is the first stage of the Joint Entrance Examination conducted by NTA. It is a gateway for admission into NITs, IIITs, and other centrally funded technical institutions.</li>
    <li><strong>JEE Advanced</strong> is the second stage, conducted by the IITs for admission into the prestigious Indian Institutes of Technology (IITs).</li>
    <li>Admissions are done through the centralized <strong>JoSAA</strong> counselling process: <a href="https://josaa.nic.in/" target="_blank">https://josaa.nic.in/</a></li>
    </ul>

    <p style="font-size:16px; margin-bottom: 6px;"><strong>Data Sources Used:</strong></p>
    <ul style="font-size:16px; padding-left: 20px; line-height: 1.6;">
    <li><a href="https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2024/10/2024102824.pdf" target="_blank">JEE Mains Information Bulletin 2025</a></li>
    <li><a href="https://jeeadv.ac.in/documents/IBEnglish_2025.pdf" target="_blank">JEE Advanced Information Bulletin 2025</a></li>
    </ul>

    <p style="font-size:16px; margin-bottom: 6px;"><strong>How to Use This Chatbot:</strong></p>
    <ul style="font-size:16px; padding-left: 20px; line-height: 1.6;">
    <li><strong>Ask a Question:</strong><br>
        Type any question related to eligibility, exam pattern, ranks, reservation, seat allocation, etc.<br>
        Example: <code>What is the eligibility for JEE Advanced?</code> or <code>When is the Online Registration for JEE Advanced 2025?</code>
    </li><br>
    <li><strong>Get Instant Answers:</strong><br>
        The bot retrieves the most relevant answer from the official brochures.
    </li>
    </ul>

    <p style="font-size:18px; margin-top: 12px;"><strong>Start asking your JEE-related questions now!</strong></p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown('\n')

    flag = True    # to check if pdf vectorization is completed

    # The storage layer for the parent documents
    store = InMemoryStore()
    id_key = "doc_id"

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # current directory
    TRUNK_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))      # Move up one level to reach the trunk
    VECTOR_DB = os.path.join(TRUNK_DIR, 'vector_db')

    # Load FAISS index
    index = faiss.read_index(f"{VECTOR_DB}/advanced_vectorstore.faiss")

    # Load vectorstore metadata
    with open(f"{VECTOR_DB}/advanced_vectorstore_metadata.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    # Assign FAISS index back to vectorstore
    vectorstore.index = index

    # Load stored documents (text & tables)
    with open(f"{VECTOR_DB}/advanced_docstore.json", "r") as f:
        doc_data = json.load(f)

    # Restore data into docstore
    store.mset(list(doc_data.items()))

    # The retriever
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key="doc_id"  # Ensure this matches how doc_ids were stored
    )

    # --- LANGGRAPH: DEFINING THE NODES ---

    class AgentState(TypedDict):
        messages: List[BaseMessage]
        documents: List[Document]
        # on_topic: str
        rephrased_question: str
        proceed_to_generate: bool
        rephrase_count: int
        question: HumanMessage

    class GradeQuestion(BaseModel):
        score: str = Field(
            description="Question is about the specified topics? If yes -> 'Yes' if not -> 'No'"
        )


    def question_rewriter(state: AgentState):
        print(f"Entering question_rewriter with following state: {state}")

        # Reset state variables except for 'question' and 'messages'
        state["documents"] = []
        state["on_topic"] = ""
        state["rephrased_question"] = ""
        state["proceed_to_generate"] = False
        state["rephrase_count"] = 0

        if "messages" not in state or state["messages"] is None:
            state["messages"] = []

        if state["question"] not in state["messages"]:
            state["messages"].append(state["question"])

        if len(state["messages"]) > 1:
            conversation = state["messages"][:-1]     # getting the conversations before the last message (question)
            current_question = state["question"].content
            messages = [
                SystemMessage(
                    content="""
                    You are a helpful assistant that rephrases the user's question to be a standalone question optimized for retrieval from the JEE Advanced Information.
                    """
                )
            ]
            messages.extend(conversation)             # adding the conversation history after the system messages, followed by the question
            messages.append(HumanMessage(content=current_question))
            rephrase_prompt = ChatPromptTemplate.from_messages(messages)
            prompt = rephrase_prompt.format()         # instead of above lines, can replace with single prompt with placeholders for question and chat history
            response = llm.invoke(prompt)
            better_question = response.content.strip()
            print(f"question_rewriter: Rephrased question: {better_question}")
            state["rephrased_question"] = better_question
        else:
            state["rephrased_question"] = state["question"].content
        return state

    def retrieve(state: AgentState):
        print("Entering retrieve")
        documents = retriever.invoke(state["rephrased_question"])
        print(f"retrieve: Retrieved {len(documents)} documents")
        state["documents"] = documents
        return state

    class GradeDocument(BaseModel):
        score: str = Field(
            description="Document is relevant to the question? If yes -> 'Yes' if not -> 'No'"
        )

    # The retrieval_grader checks the relevancy of each retrieved chunk.
    def retrieval_grader(state: AgentState):
        print("Entering retrieval_grader")
        system_message = SystemMessage(
            content="""You are a grader assessing the relevance of a retrieved document to a user question.
    Only answer with 'Yes' or 'No'.

    If the document contains information relevant to the user's question, respond with 'Yes'.
    Otherwise, respond with 'No'."""
        )

        structured_llm = llm.with_structured_output(GradeDocument)

        relevant_docs = []
        for doc in state["documents"]:
            human_message = HumanMessage(
                # content=f"User question: {state['rephrased_question']}\n\nRetrieved document:\n{doc.page_content}"
                content=f"User question: {state['rephrased_question']}\n\nRetrieved document:\n{doc}"
            )
            grade_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
            grader_llm = grade_prompt | structured_llm
            result = grader_llm.invoke({})
            print(
                # f"Grading document: {doc.page_content[:30]}... Result: {result.score.strip()}"
                f"Grading document: {doc[:30]}... Result: {result.score.strip()}"
            )
            if result.score.strip().lower() == "yes":
                relevant_docs.append(doc)
        state["documents"] = relevant_docs          # updating all docs with only the relevant set of docs
        state["proceed_to_generate"] = len(relevant_docs) > 0
        print(f"retrieval_grader: proceed_to_generate = {state['proceed_to_generate']}")
        return state

    def proceed_router(state: AgentState):
        print("Entering proceed_router")
        rephrase_count = state.get("rephrase_count", 0)
        if state.get("proceed_to_generate", False):
            print("Routing to generate_answer")
            return "generate_answer"
        elif rephrase_count >= 2:
            print("Maximum rephrase attempts reached. Cannot find relevant documents.")
            return "cannot_answer"
        else:
            print("Routing to refine_question")
            return "refine_question"

    def refine_question(state: AgentState):
        print("Entering refine_question")
        rephrase_count = state.get("rephrase_count", 0)
        if rephrase_count >= 2:
            print("Maximum rephrase attempts reached")
            return state
        question_to_refine = state["rephrased_question"]
        system_message = SystemMessage(
            content="""You are a helpful assistant that slightly refines the user's question to improve retrieval results.
    Provide a slightly adjusted version of the question."""
        )
        human_message = HumanMessage(
            content=f"Original question: {question_to_refine}\n\nProvide a slightly refined question."
        )
        refine_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
        prompt = refine_prompt.format()
        response = llm.invoke(prompt)
        refined_question = response.content.strip()
        print(f"refine_question: Refined question: {refined_question}")
        state["rephrased_question"] = refined_question
        state["rephrase_count"] = rephrase_count + 1
        return state

    # generate_answer: If at least 1 retrieved chunk is relevant to the question, generate the answer
    # If for more then n (say 3) loops the refine question-retrieval loop doesn't retrieve relevant chunks, then go to cannot_answer.

    template = """
    Answer the question based on the following context and the Chat history.
    Especially take the latest question into consideration:

    Chathistory: {history}
    Context: {context}
    Question: {question}

    Only answer the question, don't mention in output like "Based on the context and chat history, I understand that you are asking about "

    """
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = prompt | llm

    def generate_answer(state: AgentState):
        print("Entering generate_answer")
        if "messages" not in state or state["messages"] is None:
            raise ValueError("State must include 'messages' before generating an answer.")

        history = state["messages"]
        documents = state["documents"]
        rephrased_question = state["rephrased_question"]

        formatted_context = "\n\n".join(doc for doc in documents)

        response = rag_chain.invoke(
            {"history": history, "context": formatted_context, "question": rephrased_question}
        )

        generation = response.content.strip()

        state["messages"].append(AIMessage(content=generation))
        print(f"generate_answer: Generated response: {generation}")
        return state

    def cannot_answer(state: AgentState):
        print("Entering cannot_answer")
        if "messages" not in state or state["messages"] is None:
            state["messages"] = []
        state["messages"].append(
            AIMessage(
                content="I'm sorry, but I cannot find the information you're looking for."
            )
        )
        return state

    # --- LANGGRAPH: BUILDING THE GRAPH ---

    checkpointer = MemorySaver()

    workflow = StateGraph(AgentState)

    workflow.add_node("question_rewriter", question_rewriter)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("retrieval_grader", retrieval_grader)
    workflow.add_node("generate_answer", generate_answer)
    workflow.add_node("refine_question", refine_question)
    workflow.add_node("cannot_answer", cannot_answer)

    workflow.add_edge("question_rewriter", "retrieve")
    workflow.add_edge("retrieve", "retrieval_grader")

    workflow.add_conditional_edges(
        "retrieval_grader",
        proceed_router,
        {
            "generate_answer": "generate_answer",
            "refine_question": "refine_question",
            "cannot_answer": "cannot_answer",
        },
    )
    workflow.add_edge("refine_question", "retrieve")
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("cannot_answer", END)

    workflow.set_entry_point("question_rewriter")

    graph = workflow.compile(checkpointer=checkpointer)

    # --- QUERY, RETRIEVAL & GENERATION---

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if flag:
        user_query = st.text_input("Ask a question:")

        if user_query:
            input_data = {"question": HumanMessage(content=user_query)}
            response = graph.invoke(input=input_data, 
                                    config={"configurable": {"thread_id": st.session_state.thread_id}})
            st.write(response['messages'][-1].content)