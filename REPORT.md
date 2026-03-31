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

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

🐈 nanobot
The LMS system requires specifying a lab to retrieve scores. There isn't a direct endpoint for overall scores across all labs.                                                   

I can show you:                                                                                                                                                                  

 • Top learners for a specific lab (by average score)                                                                                                                            
 • Pass rates for a specific lab (avg score and attempt count per task)                                                                                                          
 • Group performance for a specific lab (avg score + student count per group)                                                                                                    

Would you like me to show scores for a particular lab? For example, I could show the top learners for lab-08 or any other lab from the list:                                     

 1 Lab 01 – Products, Architecture & Roles                                                                                                                                       
 2 Lab 02 — Run, Fix, and Deploy a Backend Service                                                                                                                               
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy                                                                                                                       
 4 Lab 04 — Testing, Front-end, and AI Agents                                                                                                                                    
 5 Lab 05 – Data Pipeline and Analytics Dashboard                                                                                                                                
 6 Lab 06 — Build Your Own Agent                                                                                                                                                 
 7 Lab 07 — Build a Client with an AI Coding Agent                                                                                                                               
 8 lab-08                                                                                                                                                                        

Just let me know which lab you'd like to see scores for! 
## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

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
