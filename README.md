# 🤖 Agentic AI Framework Recommender

An intelligent Streamlit application that helps you choose the best AI framework for your automation and agentic AI projects. Powered by Google's Gemini AI, this tool analyzes your project requirements and provides personalized recommendations from popular frameworks like n8n, LangGraph, CrewAI, and AutoGen.

## ✨ Features

- **🎯 Smart Recommendations**: AI-powered analysis of your project requirements
- **🔍 Task Validation**: Automatically validates if your request is suitable for agentic AI systems
- **📊 Framework Comparison**: Detailed comparison of popular AI frameworks
- **👨‍💻 Experience-Based Suggestions**: Tailored recommendations based on your coding experience
- **📚 Comprehensive Framework Guide**: In-depth information about each framework's strengths and use cases

## 🛠️ Supported Frameworks

| Framework | Type | Best For | Complexity |
|-----------|------|----------|------------|
| **n8n** | Visual Workflow | Business Automation, No-code | Low |
| **LangGraph** | Stateful LLM Apps | Complex Reasoning, Research | High |
| **CrewAI** | Role-based Agents | Team Collaboration, Creative Tasks | Medium |
| **AutoGen** | Conversational AI | Interactive Agents, Code Generation | Medium |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shkkonda/ai-framework-finder.git
   cd ai-framework-finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   **Option A: Environment Variables (Local Development)**
   ```bash
   # Create a .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

   **Option B: Streamlit Secrets (Deployment)**
   ```toml
   # Create .streamlit/secrets.toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📦 Dependencies

Create a `requirements.txt` file with:

```
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

## 🎯 How It Works

1. **Describe Your Project**: Enter details about your AI automation system or agentic AI project
2. **Select Experience Level**: Choose your coding experience (Yes/No) for tailored recommendations
3. **Get AI-Powered Analysis**: The system validates your request and analyzes requirements
4. **Receive Recommendations**: Get detailed suggestions with implementation tips and potential challenges
5. **Explore Alternatives**: Review alternative frameworks and detailed comparisons

## 💡 Example Use Cases

### ✅ Valid Requests
- "Personalized email generator that analyzes company websites and creates tailored outreach"
- "Multi-agent system for customer service automation"
- "AI workflow for lead qualification and scoring"
- "Intelligent document processing pipeline"
- "Automated content creation and publishing system"

### ❌ Invalid Requests
- General programming questions
- Basic calculators or static tools
- Educational AI concept explanations
- Simple websites without AI components

## 🏗️ Project Structure

```
ai-framework-finder/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .streamlit/
│   └── secrets.toml      # Streamlit secrets (for deployment)
└── README.md            # This file
```

## 🌐 Deployment

### Streamlit Cloud

1. **Fork this repository**
2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository

3. **Add secrets**
   - In your Streamlit Cloud dashboard
   - Go to "Secrets" section
   - Add: `GEMINI_API_KEY = "your_api_key_here"`

4. **Deploy**
   - Your app will be automatically deployed
   - Get a shareable URL

### Local Development

```bash
# Clone and setup
git clone https://github.com/shkkonda/ai-framework-finder.git
cd ai-framework-finder
pip install -r requirements.txt

# Add your API key to .env
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Streamlit Secrets

For deployment, add to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Ideas for Contributions

- Add more AI frameworks (Langchain, Haystack, etc.)
- Improve recommendation algorithms
- Add more detailed implementation guides
- Create framework-specific tutorials
- Enhance the UI/UX
- Add support for more AI models

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powering the intelligent recommendations
- **Streamlit** for the amazing web app framework
- **Framework Communities** (n8n, LangGraph, CrewAI, AutoGen) for building excellent tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/shkkonda/ai-framework-finder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shkkonda/ai-framework-finder/discussions)
- **Email**: shriharsha@appweave.tech

## 🔮 Roadmap

- [ ] Add more AI frameworks
- [ ] Implement user authentication
- [ ] Save recommendation history
- [ ] Add framework-specific tutorials
- [ ] Create API endpoints
- [ ] Add multi-language support
- [ ] Implement advanced filtering options

---

**Made with ❤️ and AI**

*Help others discover the perfect AI framework for their projects!*
