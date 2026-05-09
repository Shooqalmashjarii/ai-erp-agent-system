from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import sys, os
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

print("Starting Router Agent...")

# 1. LLM Setup
print("Initializing LLM...")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)
print("LLM ready")

# 2. Import All Agents (Fixed Paths)
try:
    from agents.salesAgent import SalesReactAgent
    sales_agent_instance = SalesReactAgent()
    print("✅ Sales Agent loaded")
except Exception as e:
    print(f"⚠️ Failed to load Sales Agent: {e}")
    sales_agent_instance = None

try:
    from agents.inventory_agent import InventoryAgent2
    print("✅ Inventory Agent loaded")
except Exception as e:
    print(f"⚠️ Failed to load Inventory Agent: {e}")
    InventoryAgent2 = None

try:
    from agents.analyticsAgent import AnalyticsReActAgent
    analytics_agent_instance = AnalyticsReActAgent()
    print("✅ Analytics Agent loaded")
except Exception as e:
    print(f"⚠️ Failed to load Analytics Agent: {e}")
    analytics_agent_instance = None

# 3. Intent Classification Tool
def classify_intent(query: str) -> str:
    prompt = f"""
    You are an intent classifier for an ERP system. 
    Classify the user query into one of these agents only:
    - SALES_AGENT
    - inventory_agent
    - ANALYTICS_AGENT

    Query: "{query}"

    Respond ONLY with the agent name.
    """
    response = llm([HumanMessage(content=prompt)])
    agent_name = response.content.strip().upper()
    return agent_name

def execute_agent(agent_type: str, query: str) -> str:
    print(f"🎯 Executing {agent_type} with query: {query}")
    try:
        if agent_type == "SALES_AGENT" and sales_agent_instance:
            return sales_agent_instance.invoke( query)
        elif agent_type == "inventory_agent" and InventoryAgent2:
            result = InventoryAgent2({"input": query})
            return str(result.get("output", result))
        elif agent_type == "ANALYTICS_AGENT" and analytics_agent_instance:
            result = analytics_agent_instance.invoke({"input": query})
            return str(result.get("output", result))
        else:
            return f"❌ Agent {agent_type} not available."
    except Exception as e:
        print(f"❌ Error executing {agent_type}: {e}")
        return f"Error executing {agent_type}: {str(e)}"

intent_tool = Tool(
    name="Intent_Classifier",
    func=classify_intent,
    description="Route query to SALES_AGENT, inventory_agent, or ANALYTICS_AGENT."
)

agent_executor_tool = Tool(
    name="Execute_Agent",
    func=lambda query_with_agent: execute_agent(*query_with_agent.split("|", 1)),
    description="Execute agent with format 'AGENT_TYPE|query'."
)

# 4. SQL Tool
try:
    DB_PATH = r"db/erp.db"
    print(f"🔍 Checking database at: {DB_PATH}")
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"❌ Database not found at: {DB_PATH}")

    DB_URI = f"sqlite:///{DB_PATH.replace(os.sep, '/')}"
    print(f"🔗 Connecting to DB: {DB_URI}")
    db = SQLDatabase.from_uri(DB_URI)

    def run_sql(query: str) -> str:
        print(f"💾 Running SQL: {query}")
        try:
            result = db.run(query)
            print(f"✅ SQL Result: {result}")
            return result
        except Exception as e:
            print(f"❌ SQL Error: {e}")
            return f"SQL Error: {e}"

    sql_tool = Tool(
        name="RouterSQL",
        func=run_sql,
        description="Check approvals, messages, or statuses directly from DB."
    )
    print("✅ SQL Tool ready")
except Exception as e:
    print(f"⚠️ SQL Tool failed: {e}")
    sql_tool = Tool(
        name="RouterSQL",
        func=lambda x: "Database unavailable.",
        description="Fallback SQL tool"
    )

# 5. Build Router Agent (LangChain)
tools = [intent_tool, agent_executor_tool, sql_tool]

system_prompt = """You are the Router Agent for Helios Dynamics ERP.

Workflow:
1. Use 'Intent_Classifier' to determine which agent should handle the query
2. Use 'Execute_Agent' with format 'AGENT_TYPE|query' to run it
3. If agents fail, use 'RouterSQL' for direct database queries
4. Never guess — always use tools.
"""

from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("placeholder", "{messages}")
])

print("🛠️ Creating Router Agent (LangChain)...")
router_agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

print("✅ Router Agent ready")

# 6. Test Function
def run_query(query: str):
    print("=" * 60, "Question" , "=" * 60)
    print(f"\n🧪 Testing Router Agent with query: '{query}'")
    print("=" * 60)

    try:
        result = router_agent.run(query)
        print("=" * 60, "Answer" , "=" * 60)
        print(f"📢 Final Router Response: {result}")
        print("=" * 60)

        return result
    except Exception as e:
        print(f"❌ Router Agent Error: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    test_query = "who are the most paying customers?"
    run_query(test_query)
