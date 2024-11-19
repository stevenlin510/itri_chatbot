# LLM-Vis3D

## What is LLM-Vis3D?

LLM-Vis3D is a system that drives 3D high-fidelity virtual human interaction using a large language model as the backend. Users can interact with the virtual human through microphone, achieving easy use of LLM tools and customization of personal responses.

## System Requirements and Software Dependencies

+ OS: Windows 10/11
+ GPU: Nvidia consumer-grade gaming graphics card( recommend RTX-3070 or higher)
+ API Key:
  + OpenAI(LLM)
  + Qdrant(vector database)
  + Google-serper(search engine)
  + Azure Speech(text-to-speech)
+ Unreal Engine 5.1
+ Plugins in Unreal Engine
  + OSC(Open Sound Control)
  + Pixel Streaming
  + Pixel Streaming Player

## Installation Guide

1. Install **Miniconda**

    [installation guide for miniconda](https://docs.anaconda.com/free/miniconda/index.html)

2. Install **Visual Studio Code**

    [installation guide for VS Code](https://medium.com/nerd-for-tech/install-visual-studio-code-fe3908c5cf15)

3. Install and setup windows environment variables for **FFmpeg**

    [installation and setup guide for FFmped (in Mandarin Chinese)](https://vocus.cc/article/64701a2cfd897800014daed0)

4. Install 7-Zip(Optional if you don't have other unzip app)

    [installation guide for 7-Zip](https://7ziphelp.com/how-to-use-7-zip)

5. Restart Windows(Optional)
6. Install [Omniverse Launcher](https://www.nvidia.com/en-us/omniverse/download/)
7. Setup Audio2Face
   + setup Audio2face app, server, and blend shape
   + launch Omniverse Launcher to install Audio2Face
   + setup a local server
   + launch the Audio2Face app and begin setting up
   + launch the Audio2Face app and create a new usd file

   Step by step setup guide with pictures see  [Setup Audio2Face](./Setup%20Audio2Face.md).
8. Open anaconda prompt and run the following command step-by-step to create virtual envirement

        cd the/path/of/the/folder/Final2023

        conda env create -n bot -f environment.yml
        
        pip install protobuf==3.20.0

    *Note: You could modify the virtual envirement name in the top-line of the file environment.yml(default to bot)*

## Usage

There are two steps to run the LLM-Vis3D system

1. Start audio2face OSC server

        ./audio2face/audio2face_headless.kit.bat - 捷徑

2. Run the program in anaconda prompt with created virtual envirement

        python main.py

    or double-click the file

        start.bat

    *Note: the path in the **start.bat** should be modified before running.*
