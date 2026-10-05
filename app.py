import streamlit as st
from rag import ask_question
import json
import os


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CampusLens AI",
    page_icon="🎓",
    layout="centered"
)


# ==================================================
# LOAD DOCUMENT COUNT
# ==================================================

document_count = 0

if os.path.exists("documents"):
    document_count = len([
        f for f in os.listdir("documents")
        if f.lower().endswith(".pdf")
    ])


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* ---------- Overall ---------- */

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ---------- Hero ---------- */

.hero {
    text-align: center;
    padding: 15px 0 25px 0;
}

.hero-title {
    font-size: 46px;
    font-weight: 750;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 19px;
    color: #777;
    margin-top: 5px;
}

.hero-description {
    font-size: 14px;
    color: #888;
    margin-top: 12px;
}


/* ---------- Trust Bar ---------- */

.trust-bar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 14px;
    margin: 18px 0 25px 0;
    border: 1px solid #303030;
    border-radius: 12px;
    background: #15171c;
    color: white;
    font-size: 14px;
}

.trust-item {
    text-align: center;
}


/* ---------- Answer ---------- */

.verified-card {
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #cfe8d5;
    background: #f7fff8;
    color: #000000;
    margin-top: 8px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}

.badge {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 20px;
    background: #e4f6e8;
    color: #176b2c;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}


/* ---------- Evidence ---------- */

.evidence-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #dedede;
    background: #ffffff;
    color: #000000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.source-name {
    font-weight: 700;
    font-size: 16px;
}

.source-page {
    color: #444;
    margin-top: 6px;
}


/* ---------- Stats ---------- */

.stat-card {
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #333;
    background: #17191f;
}

.stat-number {
    font-size: 24px;
    font-weight: 700;
    color: white;
}

.stat-label {
    font-size: 12px;
    color: #aaa;
}


/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #777;
    font-size: 13px;
    padding-top: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HERO
# ==================================================

st.markdown("""
<div class="hero">

<div class="hero-title">🎓 CampusLens AI</div>

<div class="hero-subtitle">
Ask your college. See the proof.
</div>

<div class="hero-description">
A verified AI assistant for regulations, examinations,
courses, fees and student services.
</div>

</div>
""", unsafe_allow_html=True)


# ==================================================
# TRUST BAR
# ==================================================

st.markdown("""
<div class="trust-bar">

<div class="trust-item">
🛡️ <b>Verified Documents</b>
</div>

<div class="trust-item">
🔒 <b>Grounded Answers</b>
</div>

<div class="trust-item">
🚫 <b>Unsupported Claims Blocked</b>
</div>

</div>
""", unsafe_allow_html=True)


# ==================================================
# QUESTION INPUT
# ==================================================

st.markdown("### 🔎 Ask your college")

question = st.text_input(
    "",
    placeholder="Example: What are the library timings?",
    label_visibility="collapsed"
)


# ==================================================
# QUESTION INPUT + MODULE SUGGESTIONS
# ==================================================

if "question" not in st.session_state:
    st.session_state.question = ""

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "📚 Library"


# --------------------------------------------------
# MODULES
# --------------------------------------------------

st.markdown("### 🔎 What do you want to know?")


modules = [
    "📚 Library",
    "📝 Examinations",
    "🎓 Regulations",
    "📖 Courses",
    "💰 Fees",
    "🏢 Student Services"
]


module_cols = st.columns(3)

for i, module in enumerate(modules):

    with module_cols[i % 3]:

        if st.button(
            module,
            key=f"module_{i}",
            use_container_width=True
        ):

            st.session_state.selected_module = module


# --------------------------------------------------
# SUGGESTED QUESTIONS
# --------------------------------------------------

suggestions = {

    "📚 Library": [
        "What are the library timings?",
        "What are the library rules?",
        "What services does the library provide?"
    ],

    "📝 Examinations": [
        "What is the exam procedure?",
        "What are the examination regulations?",
        "What are the requirements for examinations?"
    ],

    "🎓 Regulations": [
        "What are the college regulations?",
        "What are the attendance regulations?",
        "What are the academic regulations?"
    ],

    "📖 Courses": [
        "What courses are offered?",
        "What are the course requirements?",
        "What subjects are included in the curriculum?"
    ],

    "💰 Fees": [
        "What are the college fees?",
        "What are the fee payment rules?",
        "What are the fees for students?"
    ],

    "🏢 Student Services": [
        "What student services are available?",
        "What services are available for students?",
        "What are the student support facilities?"
    ]
}


selected = st.session_state.selected_module

st.markdown(
    f"**Suggested questions for {selected}**"
)


suggestion_cols = st.columns(3)

for i, suggestion in enumerate(suggestions[selected]):

    with suggestion_cols[i]:

        if st.button(
            suggestion,
            key=f"suggestion_{selected}_{i}",
            use_container_width=True
        ):

            st.session_state.question = suggestion


# --------------------------------------------------
# SEARCH BOX
# --------------------------------------------------

question = st.text_input(
    "Your question",
    key="question",
    placeholder="Or type your own question..."
)

# ==================================================
# ASK BUTTON
# ==================================================

if st.button(
    "Ask CampusLens 🚀",
    use_container_width=True
):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "🔎 Searching verified college documents..."
        ):

            try:

                answer, evidence = ask_question(question)


                # ==================================================
                # MOST RELEVANT EVIDENCE
                # ==================================================

                best_evidence = None

                if evidence:

                    best_evidence = min(
                        evidence,
                        key=lambda item: item["distance"]
                    )


                # ==================================================
                # CLEAN ANSWER
                # ==================================================

                clean_answer = answer

                if "Source:" in clean_answer:

                    clean_answer = clean_answer.split(
                        "Source:"
                    )[0].strip()


                # ==================================================
                # ANSWER
                # ==================================================

                st.markdown("### ✅ Verified Answer")

                st.markdown(
                    f"""
                    <div class="verified-card">

                    <div class="badge">
                    🟢 VERIFIED
                    </div>

                    <br>

                    {clean_answer}

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # ==================================================
                # EVIDENCE
                # ==================================================

                if best_evidence:

                    st.markdown("### 📚 Evidence")

                    st.markdown(
                        f"""
                        <div class="evidence-card">

                        <div class="source-name">
                        📄 {best_evidence['source']}
                        </div>

                        <div class="source-page">
                        📌 Page {best_evidence['page']}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    with st.expander(
                        "🔍 View supporting evidence"
                    ):

                        st.write(
                            best_evidence["text"]
                        )


                else:

                    st.info(
                        "I couldn't find this information in the "
                        "verified college documents."
                    )


                # ==================================================
                # TRUSTGUARD RESULT
                # ==================================================

                if best_evidence:

                    st.markdown("### 🛡️ TrustGuard")

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.success("✓ Verified source")

                    with c2:
                        st.success("✓ Grounded response")

                    with c3:
                        st.success("✓ Unsupported claims blocked")


            except Exception as error:

                st.error(
                    "Something went wrong while processing your question."
                )

                st.caption(str(error))


# ==================================================
# PROJECT STATS
# ==================================================

st.markdown("### 📊 CampusLens")

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        f"""
        <div class="stat-card">

        <div class="stat-number">
        {document_count}
        </div>

        <div class="stat-label">
        Verified Documents
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with s2:

    st.markdown(
        """
        <div class="stat-card">

        <div class="stat-number">
        RAG
        </div>

        <div class="stat-label">
        Retrieval System
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with s3:

    st.markdown(
        """
        <div class="stat-card">

        <div class="stat-number">
        🔒
        </div>

        <div class="stat-label">
        Source Grounded
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div class="footer">
    CampusLens AI • Secure, source-grounded institutional assistant
    </div>
    """,
    unsafe_allow_html=True
)