import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add the current directory to the path to import our chatbot modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the chatbot components
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from openai import AzureOpenAI
import httpx
import json
from dotenv import load_dotenv

# Import Quick Actions functions
from quick_actions import (
    reset_password, 
    request_admin_permission, 
    unblock_account, 
    submit_ticket, 
    request_wifi_access
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="IT Helpdesk Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .status-online {
        color: #4caf50;
        font-weight: bold;
    }
    .status-offline {
        color: #f44336;
        font-weight: bold;
    }
    .status-warning {
        color: #ff9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'embeddings_initialized' not in st.session_state:
    st.session_state.embeddings_initialized = False
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'retrieval_chain' not in st.session_state:
    st.session_state.retrieval_chain = None
if 'chat_model' not in st.session_state:
    st.session_state.chat_model = None

# Functions from the original chatbot
def check_system_status(device_id: str) -> str:
    """Mock function simulating system status check"""
    status_map = {
        "printer01": "Online and functioning normally.",
        "router23": "Offline, requires maintenance.",
        "server07": "Online but high CPU usage detected.",
        "laptop45": "Online and functioning normally.",
        "desktop12": "Offline, power supply issue detected.",
        "switch05": "Online, all ports active.",
        "firewall02": "Online, last rule update: 2 hours ago.",
        "scanner09": "Online, low toner warning.",
        "tablet21": "Online, battery at 80%.",
        "monitor33": "Online, no issues detected.",
        "phone88": "Offline, network unreachable.",
        "projector14": "Online, lamp replacement recommended soon.",
        "nas01": "Online, disk usage at 75%.",
        "camera17": "Online, recording active.",
        "accesspoint03": "Online, 12 users connected.",
    }
    return status_map.get(device_id, "Device not found.")

def load_knowledge_base_from_csv(csv_file="helpdesk_knowledge_base.csv"):
    """Load IT helpdesk knowledge base from CSV file"""
    try:
        csv_path = os.path.join(current_dir, csv_file)
        df = pd.read_csv(csv_path)
        
        documents = []
        for _, row in df.iterrows():
            doc = f"{row['question']} {row['solution']}"
            documents.append(doc)
        
        return documents, df
        
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        # Fallback documents
        fallback_docs = [
            "How to reset my password? Visit the password reset page and follow the instructions.",
            "My computer is slow. Restart, close apps, run antivirus scan.",
            "Connect to VPN by installing client from IT portal and login.",
            "Printer issues: check paper jam, ensure toner is full, restart printer.",
        ]
        fallback_df = pd.DataFrame({
            'category': ['Password', 'Performance', 'Network', 'Hardware'],
            'question': ['How to reset my password?', 'My computer is slow', 'Connect to VPN', 'Printer issues'],
            'solution': ['Visit the password reset page and follow the instructions.',
                        'Restart, close apps, run antivirus scan.',
                        'Install client from IT portal and login.',
                        'Check paper jam, ensure toner is full, restart printer.']
        })
        return fallback_docs, fallback_df

# Quick Actions Functions are imported from quick_actions.py

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot components"""
    try:
        # Load environment variables
        ssl_verify = os.getenv("SSL_VERIFY", "false").lower() == "true"
        http_client = httpx.Client(verify=ssl_verify)
        
        AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        AZURE_EMBEDDINGS_ENDPOINT = os.getenv("AZURE_EMBEDDINGS_ENDPOINT")
        AZURE_EMBEDDINGS_API_KEY = os.getenv("AZURE_EMBEDDINGS_API_KEY")
        
        # Load knowledge base
        documents, knowledge_df = load_knowledge_base_from_csv()
        
        # Initialize embeddings
        embeddings = AzureOpenAIEmbeddings(
            model="text-embedding-3-small",
            api_version="2024-02-01",
            azure_endpoint=AZURE_EMBEDDINGS_ENDPOINT,
            api_key=AZURE_EMBEDDINGS_API_KEY,
            http_client=http_client
        )
        
        # Create vector store
        vector_store = FAISS.from_texts(documents, embedding=embeddings)
        
        # Initialize chat model
        chat_model = AzureChatOpenAI(
            azure_deployment="GPT-4o-mini",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version="2024-02-01",
            api_key=AZURE_OPENAI_API_KEY
        )
        
        # Setup retrieval chain
        retrieval_chain = ConversationalRetrievalChain.from_llm(
            llm=chat_model,
            retriever=vector_store.as_retriever(),
            return_source_documents=True
        )
        
        return {
            'vector_store': vector_store,
            'retrieval_chain': retrieval_chain,
            'chat_model': chat_model,
            'knowledge_df': knowledge_df,
            'documents_count': len(documents),
            'categories': knowledge_df['category'].unique().tolist(),
            'initialized': True
        }
        
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return {'initialized': False, 'error': str(e)}

def chat_with_functions(user_input, chat_history):
    """Handle function calling for system status checks"""
    try:
        # Environment variables
        AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
        
        ssl_verify = os.getenv("SSL_VERIFY", "false").lower() == "true"
        http_client = httpx.Client(verify=ssl_verify)
        
        client = AzureOpenAI(
            api_version="2024-02-01",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            http_client=http_client
        )
        
        # Build messages
        messages = [{"role": "system", "content": "You are a helpful IT support assistant."}]
        for question, answer in chat_history:
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "user", "content": user_input})
        
        # Function definition
        functions = [{
            "name": "check_system_status",
            "description": "Check the status of a device",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "The ID of the device to check"
                    }
                },
                "required": ["device_id"]
            }
        }]
        
        response = client.chat.completions.create(
            model="GPT-4o-mini",
            messages=messages,
            tools=[{"type": "function", "function": functions[0]}],
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "check_system_status":
                result = check_system_status(function_args["device_id"])
                return result, True
        
        return message.content, False
        
    except Exception as e:
        return f"Error in function calling: {e}", False

# Main UI
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 IT Helpdesk Chatbot</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Status")
        
        # Initialize chatbot
        if not st.session_state.embeddings_initialized:
            with st.spinner("Initializing chatbot..."):
                chatbot_data = initialize_chatbot()
                if chatbot_data['initialized']:
                    st.session_state.vector_store = chatbot_data['vector_store']
                    st.session_state.retrieval_chain = chatbot_data['retrieval_chain']
                    st.session_state.chat_model = chatbot_data['chat_model']
                    st.session_state.knowledge_df = chatbot_data['knowledge_df']
                    st.session_state.embeddings_initialized = True
                    st.success("✅ Chatbot initialized successfully!")
                        
                else:
                    st.error("❌ Failed to initialize chatbot")
                    st.text(chatbot_data.get('error', 'Unknown error'))
        
        # Quick Actions (always visible after initialization)
        if st.session_state.embeddings_initialized:
            st.subheader("⚡ Quick Actions")
            
            if st.button("🔐 Reset Password", key="reset_pwd", use_container_width=True):
                result = reset_password()
                st.balloons()
                # Create a popup dialog
                @st.dialog("🔐 Reset Password - Action Completed!")
                def show_reset_password_dialog():
                    st.success("Password reset process has been initiated successfully!")
                    st.markdown(result)
                    if st.button("Close", key="close_reset"):
                        st.rerun()
                show_reset_password_dialog()
            
            if st.button("🔑 Request Admin Permission", key="admin_perm", use_container_width=True):
                result = request_admin_permission()
                st.balloons()
                # Create a popup dialog
                @st.dialog("🔑 Admin Permission - Request Submitted!")
                def show_admin_permission_dialog():
                    st.success("Admin permission request has been submitted successfully!")
                    st.markdown(result)
                    if st.button("Close", key="close_admin"):
                        st.rerun()
                show_admin_permission_dialog()
            
            if st.button("🔓 Unblock Account", key="unblock_acc", use_container_width=True):
                result = unblock_account()
                st.balloons()
                # Create a popup dialog
                @st.dialog("🔓 Unblock Account - Action Completed!")
                def show_unblock_account_dialog():
                    st.success("Account unblock process has been completed successfully!")
                    st.markdown(result)
                    if st.button("Close", key="close_unblock"):
                        st.rerun()
                show_unblock_account_dialog()
            
            if st.button("🎫 Submit Ticket", key="submit_ticket", use_container_width=True):
                result = submit_ticket()
                st.balloons()
                # Create a popup dialog
                @st.dialog("🎫 Support Ticket - Created Successfully!")
                def show_submit_ticket_dialog():
                    st.success("IT support ticket has been created successfully!")
                    st.markdown(result)
                    if st.button("Close", key="close_ticket"):
                        st.rerun()
                show_submit_ticket_dialog()
            
            if st.button("📶 Request WiFi Access", key="wifi_access", use_container_width=True):
                result = request_wifi_access()
                st.balloons()
                # Create a popup dialog
                @st.dialog("📶 WiFi Access - Request Processed!")
                def show_wifi_access_dialog():
                    st.success("WiFi access request has been processed successfully!")
                    st.markdown(result)
                    if st.button("Close", key="close_wifi"):
                        st.rerun()
                show_wifi_access_dialog()
        
    # Main chat interface
    if st.session_state.embeddings_initialized:
        st.subheader("💬 Chat with IT Support")
        
        # Display chat history
        for i, (question, answer, timestamp) in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f'''
            <div class="chat-message user-message">
                <strong>🙋 You ({timestamp}):</strong><br>
                {question}
            </div>
            ''', unsafe_allow_html=True)
            
            # Bot response
            st.markdown(f'''
            <div class="chat-message bot-message">
                <strong>🤖 IT Support:</strong><br>
                {answer}
            </div>
            ''', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Type your question here...")
        
        if user_input:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            with st.spinner("🔍 Searching knowledge base..."):
                try:
                    # Get answer from retrieval chain
                    rag_result = st.session_state.retrieval_chain.invoke({
                        "question": user_input, 
                        "chat_history": [(q, a) for q, a, _ in st.session_state.chat_history]
                    })
                    
                    knowledge_answer = rag_result['answer']
                    
                    # Check for function calling
                    func_answer, is_function_call = chat_with_functions(
                        user_input, 
                        [(q, a) for q, a, _ in st.session_state.chat_history]
                    )
                    
                    # Combine answers
                    if is_function_call:
                        final_answer = f"📚 {knowledge_answer}\n\n🔧 *System Status:  {func_answer}"
                    else:
                        final_answer = f"📚 {knowledge_answer}\n\n💡 *Additional Info:  {func_answer}"
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_input, final_answer, timestamp))
                    
                    # Rerun to update the display
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing request: {e}")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
            
    else:
        st.warning("⏳ Please wait for the chatbot to initialize...")
        
    # Footer
    st.markdown("---")
    st.markdown("🔧 **Features:** Vector-based search | Function calling | CSV knowledge base | Real-time chat")

if __name__ == "__main__":
    main()
