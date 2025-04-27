# MCP Server Implementation Specification

## Overview

This document provides guidelines for implementing an MCP (Model Context Protocol) server using Python. The MCP server acts as an intermediary between AI assistants and application-specific functionality, providing tools, resources, and APIs that enable AI models to perform domain-specific tasks.

## Core Components

### 1. MCP Server

The MCP server is the central component that handles requests from AI assistants and provides a structured interface for tool and resource definitions.

```python
from mcp.server.fastmcp import FastMCP

# Setup MCP
mcp = FastMCP("My Application", dependencies=["pydantic", "rich"])

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### 2. Tools

Tools are functions that can be called by AI assistants to perform specific actions. Each tool is annotated with metadata describing its purpose and parameters.

```python
from typing import Annotated
from pydantic import Field

@mcp.tool()
def create_item_tool(
    name: Annotated[str, Field(description="The name of the item to create")],
    description: Annotated[str, Field(description="A detailed description of the item")]
) -> Item:
    """
    Create a new item.
    """
    return create_item(name, description)

@mcp.tool()
def update_item_tool(
    item_id: Annotated[int, Field(description="The ID of the item to update")],
    name: Annotated[str, Field(description="The new name for the item")],
    description: Annotated[str, Field(description="The new description for the item")]
) -> Item:
    """
    Update an existing item.
    """
    return update_item(item_id, name, description)

@mcp.tool()
def delete_item_tool(
    item_id: Annotated[int, Field(description="The ID of the item to delete")]
) -> bool:
    """
    Delete an item.
    
    Warning: This will permanently delete the item and all associated data.
    """
    return delete_item(item_id)

@mcp.tool()
def search_items_tool(
    query: Annotated[str, Field(description="Search term to look for in item names and descriptions")]
) -> list[Item]:
    """
    Search items by name or description.
    """
    return search_items(query)
```

### 3. Resources

Resources are endpoints that provide data to AI assistants but don't modify system state. They are useful for retrieving information that might be referenced in conversations.

```python
@mcp.resource("item://{item_id}")
def get_item_resource(item_id: int) -> Item:
    """
    Get item details.
    """
    return get_item(item_id)

@mcp.resource("item://list")
def list_items_resource() -> list[Item]:
    """
    List all items.
    """
    return list_items()
```

### 4. Models

Models define the data structures used by your application. These should be defined using Pydantic for type safety and validation.

```python
from pydantic import BaseModel
from typing import Dict, Optional

class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    data: Dict
    created_at: str
    updated_at: str
```

## Implementation Guidelines

### Project Structure

```
project_root/
├── src/
│   ├── __init__.py
│   ├── main.py             # Main MCP server entry point
│   ├── models/             # Pydantic models
│   │   ├── __init__.py
│   │   └── item.py         # Example model
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── helpers.py      # Helper functions
├── tests/
│   ├── __init__.py
│   ├── environment.py      # Behave test environment setup
│   ├── features/           # BDD feature files
│   │   └── item_management.feature
│   └── steps/              # BDD step implementations
│       ├── __init__.py
│       └── item_steps.py
├── Makefile                # Project automation
└── requirements.txt        # Project dependencies
```

### Dependencies

```
mcp>=1.2.1
pydantic>=1.10.2
rich>=12.6.0
behave>=1.2.6  # For testing
```

### Parameter Annotations

Use Pydantic's Field and typing.Annotated to provide rich metadata about your tool parameters:

```python
from typing import Annotated, List, Dict, Optional
from pydantic import Field

def my_tool(
    required_param: Annotated[str, Field(description="This parameter is required")],
    optional_param: Annotated[str | None, Field(description="This parameter is optional")] = None,
    list_param: Annotated[List[str] | None, Field(description="This accepts a list of strings")] = None,
    dict_param: Annotated[Dict | None, Field(description="This accepts a dictionary")] = None,
    int_param: Annotated[int, Field(description="This accepts an integer")] = 0
):
    # Implementation
    pass
```

### Documentation

Provide clear documentation for each tool and resource:

1. Include a docstring describing the purpose
2. Document parameters with Field annotations
3. Specify return types
4. Include warnings for destructive operations

## Testing Strategy

### BDD Testing with Behave

Behavior-Driven Development (BDD) using Behave allows you to write human-readable tests that verify your MCP server's functionality.

Example feature file (tests/features/item_management.feature):

```gherkin
Feature: Item Management
  As a user
  I want to manage items
  So that I can organize my data

  Scenario: Create a new item
    Given there are no items
    When I create an item with the following details:
      | name        | description           |
      | Example     | This is an example    |
    Then the item "Example" should be created successfully
    And the item "Example" should have description "This is an example"
```

Example steps implementation (tests/steps/item_steps.py):

```python
from behave import given, when, then
from src.main import (
    create_item_tool,
    search_items_tool,
    get_item_resource
)

@given('there are no items')
def step_impl_no_items(context):
    # Clear the items (implementation depends on your app)
    pass

@when('I create an item with the following details')
def step_impl_create_item_details(context):
    table = context.table
    for row in table:
        name = row['name']
        description = row['description']
        item = create_item_tool(name=name, description=description)
        context.created_item = item

@then('the item "{name}" should be created successfully')
def step_impl_item_created(context, name):
    # Search for item by name
    items = search_items_tool(query=name)
    item = next((i for i in items if i.name == name), None)
    assert item is not None
    item = get_item_resource(item_id=item.id)
    assert item.name == name
```

### Test Environment Setup

Create a test environment in tests/environment.py:

```python
def before_all(context):
    """Set up test environment before running tests"""
    # Setup test environment here
    # This could include setting up a test database, initializing your MCP server, etc.
    pass
```

## Example Makefile Commands

```makefile
.PHONY: setup install run test test-scenario

# Install project dependencies
install:
	pip install -r requirements.txt

# Run the MCP server
run:
	python src/main.py

# Run BDD tests using Behave
test:
	PYTHONPATH=src behave tests/features --no-capture --format pretty

# Run a specific scenario
test-scenario:
	PYTHONPATH=src behave tests/features/$(FEATURE).feature --name "$(SCENARIO)"

# Setup virtual environment
setup-venv:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && $(MAKE) install
```

## Implementing Complex Tools

For tools with complex logic or many parameters, follow these guidelines:

1. Group related parameters
2. Provide reasonable defaults
3. Use clear, descriptive parameter names
4. Handle and validate inputs before processing
5. Return structured responses (using Pydantic models)

## Best Practices

1. **Input Validation**: Always validate inputs before processing them
2. **Error Handling**: Provide clear error messages when operations fail
3. **Documentation**: Document tools and resources thoroughly
4. **Naming Conventions**: Use consistent naming patterns (e.g., `*_tool` for tools, `*_resource` for resources)
5. **Testing**: Write comprehensive tests for all tools and resources
6. **Type Hints**: Use type hints throughout your code for better IDE support and documentation

## Advanced Features

### Optional Parameters

For tools that have many parameters where most are optional:

```python
@mcp.tool()
def advanced_search_tool(
    query: Annotated[str | None, Field(description="Main search term")] = None,
    category: Annotated[str | None, Field(description="Filter by category")] = None,
    min_value: Annotated[int | None, Field(description="Minimum value")] = None,
    max_value: Annotated[int | None, Field(description="Maximum value")] = None,
    sort_by: Annotated[str | None, Field(description="Field to sort by")] = None,
    sort_order: Annotated[str | None, Field(description="Sort order (asc/desc)")] = "asc"
) -> Dict:
    """
    Advanced search with multiple optional filters.
    """
    # Build search parameters from non-None values
    search_params = {k: v for k, v in locals().items() if k != 'self' and v is not None}
    return perform_search(**search_params)
```

### Command Line Arguments

Use argparse to handle command-line arguments:

```python
import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="MCP Server Application")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--log-level", default="info", help="Logging level")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Configure logging based on args.log_level
    
    # Run the MCP application
    mcp.run(port=args.port)
```

## Conclusion

This specification provides a framework for building an MCP server that can be used by AI assistants to interact with your application. By following these guidelines, you can create a well-structured, testable, and maintainable MCP server that enables AI assistants to perform complex domain-specific tasks. 