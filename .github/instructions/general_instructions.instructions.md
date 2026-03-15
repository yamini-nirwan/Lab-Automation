---
description: Describe when these instructions should be loaded by the agent based on task context
# applyTo: 'Describe when these instructions should be loaded by the agent based on task context' # when provided, instructions will automatically be added to the request context when the pattern matches an attached file
---

<!-- Tip: Use /create-instructions in chat to generate content with agent assistance -->

Python Coding Guidelines for Lab Automation Project

When generating, modifying, or reviewing Python code in this lab automation project, follow these guidelines:

- **Explain with Comments**: Always include clear, beginner-friendly comments explaining what each section of code does, why it's needed, and how it works. Use simple language to help newcomers understand complex concepts.

- **Meaningful Variables**: Use descriptive variable names that clearly indicate their purpose (e.g., `experiment_yield` instead of `y`). Avoid single-letter names except for common loop variables like `i`.

- **Python Best Practices**: Adhere to PEP 8 style guidelines, use list comprehensions where appropriate, handle exceptions properly, and prefer readable, maintainable code over clever shortcuts. Ensure code is modular and reusable.

- **Project Context**: This is a lab automation system for electrochemical reactions. Code should focus on experiment simulation, data logging, optimization, and analysis. Prioritize accuracy, reproducibility, and ease of modification for research purposes.