Create virtual environment:
python3 -m venv venv

Activate it:
source venv/bin/activate 
-> Under Windows: 
.\venv\Scripts\activate

Install packages:
pip install -r requirements.txt

Add a config.json file. Copy this code into the file and replace the X's for the API keys:
{
  "api_key": "XXX",
  "elevenLabs_key": "XXX"
}

Auf mac falls ffmpeg nicht gefunden werden kann:
brew install ffmpeg

Für streaming auf mac wird mpv benötigt:
brew install mpv

