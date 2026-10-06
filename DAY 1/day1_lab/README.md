# Day 1 - Agentic AI Foundations

## Project Overview

This project demonstrates three approaches to solving a college fee-related problem:

1. Plain Chatbot
2. Rule-Based Workflow
3. AI Agent

The AI Agent uses:

**LLM + Tools + Loop**

## Systems

### 1. Plain Chatbot

The chatbot directly uses the language model to answer user questions.

It does not use external tools or private data.

### 2. Rule-Based Workflow

The workflow follows predefined rules and conditions.

It uses the private course fee data directly without making decisions using an LLM.

### 3. AI Agent

The AI Agent combines:

- Large Language Model
- Tools
- Reasoning
- Tool selection
- Observation
- Multi-step loop

Available tools:

- `get_course_fee`
- `calculator`

## Example

User:

```text
What is the fee for AI202?