# Google Antigravity (AGY) Master Training Guide & Tutorials

Welcome to the Google Antigravity (AGY) user training system. This guide provides
a structured walkthrough, checklists, and references to get up-to-speed with
the AI-first developer suite.

---

## 1. Introduction

Google Antigravity is a suite of AI-first development tools designed to augment
software engineering with high-autonomy agents. Antigravity can operate as:
- A command-line TUI (`agy` CLI)
- A standalone desktop controller (Antigravity 2.0)
- IDE extensions (Antigravity Tab, inline Ctrl+I, Sidebar Agent)
- An automation Python SDK

---

## 2. Antigravity CLI (`agy`)

The `agy` CLI is a terminal-based interface designed for quick queries and
headless task runs.

### Basic CLI Operations
- **Launch CLI**: Type `agy` in your terminal to start the TUI mode.
- **Get Help**:
  - Shell command-line: `agy --help`
  - Inside CLI session: `/help`
- **Settings File**: Global behavior is customized via the JSON file at:
  `~/.gemini/antigravity-cli/settings.json`
- **Exit Session**: Type `/exit`, `/quit`, or press `Ctrl+D` twice.

### TUI Slash Commands Reference
- `/goal`: Command the agent to execute a long-running, recursive task.
- `/plan`: Request a step-by-step layout of an action before running.
- `/grill-me`: Launch an interactive interview to clarify design choices.
- `/schedule`: Set up recurring cron operations or timers.
- `/teamwork-preview`: Launch multiple specialized subagents concurrently.

---

## 3. Antigravity IDE (VS Code Integration)

The IDE integrations bake agentic workflow loops directly into your editor.

### The Three Modalities of Interaction
1. **Passive (Antigravity Tab Autocomplete)**:
   Predicts next-intent actions at a single keystroke.
   - **Controls**: Accept suggestion with `Tab`. Reject/close with `Esc`.
     Accept word-by-word with `Ctrl+RightArrow` (Linux) / `Cmd+RightArrow` (Mac).
   - **Capabilities**: Auto-imports missing packages; jumps to next cursor locations.
2. **Instructive (Inline Command Ctrl+I / Cmd+I)**:
   - Highlight any block of code and press `Ctrl+I` to refactor, write docstrings,
     or ask questions about that localized region.
   - Run without a selection to generate fresh code at the cursor.
3. **Collaborative (Sidebar Chat & Agent Mode)**:
   - Launch an interactive developer workspace-agent in the sidebar panel.
   - Review file edit plans and approve sandboxed terminal operations.

---

## 4. Antigravity 2.0 (Electron Desktop App)

Antigravity 2.0 is the parallel desktop application that manages agents and
system integrations independently of your IDE.

### UI Panels
- **Left Sidebar**: Start new chat threads, manage project lists, monitor cron
  schedules, configure global preferences, and customize active skills.
- **Chat Canvas**: The main interface supporting `@-mentions` (context attachment
  for files, logs, rules) and drag-and-drop media uploads.
- **Auxiliary Pane**: Displays running subagent tasks, background commands, and
  file diffs.

### Agent Permissions & Security Policy Gates
Configure these in the project/global Settings sidebar:
- **Sandbox Mode**: Enforces sandboxed commands to prevent system pollution.
- **File Access**: Choose `allow`, `ask`, or `deny` for non-workspace directories.
- **Internet Access**: Enable or restrict external HTTP requests.
- **Allowlist/Denylist**: Hardcode commands or web domains the agent can run.

---

## 5. Python SDK

For programmatic pipelines, the `google-antigravity` package enables leasing
and controlling agents via code.

### Installation
```sh
pip install google-antigravity
```

### Python Lifecycle Quickstart
```python
import asyncio
import sys
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

async def main():
    # Lease agent with command/write capabilities
    config = LocalAgentConfig(
        system_instructions="You are an expert compiler auditor.",
        capabilities=CapabilitiesConfig()
    )

    async with Agent(config) as agent:
        response = await agent.chat("Check build logs for warning traces.")
        async for token in response:
            sys.stdout.write(token)
            sys.stdout.flush()
        print()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. Onboarding Checklist

Use this checklist when setting up a workspace for Antigravity-assisted work:
- [ ] Install `google-antigravity` client or CLI binary.
- [ ] Run `agy` to verify authentication setup.
- [ ] Audit `~/.gemini/antigravity-cli/settings.json` for proper default models.
- [ ] Bind IDE shortcut keys for `Ctrl+I` inline edit prompts.
- [ ] Verify that the workspace root contains `.github/copilot-instructions.md`
      to enforce repo standards.
- [ ] Read the local guides in the `users/` directory.

---

# EOF: users/antigravity_guide.md
