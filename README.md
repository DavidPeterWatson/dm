# D&D Game Master Assistant MCP Server

## Overview

The D&D Game Master Assistant MCP server assists Claude in running Dungeons & Dragons games by providing tools for managing campaign information, storing game data, and retrieving relevant information during gameplay sessions.

## Features

- **Campaign Management**: Create, update, delete, and search campaigns.
- **Character Management**: Manage player and NPC characters.
- **Location Management**: Organize and retrieve game locations.
- **Item Management**: Handle in-game items and equipment.
- **Database Integration**: Uses SQLite for local storage.
- **BDD Testing**: Ensures functionality through Behave tests.

## Technology Stack

- **Language**: Python 3.10+
- **MCP Implementation**: MCP Python SDK
- **Database**: SQLite
- **Testing**: Behave
- **Libraries**:
  - `pydantic`
  - `sqlite-utils`
  - `rich`

## Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/dnd-gm-assistant.git
    cd dnd-gm-assistant
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Initialize the Database**
    ```bash
    python src/database/schema.py
    ```

4. **Run the MCP Server**
    ```bash
    python src/dm.py
    ```

## Testing

Run BDD tests using Behave:
```bash
behave
```

## Contributing

Contributions are welcome! Please see the [Contributing Guide](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. 