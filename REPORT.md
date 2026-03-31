# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
🐈 nanobot
The agentic loop is the core iterative execution cycle that powers autonomous AI agents. Here's how it works:                                                                    

The Agentic Loop Cycle                                                                                                                                                           

 1 Perceive — The agent gathers context from its environment, inputs, and memory                                                                                                 
 2 Reason — The LLM analyzes the context and determines what action to take next                                                                                                 
 3 Act — The agent executes the chosen action (calls tools, APIs, makes changes, etc.)                                                                                           
 4 Observe — The agent captures the outcome/result of the action                                                                                                                 
 5 Loop — The observation feeds back into the next iteration, and the cycle continues                                                                                            

Key Characteristics                                                                                                                                                              

 • Autonomous: Unlike traditional AI that produces single reactive outputs, agentic AI operates in a continuous loop                                                             
 • Goal-driven: The loop continues until the agent achieves its objective or reaches a stopping condition                                                                        
 • Adaptive: Each iteration learns from feedback and adjusts the next action accordingly                                                                                         
 • Tool-enabled: Agents can access external tools, APIs, databases, and other resources during execution                                                                         

Why It Matters                                                                                                                                                                   

This loop architecture (sometimes called "the billion-dollar while loop") is what enables AI agents to:                                                                          

 • Plan multi-step tasks                                                                                                                                                         
 • Self-correct when errors occur                                                                                                                                                
 • Collaborate with other agents or humans                                                                                                                                       
 • Operate safely in production environments                                                                                                                                     

In essence, the agentic loop transforms an LLM from a passive text generator into an active, goal-oriented system that can perceive, reason, act, and learn continuously. 
## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->
🐈 nanobot
Here are the available labs in the LMS:                                                                                                                                          

                                                             
 ID  Title                                                   
 ─────────────────────────────────────────────────────────── 
 1   Lab 01 – Products, Architecture & Roles                 
 2   Lab 02 — Run, Fix, and Deploy a Backend Service         
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy 
 4   Lab 04 — Testing, Front-end, and AI Agents              
 5   Lab 05 — Data Pipeline and Analytics Dashboard          
 6   Lab 06 — Build Your Own Agent                           
 7   Lab 07 — Build a Client with an AI Coding Agent         
 8   lab-08                                                  
                                                             

Would you like more details about any specific lab, such as pass rates, completion rates, or top learners?

🐈 nanobot
Based on the documentation and configuration files, here's the LMS (Learning Management System) architecture:                                                                    

LMS System Architecture                                                                                                                                                          

Overview                                                                                                                                                                         

The LMS is a full-stack web application that provides a learning analytics dashboard. It's built with modern technologies and deployed using Docker Compose.                     

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Core Components                                                                                                                                                                  

                                                                                                                                                                                 
 ┌─────────────────────────────────────────────────────────────────┐                                                                                                             
 │                         Client Layer                            │                                                                                                             
 │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │                                                                                                              
 │  │   React     │  │   Flutter    │  │   Telegram Bot       │   │                                                                                                              
 │  │   Frontend  │  │   Frontend   │  │   (optional)         │   │                                                                                                              
 │  └──────┬──────┘  └──────┬───────┘  └──────────┬───────────┘   │                                                                                                              
 └─────────┼────────────────┼─────────────────────┼────────────────┘                                                                                                             
           │                │                     │                                                                                                                              
           ▼                ▼                     ▼                                                                                                                              
 ┌─────────────────────────────────────────────────────────────────┐                                                                                                             
 │                      Gateway Layer                              │                                                                                                             
 │  ┌──────────────────────────────────────────────────────────┐   │                                                                                                             
 │  │                      Caddy                               │   │                                                                                                             
 │  │              (Reverse Proxy / API Gateway)               │   │                                                                                                             
 │  └──────────────────────────────────────────────────────────┘   │                                                                                                             
 └─────────────────────────────────────────────────────────────────┘                                                                                                             
           │                                                                                                                                                                     
           ▼                                                                                                                                                                     
 ┌─────────────────────────────────────────────────────────────────┐                                                                                                             
 │                      Application Layer                          │                                                                                                             
 │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │                                                                                                              
 │  │   LMS Backend   │  │  Qwen Code API  │  │   Nanobot      │  │                                                                                                              
 │  │   (FastAPI)     │  │  (LLM Gateway)  │  │   (AI Agent)   │  │                                                                                                              
 │  └────────┬────────┘  └────────┬────────┘  └───────┬────────┘  │                                                                                                              
 └───────────┼────────────────────┼───────────────────┼────────────┘                                                                                                             
             │                    │                   │                                                                                                                          
             ▼                    ▼                   ▼                                                                                                                          
 ┌─────────────────────────────────────────────────────────────────┐                                                                                                             
 │                      Data & Observability Layer                 │                                                                                                             
 │  ┌──────────┐  ┌───────────┐  ┌──────────────┐  ┌───────────┐  │                                                                                                              
 │  │PostgreSQL│  │  pgAdmin  │  │VictoriaLogs │  │Victoria   │  │                                                                                                               
 │  │Database  │  │  (Admin)  │  │  (Logs)     │  │Traces     │  │                                                                                                               
 │  └──────────┘  └───────────┘  └──────────────┘  └───────────┘  │                                                                                                              
 │  ┌───────────────────────────────────────────────────────────┐  │                                                                                                             
 │  │              OpenTelemetry Collector                      │  │                                                                                                             
 │  └───────────────────────────────────────────────────────────┘  │                                                                                                             
 └─────────────────────────────────────────────────────────────────┘                                                                                                             
           │                                                                                                                                                                     
           ▼                                                                                                                                                                     
 ┌─────────────────────────────────────────────────────────────────┐                                                                                                             
 │                    External Services                            │                                                                                                             
 │  ┌───────────────────────────────────────────────────────────┐ │                                                                                                              
 │  │              Autochecker API                              │ │                                                                                                              
 │  │         (External learning data source)                   │ │                                                                                                              
 │  └───────────────────────────────────────────────────────────┘ │                                                                                                              
 └─────────────────────────────────────────────────────────────────┘                                                                                                             
                                                                                                                                                                                 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Service Details                                                                                                                                                                  

                                                                                                                                                
 Service             Technology                 Purpose                                                                                         
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 
 backend             FastAPI (Python)           Core LMS API providing endpoints for items, analytics, learners, labs, and ETL pipeline         
 client-web-react    React + TypeScript + Vite  Web frontend with Items page and Dashboard (charts for submissions, scores, groups, pass rates) 
 client-web-flutter  Flutter                    Alternative web client (optional)                                                               
 caddy               Caddy                      Reverse proxy serving frontend files and routing API requests                                   
 postgres            PostgreSQL 18.3            Primary database storing learning data                                                          
 pgadmin             pgAdmin4                   Database administration UI                                                                      
 qwen-code-api       Python                     LLM gateway for AI coding assistance                                                            
 nanobot             Python                     AI agent for chat and automation (optional)                                                     
 victorialogs        VictoriaLogs               Log storage and retrieval                                                                       
 victoriatraces      VictoriaTraces             Distributed trace storage                                                                       
 otel-collector      OpenTelemetry              Collects and exports traces/logs to Victoria stack                                              
                                                                                                                                                

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Key Features                                                                                                                                                                     

 1 API-First Design: FastAPI backend with Swagger UI documentation                                                                                                               
 2 Authentication: Bearer token auth using LMS_API_KEY                                                                                                                           
 3 ETL Pipeline: Syncs data from external Autochecker API via POST /pipeline/sync                                                                                                
 4 Analytics Dashboard:                                                                                                                                                          
    • Submissions timeline                                                                                                                                                       
    • Score distribution                                                                                                                                                         
    • Group performance                                                                                                                                                          
    • Task pass rates                                                                                                                                                            
 5 Observability: Full OpenTelemetry integration with VictoriaLogs and VictoriaTraces                                                                                            
 6 Containerized: All services run in Docker containers on a private network (lms-network)                                                                                       

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Data Flow                                                                                                                                                                        

 1 Data Ingestion: ETL pipeline pulls from Autochecker API → PostgreSQL                                                                                                          
 2 API Requests: Frontend → Caddy → Backend → PostgreSQL                                                                                                                         
 3 AI Integration: Backend/Nanobot → Qwen Code API → LLM                                                                                                                         
 4 Observability: All services → OpenTelemetry → VictoriaLogs/Traces                                                                                                             

This architecture supports scalability, observability, and extensibility for learning analytics and AI-assisted education.
 
## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->


🐈 nanobot
The LMS system requires a specific lab to retrieve score-related data (pass rates, completion rates, group performance, top learners). However, I can show you the registered    
learners in the system without lab filtering:                                                                                                                                    

LMS Learners Overview                                                                                                                                                            

Total Learners: 258                                                                                                                                                              

Group Distribution:                                                                                                                                                              

                    
 Group        Count 
 ────────────────── 
 B25-CSE-01   24    
 B25-CSE-02   24    
 B25-CSE-03   24    
 B25-CSE-04   24    
 B25-CSE-05   25    
 B25-DSAI-01  24    
 B25-DSAI-02  24    
 B25-DSAI-03  24    
 B25-DSAI-04  24    
 B25-DSAI-05  25    
 unknown      3     
                    

Sample Learners:                                                                                                                                                                 

                               
 ID   External ID  Group       
 ───────────────────────────── 
 1    4a861abe     unknown     
 2    dc74d73d     B25-DSAI-05 
 3    1c25f779     B25-CSE-03  
 4    4ab50349     B25-DSAI-05 
 5    f8ae7ade     B25-CSE-03  
 ...  ...          ...         
                               

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To see scores, you need to specify a lab. Available labs are:                                                                                                                    

 • lab-01 through lab-08                                                                                                                                                         

Would you like me to show scores for a specific lab? For example:                                                                                                                

 • Pass rates per task                                                                                                                                                           
 • Completion rate                                                                                                                                                               
 • Top learners by average score                                                                                                                                                 
 • Group performance comparison 

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

**Nanobot Gateway Startup Log:**

```
nanobot-1  | Resolved config written to /app/nanobot/config.resolved.json
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-31 15:01:28.271 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-03-31 15:01:28.665 | INFO     | nanobot.channels.manager:start_all:91 - Starting webchat channel...
nanobot-1  | 2026-03-31 15:01:28.668 | INFO     | nanobot.channels.manager:_dispatch_outbound:119 - Outbound dispatcher started
```

**Docker Compose Service Status:**

```
NAME                    SERVICE         STATUS
se-toolkit-lab-8-nanobot-1   nanobot         running
```

The nanobot gateway is running as a Docker Compose service with the webchat channel enabled. The gateway resolves environment variables at runtime via `entrypoint.py` and connects to:
- LLM: `http://qwen-code-api:8080/v1` (Docker service name)
- LMS Backend: `http://backend:8000` (Docker service name)
- WebChat channel: port 8765, accessible via Caddy at `/ws/chat`

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

**Flutter Web Client:**

The Flutter web client is accessible at `http://localhost:42002/flutter`. The main.dart.js file is present and serving real content (2.4MB).

**Full Stack Verification:**

```bash
# 1. Flutter serves content at /flutter
curl -sf http://localhost:42002/flutter/main.dart.js | wc -c
# Output: 2455692 (2.4MB of content)

# 2. WebSocket at /ws/chat accepts connections with NANOBOT_ACCESS_KEY
# 3. Agent responds through WebSocket without LLM errors
```

**WebSocket Test Results:**

Test command:
```bash
/root/se-toolkit-lab-8/.venv/bin/python3 -c "
import asyncio, websockets, json
async def test():
    async with websockets.connect('ws://localhost:42002/ws/chat?access_key=msnk') as ws:
        await ws.send(json.dumps({'content': 'What labs are available?'}))
        print(await ws.recv())
asyncio.run(test())
"
```

**Agent Response to "What labs are available?":**

```json
{
  "type": "text",
  "content": "Here are the available labs for **Lab 8 — The Agent is the Interface**:\n\n## Required Tasks\n\n1. **Task 1 — Set Up the Agent**\n   - Install nanobot, configure Qwen API, add MCP tools, write skill prompt\n\n2. **Task 2 — Deploy and Connect a Web Client**\n   - Dockerize nanobot, add WebSocket channel + Flutter chat UI\n\n3. **Task 3 — Give the Agent New Eyes**\n   - Explore observability data, write log/trace MCP tools\n\n4. **Task 4 — Diagnose a Failure and Make the Agent Proactive**\n   - Investigate a failure, schedule in-chat health checks, fix a planted bug\n\n## Optional Tasks\n\n1. **Task 1 — Add a Telegram Bot Client**\n   - Same agent, different interface\n\nWould you like to start with the prerequisites, or jump into Task 1?",
  "format": "markdown"
}
```

**Agent Response to "What can you do in this system?":**

```
I'm nanobot 🐈, your AI development assistant. Here's what I can help you with:

## File & Project Operations
- **Read, write, and edit files** — I can work with any file in your workspace
- **Browse directories** — Explore project structure
- **Run shell commands** — Execute CLI tools, build commands, tests (with safety limits)

## Development Support
- **Build the Telegram bot** — We're working through a lab with 4 tasks:
  1. Basic handlers with `--test` mode
  2. LMS API integration
  3. LLM tool-calling for natural language
  4. Docker deployment
- **Debug errors** — Diagnose issues by checking logs, configs, and code
- **Search documentation** — I check the `wiki/` directory first for answers

## Web & Research
- **Search the web** — Find documentation, tutorials, solutions
- **Fetch URLs** — Extract readable content from web pages

## Automation
- **Schedule tasks** — Set up reminders or recurring jobs with cron
- **Spawn subagents** — Delegate complex tasks to background agents

## Memory
- **Remember context** — I store important facts in `MEMORY.md`
- **Log history** — All sessions are logged in `HISTORY.md` for later reference
```

**Full Stack Verification:**

1. ✅ Flutter serves content at `/flutter` (main.dart.js present)
2. ✅ WebSocket at `/ws/chat` accepts connections with `NANOBOT_ACCESS_KEY`
3. ✅ Agent responds through WebSocket without LLM errors

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
