# Interactive Systems Project 2 - Text-Based Adventure Game

## Team Members
- Rafael Hermida Toloedo
- Sebastian Castro Obando

## Project Description

This project is a text-based adventure game inspired by classic interactive fiction like Zork. The game creates an immersive audio experience using OpenAL for 3D spatial sound positioning.

### Story Overview
Our approach focused on creating a suspense story where the protagonist must discover who murdered their parents. The player navigates through different locations, gathering clues and interacting with the environment to solve the mystery. The narrative follows a complete story structure with beginning, development, climax, and resolution.

### Key Features
- **3D Spatial Audio**: Sounds are positioned in 3D space according to the story events (left, right, behind, distant, etc.)
- **Interactive Storyline**: Players can progress through the story line by line using command-line interface
- **Immersive Sound Design**: Each story line includes appropriate sound effects or music that match the narrative
- **Mystery Genre**: A complete suspense story with investigation elements
- **Command-Line Interface**: Simple text-based interaction system

## Technical Implementation

### Technologies Used
- **Programming Language**: [Specify: Python]
- **Audio Library**: OpenAL for 3D spatial audio processing
- **Architecture**: Object-Oriented Programming principles

### Audio System
The game implements spatial audio where:
- Sounds from the right appear in the right speaker
- Distant sounds have appropriate volume and reverb
- Sounds from behind use rear positioning
- Each story line has corresponding positioned audio

### Story Structure
- **Total Lines**: 50+ lines of narrative text
- **Complete Story Arc**: Beginning → Investigation → Discovery → Resolution
- **Interactive Elements**: Player can progress through the story at their own pace

## Installation & Setup

### 1. Create and activate the virtual environment

On Windows, run the following command in the project folder:

```
.\setup_env.bat
```

This will create a virtual environment, activate it, and install all required dependencies from `requirements.txt`.

If you want to activate the environment later, use:

```
call venv\Scripts\activate
```

### 2. Run the game

Once the environment is activated, start the game with:

```
python main.py
```

The game runs in the console and uses spatial audio. Make sure your sound output is configured correctly for the best experience.

## Audio Resources
All audio resources used in this project were extracted from YouTube and have been edited to fit the game's requirements. The sounds include ambient effects, music, and sound effects that enhance the suspense atmosphere of the story.

## Design Decisions

### Why This Approach?
We chose a murder mystery theme because:
1. **Engagement**: Mystery stories naturally keep players interested in progressing
2. **Audio Opportunities**: Investigation scenarios provide many opportunities for spatial audio (footsteps, doors, environmental sounds)
3. **Narrative Structure**: Mystery format naturally provides a clear beginning, development, and resolution
4. **Immersion**: The suspense genre benefits greatly from atmospheric audio design

### Object-Oriented Design
The code follows OOP principles with clear separation of concerns:
- Story management classes
- Audio system classes  
- Player interaction handlers
- Game state management

## Project Structure
```
PROJECT2_-_Interactive_Systems/
├── sounds/                # Audio files and sound effects
├── src/                   # Source code directory
│   ├── pycache/          # Python cache files
│   ├── game.py           # Main game logic
│   ├── sound_manager.py  # Audio and spatial sound management
│   └── story.py          # Story content and narrative handling
├── venv/                 # Virtual environment
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── test_spatial.py       # Spatial audio testing
```

## Requirements Compliance
- ✅ Uses OpenAL library for spatial audio
- ✅ Text-based interface with line-by-line story progression
- ✅ 50+ lines of complete story
- ✅ 3D positioned audio for each story element
- ✅ Object-oriented programming implementation
- ✅ Playable for 5+ minutes
- ✅ Command-line interface
