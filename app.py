import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM

st.set_page_config(page_title="Multi-Agent AI Hub", layout="centered")

st.title("Autonomous Multi-Agent System")
st.write("A collaborative AI system powered by CrewAI & Google Gemini.")

api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
topic = st.text_input("Enter Research Topic:", placeholder="e.g. AI in Renewable Energy Grids")

if st.button("Run Multi-Agent System"):
    if not api_key:
        st.warning("Please enter your Gemini API Key first.")
    elif not topic:
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Agents are working... please wait..."):
            llm = LLM(
                model="gemini/gemini-2.0-flash",
                api_key=api_key
            )

            researcher = Agent(
                role="Senior AI Researcher",
                goal=f"Discover breakthroughs in: {topic}",
                backstory="Expert AI researcher.",
                llm=llm
            )

            writer = Agent(
                role="Technical Brief Writer",
                goal=f"Summarize findings on {topic}",
                backstory="Technical communicator.",
                llm=llm
            )

            task1 = Task(
                description=f"List 3 key ways AI transforms {topic}.",
                expected_output="3 bullet points.",
                agent=researcher
            )

            task2 = Task(
                description="Write a 2-paragraph executive report based on the research.",
                expected_output="A polished 2-paragraph summary.",
                agent=writer
            )

            crew = Crew(
                agents=[researcher, writer],
                tasks=[task1, task2],
                process=Process.sequential
            )

            result = crew.kickoff()

            st.success("Completed!")
            st.subheader("Final Report:")
            st.markdown(result.raw if hasattr(result, "raw") else str(result))
