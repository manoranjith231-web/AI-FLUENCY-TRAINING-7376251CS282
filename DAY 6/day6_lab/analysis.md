# Day 6 Analysis – Robust Agents and Structured Outputs

## 1. Objective

The objective of Day 6 is to improve the reliability and safety of an AI agent.

A normal AI agent can generate tool calls, but the generated arguments may be invalid, incomplete, or unsafe. Therefore, the application should validate every tool call before executing it.

In this task, the college fee assistant was improved using:

- Groq API
- Tool calling
- JSON Schema validation
- Argument validation
- Error handling
- Safe calculator execution
- Retry and loop protection
- Structured JSON outputs
- Fault injection testing

---

## 2. Basic Agent vs Robust Agent

### Basic Agent

A basic tool-using agent follows:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Answer