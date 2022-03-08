call C:\DevelopmentTools\Miniconda3\miniconda3\Scripts\activate.bat C:\DevelopmentTools\Miniconda3\miniconda3\envs\bysj
pyrcc5 apprcc.qrc -o apprcc_rc.py
python -m PyQt5.uic.pyuic ui/main.ui -o ui/main.py
python -m PyQt5.uic.pyuic ui/sound_recording_frame.ui -o ui/sound_recording_frame.py
python -m PyQt5.uic.pyuic ui/help_frame.ui -o ui/help_frame.py
python -m PyQt5.uic.pyuic ui/about_frame.ui -o ui/about_frame.py