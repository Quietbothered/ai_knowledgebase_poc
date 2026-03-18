# Project Direction — Internal Knowledge Assistant

## Context
Organizations accumulate knowledge across multiple platforms such as:
- Microsoft Teams (chat, discussions)
- Microsoft SharePoint (documents, files)
- Jira (tickets, workflows)

This knowledge is often fragmented and hard to access, especially for new team members.

## Problem
- Knowledge is siloed across tools
- New joiners depend on senior engineers/managers
- Repeated questions reduce team productivity
- No unified search or reasoning layer

## Goal
Build a RAG-based assistant that:
- Answers questions about internal systems
- Retrieves accurate information from multiple sources
- Provides citations and traceability
- Reduces dependency on human knowledge holders

## Key Capabilities
- Natural language querying
- Source-backed answers
- Cross-system knowledge retrieval
- Context-aware follow-up questions

## Supported Data Sources
- Microsoft Teams
- Microsoft SharePoint
- Jira
- (Future: GitHub, Confluence, Email) Don't implement now

## Success Criteria
- Reduced onboarding time
- Fewer repetitive questions to senior engineers
- High answer accuracy with citations