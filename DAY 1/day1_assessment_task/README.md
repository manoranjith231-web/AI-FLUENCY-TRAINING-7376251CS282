# Agentic AI Day 1
## Foundations of AI Agents - Agent = LLM + Tools + Loop

This project compares three approaches for solving the same private-data
problem:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent

## Scenario

The scenario is a Private Student Academic Assistant.

The system contains synthetic student information including:

- Student details
- Subject marks
- Attendance
- Assignment status

## Architecture

### Plain Chatbot

```text
User
 ↓
Chatbot / LLM
 ↓
Response