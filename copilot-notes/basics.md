# GitHub Copilot in VS Code: Basics & Customization

These notes cover the essentials of using GitHub Copilot in VS Code as of late 2024 / early 2025.

## 1. Copilot Instructions

You can customize how Copilot applies to your specific project by using instruction files. This prevents you from having to repeat the same context (like "use Python 3.12" or "prefer functional style") in every query.

### Repository-level Instructions
Create a file named `.github/copilot-instructions.md` in your project root. Copilot will read this file at the start of every chat session.

**Example Content:**
```markdown
- We are using Python 3.13.
- Use type hints for all function arguments: `def my_func(a: int) -> str:`.
- Prefer `pytest` over `unittest`.
- Always respond in Spanish.
```

### Folder-Specific Instructions
You can also place instruction files in specific directories (often named `AGENTS.md` or similar, though convention varies) to guide the agent when working in that folder.

*See more: [Adding repository custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)*

## 2. Agents (Participants)

In VS Code, Copilot is not just a single chatbot. It uses "Agents" (or Participants) specialized for different tasks. You invoke them using the `@` symbol.

### Built-in Agents
- **`@workspace`**: The project expert. It indexes your files and understands your folder structure.
  - *Use for:* "Where is the authentication logic?" or "Refactor this class to use the Singleton pattern."
- **`@vscode`**: The editor expert. It knows VS Code commands and settings.
  - *Use for:* "Change the theme to Dark Mode" or "How do I debug a Python file?"
- **`@terminal`**: (If available) Contextual help regarding the integrated terminal.

### Custom Agents (Extensions)
You can install **Copilot Extensions** from the VS Code Marketplace. These add new `@` agents that connect to external services.
- **`@azure`**: Manage Azure resources.
- **`@github`**: Search issues, pull requests, and repo metadata.
- **`@docker`**: Manage containers and images.

## 3. Tools and Capabilities

Agents use "Tools" to perform actions. You can also manually reference context variables using the `#` symbol.

| Symbol | Name | Description |
| :--- | :--- | :--- |
| **`#file`** | File Context | Explicitly add a file to the chat context. |
| **`#codebase`** | Codebase | Force a search across the entire workspace. |
| **`#editor`** | Editor View | The currently visible code in your active editor. |
| **`#terminalSelection`**| Terminal | The text currently selected in your terminal. |

**Key Capabilities:**
- **Code Editing:** Copilot can propose changes that you apply directly with a "Apply in Editor" button.
- **Terminal Commands:** Copilot can generate shell commands for you to run (e.g., install packages, git operations).

---
*Reference: [VS Code Copilot Documentation](https://code.visualstudio.com/docs/copilot/overview)*
