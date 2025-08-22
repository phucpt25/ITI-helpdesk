# 🤖 IT Helpdesk Chatbot

A modern, AI-powered IT helpdesk chatbot built with Streamlit, featuring Quick Actions, popup dialogs, and intelligent knowledge base search using Azure OpenAI and vector embeddings.

![IT Helpdesk Chatbot](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft_Azure-0089D0?style=for-the-badge&logo=microsoft-azure&logoColor=white)

## ✨ Features

### 🚀 Core Functionality
- **Intelligent Chat Interface**: Natural language conversation with IT support knowledge
- **Vector-based Search**: FAISS embeddings for accurate knowledge retrieval
- **Function Calling**: Dynamic system status checks and automated responses
- **CSV Knowledge Base**: Easy-to-maintain knowledge database with 103+ IT solutions

### ⚡ Quick Actions (with Popup Dialogs)
- **🔐 Reset Password**: Automated password reset with temporary credentials
- **🔑 Request Admin Permission**: Permission request workflow with ticket tracking
- **🔓 Unblock Account**: Account unlock process with security recommendations
- **🎫 Submit Ticket**: IT support ticket creation with tracking information
- **📶 Request WiFi Access**: Guest network access with temporary credentials

### 🎨 User Experience
- **Modal Popup Dialogs**: Professional popup responses for Quick Actions
- **Balloons Animation**: Visual feedback for successful actions
- **Responsive Design**: Clean, modern interface with custom CSS styling
- **Real-time Chat**: Live conversation history with timestamps
- **Easy Initialization**: One-click chatbot setup

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Azure OpenAI (GPT-4o-mini, text-embedding-3-small)
- **Vector Database**: FAISS
- **Language Framework**: LangChain
- **Data Storage**: CSV files
- **Authentication**: Azure OpenAI API keys
- **Python Version**: 3.8+

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed
2. **Azure OpenAI API access** with the following:
   - GPT-4o-mini deployment
   - text-embedding-3-small embedding model
   - API keys and endpoints
3. **Required Python packages** (see requirements below)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Workshop4
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install streamlit langchain-openai langchain-community faiss-cpu pandas python-dotenv httpx openai
```

### 4. Environment Configuration
Create a `.env` file in the Workshop4 directory:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_EMBEDDINGS_ENDPOINT=https://your-embeddings-resource.openai.azure.com/
AZURE_EMBEDDINGS_API_KEY=your-embeddings-api-key-here

# Optional SSL Configuration
SSL_VERIFY=false
```

### 5. Knowledge Base Setup
Ensure `helpdesk_knowledge_base.csv` is in the Workshop4 directory with the following structure:
```csv
Category,Problem,Solution
Password,How to reset my password,Visit the password reset page and follow the instructions...
Performance,My computer is slow,Restart your computer and close unnecessary applications...
```

## 🎮 Usage

### Quick Start
1. **Run the Application**:
   ```bash
   streamlit run helpdesk_chatbot_ui.py
   ```

2. **Open Browser**: Navigate to `http://localhost:8501`

3. **Initialize Chatbot**: The chatbot will automatically initialize on first load

4. **Start Using**:
   - Use **Quick Actions** for common tasks (with popup dialogs)
   - Type questions in the **chat interface** for knowledge base search
   - Get **intelligent responses** combining knowledge base and function calling

### Alternative Launch
Use the provided batch file for easy startup:
```bash
start_helpdesk_ui.bat
```

## �️ Architecture & Code Organization

### Modular Design
The application follows a clean, modular architecture:

- **`helpdesk_chatbot_ui.py`**: Main Streamlit application with UI components, chat interface, and dialog management
- **`quick_actions.py`**: Separated module containing all Quick Action functions for better maintainability
- **`helpdesk_knowledge_base.csv`**: Data layer with IT support knowledge

### Benefits of Modular Structure
- **Maintainability**: Easy to update Quick Actions without touching UI code
- **Testability**: Quick Actions can be tested independently
- **Extensibility**: Simple to add new Quick Actions by updating the module
- **Code Clarity**: Clear separation of concerns between UI and business logic

## � Key Features Explained

### Quick Actions with Popup Dialogs
Each Quick Action button triggers:
1. **Balloons animation** for visual feedback
2. **Function execution** with realistic IT workflows
3. **Modal popup dialog** displaying detailed results
4. **Professional formatting** with success indicators

### Intelligent Chat System
- **Knowledge Base Search**: Vector similarity search through FAISS
- **Function Calling**: Automatic system status checks
- **Context Awareness**: Maintains conversation history
- **Hybrid Responses**: Combines multiple information sources

### Knowledge Base Management
- **CSV-based**: Easy editing and maintenance
- **Category Organization**: Structured by IT support areas
- **Vector Indexing**: Automatic embedding generation
- **Real-time Loading**: Dynamic knowledge base updates

## 📁 Project Structure

```
Workshop4/
├── helpdesk_chatbot_ui.py      # Main Streamlit application
├── quick_actions.py            # Quick Actions functions module
├── test_quick_actions.py       # Test suite for Quick Actions module
├── helpdesk_knowledge_base.csv # IT support knowledge database
├── start_helpdesk_ui.bat      # Windows launcher script
├── .env                       # Environment configuration
├── .streamlit/                # Streamlit configuration
├── __pycache__/              # Python cache files
└── README.md                 # This file
```

## ⚙️ Configuration

### Streamlit Configuration
The application uses custom CSS for styling and responsive design. Key configurations:
- **Wide layout** for better space utilization
- **Custom colors** for chat messages and status indicators
- **Professional styling** for buttons and containers

### Azure OpenAI Models
- **Chat Model**: GPT-4o-mini for conversational responses
- **Embedding Model**: text-embedding-3-small for vector search
- **API Version**: 2024-02-01 for latest features

## 🔧 Customization

### Adding New Quick Actions
With the modular structure, adding new Quick Actions is simple:

1. **Add Function to `quick_actions.py`**:
```python
def new_custom_action():
    """Your custom action description"""
    return """🆕 Custom Action Result
    
✅ Function called: new_custom_action()

Your custom response here with:
- Step-by-step results
- Status indicators
- Professional formatting"""

# Update the QUICK_ACTIONS registry
QUICK_ACTIONS['new_custom_action'] = new_custom_action
```

2. **Import in Main UI** (add to imports in `helpdesk_chatbot_ui.py`):
```python
from quick_actions import (
    reset_password, 
    request_admin_permission, 
    unblock_account, 
    submit_ticket, 
    request_wifi_access,
    new_custom_action  # Add your new function
)
```

3. **Add Button to UI** (in the Quick Actions section):
```python
if st.button("🆕 Custom Action", key="custom_action", use_container_width=True):
    result = new_custom_action()
    st.balloons()
    @st.dialog("🆕 Custom Action - Completed!")
    def show_custom_action_dialog():
        st.success("Action completed successfully!")
        st.markdown(result)
        if st.button("Close", key="close_custom"):
            st.rerun()
    show_custom_action_dialog()
```

### Quick Actions Module Functions
The `quick_actions.py` module also provides utility functions:
- `get_quick_action(action_name)`: Get function by name
- `list_available_actions()`: Get list of all available actions
- `QUICK_ACTIONS`: Dictionary registry of all functions

### Testing Quick Actions
Run the test suite to verify Quick Actions functionality:
```bash
python test_quick_actions.py
```

This will test all Quick Action functions and utility methods to ensure they work correctly after separation.

### Updating Knowledge Base
1. **Edit CSV**: Modify `helpdesk_knowledge_base.csv`
2. **Add Categories**: Include new IT support categories
3. **Restart App**: Reinitialize for changes to take effect

## 🐛 Troubleshooting

### Common Issues

**1. Application Won't Start**
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Ensure `.env` file is properly configured

**2. Azure OpenAI Errors**
- Validate API keys and endpoints
- Check deployment names match configuration
- Verify Azure subscription and quotas

**3. Knowledge Base Issues**
- Ensure CSV file exists and is properly formatted
- Check file encoding (UTF-8 recommended)
- Verify CSV structure matches expected format

**4. Quick Actions Not Working**
- Check if chatbot is properly initialized
- Verify popup dialog syntax
- Look for button key conflicts

### Debug Mode
Enable verbose logging by setting environment variable:
```bash
export STREAMLIT_LOG_LEVEL=debug
```

## 📊 Performance

### Optimization Features
- **Caching**: `@st.cache_resource` for chatbot initialization
- **Efficient Embeddings**: FAISS for fast vector operations
- **Minimal UI**: Streamlined interface for better performance
- **Async Operations**: Non-blocking function calls

### Recommended Resources
- **Memory**: 2GB+ RAM for FAISS operations
- **CPU**: Multi-core processor for embedding calculations
- **Network**: Stable internet for Azure OpenAI API calls

## 🔒 Security

### Best Practices Implemented
- **Environment Variables**: Secure API key storage
- **SSL Verification**: Configurable SSL settings
- **Input Validation**: Safe user input handling
- **Error Handling**: Graceful failure management

### Security Considerations
- Keep `.env` file out of version control
- Regularly rotate Azure OpenAI API keys
- Monitor API usage and costs
- Implement rate limiting for production use

## 📈 Future Enhancements

### Planned Features
- **Multi-language Support**: Internationalization
- **User Authentication**: Role-based access control
- **Analytics Dashboard**: Usage statistics and insights
- **Email Integration**: Automated ticket notifications
- **Database Backend**: PostgreSQL/MongoDB integration
- **REST API**: Backend API for mobile apps

### Contributing
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request with detailed description

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- **Issues**: Open GitHub issue with detailed description
- **Documentation**: Check this README and code comments
- **Community**: Join discussions in repository discussions

## 📞 Contact

- **Developer**: Your Name
- **Email**: your.email@example.com
- **Project**: IT Helpdesk Chatbot v1.0

---

**Built with ❤️ using Streamlit and Azure OpenAI**

*Last Updated: August 16, 2025*
