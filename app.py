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
        with st.spinner("Agents are researching and writing your report... please wait..."):
           try:
             llm = LLM(
                model="gemini/gemini-2.0-flash",
                api_key=api_key
 )
  
             researcher = Agent(
                 role="Senior AI Researcher",
                 goal=f"Discover top trends and breakthroughs regarding: {topic}",
                 backstory="You are an expert researcher with an eye for breakthrough insights.",
                 llm=llm,
                 verbose=True
 )
 
             writer = Agent(
              role="Technical Brief Writer",
              goal=f"Summarize research on {topic} into an executive brief",
              backstory="You are an engineering communicator who writes clear project briefs.",
              llm=llm,
              verbose=True
 )
 
             task1 = Task(
              description=f"List 3 key ways technology/AI is transforming {topic}.",
              expected_output="3 structured bullet points with technical specifics.",
              agent=researcher
 )
 
             task2 = Task(
             description="Using the researcher findings, write a 2-paragraph seminar summary.",
             expected_output="A polished 2-paragraph executive report.",
             agent=writer
)

             crew = Crew(
             agents=[researcher, writer],
             tasks=[task1, task2],
             process=Process.sequential
 )
             result = crew.kickoff()

             st.success("Multi-Agent Collaboration Completed!")
             st.subheader("Final Generated Report:")
             st.markdown(result.raw if hasattr(result, "raw") else str(result))

finally block as e:
     st.error(f"Error occurred:{e}")

    
