# Eye Disease Classification using Vision Language Model 🔬

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An AI-powered web application that analyzes eye images for common conditions like cataracts, conjunctivitis, and pterygium using advanced Vision Language Models (VLM).

## 🌟 Features

- **Real-time Analysis**: Upload and analyze eye images instantly
- **Multiple Condition Detection**: 
  - Cataracts (clouding, blurry vision)
  - Conjunctivitis (inflammation, redness)
  - Pterygium (tissue growth)
- **Interactive Chat Interface**: Ask specific questions about the uploaded images
- **Educational Information**: Detailed information about each condition
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/talalmuzaffar/Eye-Diseases-Classification-using-VLM.git
cd Eye-Diseases-Classification-using-VLM
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.streamlit/secrets.toml` file
   - Add your Groq API key:
     ```toml
     GROQ_API_KEY = "your-api-key-here"
     ```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## 💡 Usage

1. Upload an eye image using the sidebar uploader
2. Ask questions about the image in the chat interface
3. View the AI's analysis and recommendations
4. Use suggested questions or ask your own specific queries

## ⚠️ Disclaimer

This application is for educational purposes only and should not be used for medical diagnosis. Always consult healthcare professionals for proper medical advice.

## 🔧 Technical Details

- **Backend**: Python with Groq's Vision Language Model
- **Frontend**: Streamlit
- **Image Processing**: PIL (Python Imaging Library)
- **Model**: llama-3.2-90b-vision-preview

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Talal Muzaffar - [GitHub](https://github.com/talalmuzaffar)

Project Link: [https://github.com/talalmuzaffar/Eye-Diseases-Classification-using-VLM](https://github.com/talalmuzaffar/Eye-Diseases-Classification-using-VLM) 
