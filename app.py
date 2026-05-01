import streamlit as st
from chatbot.graph import build_graph

st.set_page_config(page_title="Attrition AI", layout="wide")

graph = build_graph()

# 🔥 CUSTOM CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: white;
}

.main-title {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
}

.gradient {
    background: linear-gradient(90deg, #22d3ee, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #cbd5f5;
    margin-top: 10px;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🧠 HERO SECTION
st.markdown(
    '<div class="main-title">Predict employee <span class="gradient">attrition</span> with AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered system that predicts who will leave — and why</div>',
    unsafe_allow_html=True
)

st.markdown("###")

# 🔘 MODE SWITCH
mode = st.radio("", ["Chatbot", "Prediction Form"], horizontal=True)

st.markdown("---")

# =========================
# 🤖 CHATBOT MODE
# =========================
if mode == "Chatbot":

    st.subheader("💬 Chat with AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask about employee attrition...")

    if user_input:
        result = graph.invoke({"input": user_input})

        st.session_state.messages.append(("user", user_input))
        st.session_state.messages.append(("bot", result["output"]))

    for role, msg in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

# =========================
# 📊 FORM MODE
# =========================
else:
    st.subheader("📊 Employee Prediction Form")

    col1, col2 = st.columns(2)

    with col1:
        satisfaction = st.slider("Satisfaction Level", 0.0, 1.0, 0.5)
        evaluation = st.slider("Last Evaluation", 0.0, 1.0, 0.7)
        projects = st.number_input("Number of Projects", 1, 10, 4)

    with col2:
        hours = st.number_input("Monthly Hours", 50, 300, 200)
        years = st.number_input("Years at Company", 1, 10, 3)
        department = st.selectbox("Department", ["sales", "IT", "HR", "support"])
        salary = st.selectbox("Salary", ["low", "medium", "high"])

    st.markdown("###")

    if st.button("🚀 Predict Attrition"):
        query = f"""
        satisfaction={satisfaction}, evaluation={evaluation},
        {projects} projects, {hours} hours, {years} years,
        {department}, {salary} salary
        """

        result = graph.invoke({"input": query})

        st.success(result["output"])

# 📊 STATS SECTION
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card"><h2>94.2%</h2><p>Model Accuracy</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h2>14.9k</h2><p>Records Trained</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><h2>7</h2><p>Features</p></div>', unsafe_allow_html=True)