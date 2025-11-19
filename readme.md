# N.O.V.A - Neural Optimized Virtual Assistant

A Python-based voice-controlled AI assistant that can perform various tasks including opening applications, playing YouTube videos, web browsing, and engaging in conversations using AI language models.

## Features

- 🎤 **Voice Recognition**: Hands-free control using wake words
- 🗣️ **Text-to-Speech**: Natural voice responses
- 🌐 **Web Browsing**: Open websites with voice commands
- 🎵 **YouTube Integration**: Search and play videos automatically
- 💻 **Application Control**: Open and close applications
- 🤖 **AI Conversations**: Powered by OpenRouter API with Mistral model
- 🔌 **System Control**: Shutdown PC and manage processes

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)
- Microphone for voice input
- OpenRouter API key

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/amanjaiswal1818/NOVA.git
cd nova-assistant
```

2. **Install required Python packages**
```bash
pip install speechrecognition pyttsx3 selenium requests pyaudio
```

3. **Download ChromeDriver**
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
   - Download the version matching your Chrome browser
   - Extract to `C:\chromedriver\` (or update the path in the code)

4. **Get OpenRouter API Key**
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Generate an API key
   - Replace `sk-or-your-api-key-here` in the code

## Configuration

Update the following variables in the code:

```python
OPENROUTER_API_KEY = "your-actual-api-key"
CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"
CHROME_PROFILE_PATH = r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data\Profile X"
```

### Finding Your Chrome Profile Path
1. Open Chrome and navigate to `chrome://version/`
2. Copy the "Profile Path" value
3. Update `CHROME_PROFILE_PATH` in the code

## Usage

1. **Start the assistant**
```bash
python nova.py
```

2. **Wake words**: Use any of these to activate N.O.V.A
   - "Nova"
   - "Hey Nova"
   - "OK Nova"

3. **Example commands**:
   - `"Nova, open YouTube"`
   - `"Hey Nova, play Bohemian Rhapsody"`
   - `"OK Nova, open Chrome"`
   - `"Nova, close Notepad"`
   - `"Nova, what's the weather like today?"`
   - `"Nova, shutdown"`

## Supported Commands

### Opening Applications
```
"open [app name]"
```
Supported apps: Chrome, Brave, Calculator, Notepad, Paint, File Explorer, Command Prompt, Task Manager, VLC, Spotify, Camera

### Closing Applications
```
"close [app name]"
```

### Playing YouTube Videos
```
"play [song/video name]"
```

### Opening Websites
```
"open [website.com]"
```

### AI Conversations
Ask any question and N.O.V.A will respond using the AI model

### System Control
```
"shutdown" - Immediately shuts down the PC
```

## Customization

### Adding Custom Applications

Edit the `common_apps` dictionary in the `open_app()` function:

```python
common_apps = {
    "your app": r"C:\Path\To\Your\Application.exe",
}
```

### Changing Voice Properties

Modify the speech engine settings:

```python
engine.setProperty('rate', 160)  # Speech speed
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
```

### Adjusting AI Response

Modify the OpenRouter API parameters:

```python
data = {
    "model": "mistral",  # Change model
    "temperature": 0.7,   # Creativity (0.0 to 1.0)
    "max_tokens": 200,    # Response length
}
```

## Troubleshooting

**Speech recognition not working?**
- Check microphone permissions
- Ensure stable internet connection (uses Google Speech Recognition)

**ChromeDriver errors?**
- Verify ChromeDriver version matches Chrome browser version
- Check if path is correct

**Can't open applications?**
- Verify application paths in `common_apps` dictionary
- Run as administrator if needed

**API errors?**
- Verify OpenRouter API key is valid
- Check internet connection

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data
- Be cautious with the shutdown command

## Future Enhancements

- [ ] Add email integration
- [ ] Calendar and reminder features
- [ ] Smart home device control
- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Context-aware conversations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Acknowledgments

- [OpenRouter](https://openrouter.ai/) for AI model access
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) library
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for text-to-speech
- [Selenium](https://www.selenium.dev/) for browser automation

## Contact

For questions or support, please open an issue on GitHub.

---


**⚠️ Warning**: The shutdown command will immediately turn off your computer. Use with caution!

