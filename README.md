# OpenAI Prompt Improver

A Python tool that refines raw software development prompts using OpenAI's GPT models to make them more effective and detailed.

## Features

- **Prompt Enhancement**: Transforms vague or incomplete prompts into detailed, actionable requests
- **Multiple Input Methods**: Accept prompts via command line arguments, stdin, or file redirection
- **Silent Mode**: Clean output for piping to other tools
- **Configurable**: Easy to modify the AI model and system instructions

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd openai-prompt-improver
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Basic Usage

```bash
# Command line argument
uv run prompt-enhance.py "Need help sorting a list faster in JS"

# From stdin
echo "Need help sorting a list faster in JS" | uv run prompt-enhance.py

# From file
cat myprompt.txt | uv run prompt-enhance.py

# Silent mode (no spinner)
uv run prompt-enhance.py -s "Need help sorting a list faster in JS" > output.txt
```

### Actual Usage

I alias `enhance-prompt` to

```bash
uv run ~/<path-to-project>/prompt-enhance.py $@
```

### Examples

**Input**: `enhance-prompt "a webapp that mimics instagram built in svelte v5"`

**Output**: A detailed, structured prompt that includes:

- Specific requirements and constraints
- Expected input/output format
- Performance considerations
- Code examples or pseudocode

````bash
### Polished Prompt
Develop a Svelte 5 web application that replicates core features of Instagram, focusing on:

1. User functionality including account creation, login, and profile management.
2. Image posting, editing, and deleting capabilities, with support for captions and hashtags.
3. Responsive design to support various device sizes.
4. Privacy settings allowing users to control who can view their posts.
5. Notifications for likes and comments on posts.
6. A simple feed flow where users can view posts from other users they follow.

Ensure the application adheres to best practices for Svelte development, including use of stores for state management, and comprehensive error handling.

### Technical Details

- Use Svelte v5 for frontend development ensuring a reactive and scalable design pattern.
- Implement user authentication and authorization mechanisms, possibly using JWTs.
- Ensure responsive design using CSS flexbox/grid and media queries.
- Employ Svelte stores for managing application state, especially for user data and posts.
- Follow modular design principles for code organization within Svelte.
- Implement basic backend services for user and post CRUD operations, possibly using a RESTful or GraphQL API.
- Include unit tests for critical functionalities and components.

### Architecture

- **Folder Structure:**
/```
  /src
    /components
      - Header.svelte
      - Footer.svelte
      - Post.svelte
      - Profile.svelte
      ...
    /stores
      - userStore.js
      - postStore.js
    /pages
      - Home.svelte
      - Login.svelte
      - Signup.svelte
      ...
  /public
    - styles.css
/  ```

- **Components and Pages:**
  - `Header.svelte` and `Footer.svelte`: UI components for navigational elements.
  - `Post.svelte`: Manages display and interactions for a single post.
  - `Profile.svelte`: Displays user profile information, including posts and settings.
  - `Home.svelte`, `Login.svelte`, `Signup.svelte`: Main pages handling routing and layout.

- **State Management:**
  - State lives in dedicated Svelte stores (`userStore.js`, `postStore.js`) to manage user session data and posts.

- **Backend Services:**
  - Suggested to implement RESTful or GraphQL API endpoints for user and post interactions, using Node.js/Express or an equivalent backend framework.

- **Integration:**
  - Authenticated routes handle user sessions, enforce access controls, and manage lifecycle events across the application.

````

## Configuration

- **Model**: Change `MODEL` in `prompt-enhance.py` to use different OpenAI models
- **System Instructions**: Modify `instructions.md` to customize the enhancement behavior
- **Timeout**: Adjust `TIMEOUT` for different response times

## Architecture

The tool uses a system prompt (defined in `instructions.md`) to guide the AI in transforming raw prompts into well-structured, detailed requests suitable for software development tasks.

## License

MIT
