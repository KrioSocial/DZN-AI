🧩 Product Requirements Document (PRD)
Product Name: AI Studio for Interior Designers
Type: SaaS Web Application (Dashboard + Landing Page)
Goal: Help interior designers manage clients, projects, and design processes through a unified AI-powered dashboard.

🧱 Updated Tech Stack — AI Studio for Interior Designers
Layer	Technology	Purpose
Frontend (UI)	React + Next.js + TypeScript + Tailwind CSS	High-performance dashboard, server-side rendering, component reuse, strong typing
Backend (API)	Python (FastAPI or Flask)	Handles business logic, AI API calls, authentication
Database	MySQL (via SQLAlchemy or Prisma)	Stores users, clients, projects, assets, invoices
AI Layer	OpenAI / Stability / Google APIs via Python	Text, image, and 3D generation
Authentication	NextAuth.js (frontend) + JWT in backend	Secure logins and session handling
File Storage	AWS S3 / Firebase Storage	Design assets, project uploads, moodboard exports
Hosting	Vercel (frontend) + Render / Railway / AWS (backend)	Fast global deployment
Version Control & DevOps	GitHub + CI/CD via Vercel & Render	Auto-deployments
Optional Search Layer	ElasticSearch or Pinecone	AI-powered client/style search
🧭 Architecture Overview
Here’s how each part communicates:
Browser (User)
     ↓
Next.js (React + TypeScript)
     ↓        ↔ (API calls via fetch/axios)
Python API (FastAPI / Flask)
     ↓
MySQL Database
     ↓
OpenAI / DALL·E / Stability AI APIs
Next.js handles all UI/UX: pages, dashboard routing, SEO, and client-side interactivity.
Python backend focuses on AI generation, business logic, and database operations.
MySQL holds persistent structured data.
Frontend communicates via REST or GraphQL with the Python API.

For any code that you write, you must include comments on what the code is saying.

1. 🎯 Objective
Create a web platform where interior designers can manage clients, projects, sourcing, and marketing, using AI tools to automate repetitive and creative tasks — replacing the need for multiple apps like Notion, Pinterest, Canva, Gmail, and Excel.
2. 🧠 Core Features (MVP Scope)
Each feature below should be structured as a modular component in the dashboard for scalability.
🏠 Dashboard Home
Overview of:
Ongoing projects
Pending messages
Budgets and deadlines
AI insights
“2 clients haven’t responded in 5 days — suggest follow-up?”
“You’re over budget by £420.”
🧑‍💼 Clients Hub
Client profiles:
Contact info, style preferences, shared files, and active projects
Integrated messaging system (email + chat threads)
AI tools:
Message summarization
Sentiment detection
Smart reminders
AI Persona (learns client’s taste based on past feedback)
🏗️ Project Manager
Projects include:
Design stages, tasks, and files
Visual timelines and progress tracking
AI tools:
Suggests missing steps (e.g., “No lighting plan uploaded yet.”)
Predicts possible delays and suggests fixes
🖼️ AI Design Generator
Inputs: room type, style, budget, keywords
Outputs:
AI moodboard (image generation)
Color palette
Product suggestions
Room description
Export to proposal PDF or client portal
Uses OpenAI (for text) + DALL·E / Stability AI (for images)
🛋️ Product Sourcing
Search by filters (style, price, color, brand)
AI retrieves best matches using retail APIs (e.g., Wayfair, IKEA)
Add to shopping list
Budget control alerts
💸 Finance Manager
Create and track invoices, quotes, and payments
Budget tracking across projects
AI detects overspending or missing invoices
📣 Marketing Assistant
Generate captions, blogs, emails, and post ideas
Schedule posts to Instagram, LinkedIn, Pinterest
AI content generation trained on previous projects
Integration: Meta API, LinkedIn API, or Buffer
📅 Calendar & Automations
Centralized calendar for all deadlines and meetings
Automated actions:
Proposal delivery
Follow-ups
Client reminders
Integration: Google Calendar API
🧩 Optional Add-ons (Post-MVP)
AI 3D/AR Preview (SketchUp or ARKit)
AI Contract Builder
Procurement Tracker
Design Asset Library
Designer Community Hub
Trusted Trades Network
3. ⚙️ System Architecture
Frontend
Framework: Next.js or React (with TypeScript)
UI Library: TailwindCSS + ShadCN/UI
State Management: Zustand or Redux Toolkit
Routing: Next.js App Router
Authentication: Firebase Auth / Clerk / Supabase Auth
File Uploads: Firebase Storage or AWS S3
Backend
Database: Firebase Firestore / Supabase Postgres
Server Logic: Next.js API Routes / Node.js Express
AI Integrations:
GPT-4/5 API (text)
DALL·E or Stability AI (image)
Retail APIs (product sourcing)
Stripe / PayPal (billing)
Email/Automation: SendGrid or Mailgun
Scheduling: Google Calendar API
4. 🧱 Data Model (MVP)
Users
{
  id,
  name,
  email,
  role (designer, admin),
  subscriptionTier,
  createdAt
}
Clients
{
  id,
  userId,
  name,
  contactInfo,
  preferences,
  personalityProfile,
  projects: [projectIds],
  messages: [messageIds],
  createdAt
}
Projects
{
  id,
  userId,
  clientId,
  title,
  status,
  timeline: [milestones],
  tasks: [taskIds],
  budget,
  aiInsights,
  createdAt
}
Messages
{
  id,
  clientId,
  userId,
  messageText,
  sender,
  timestamp,
  aiSummary
}
Designs
{
  id,
  projectId,
  inputs: {roomType, style, budget, keywords},
  outputs: {imageUrls, colorPalette, description, productList},
  createdAt
}
5. 💸 Monetization (Freemium Model)
Tier	Price	Features
Free	£0	2 projects, 5 AI generations/month
Pro	£29/mo	Unlimited projects, marketing tools, AI sourcing
Agency	£79/mo	Team features, analytics, branding, automation
6. 🧠 Tech Integrations (Priority Order)
Function	Integration
Auth & DB	Firebase / Supabase
AI Text	OpenAI GPT-4/5
AI Image	DALL·E / Stability
Payments	Stripe
Calendar	Google Calendar API
Email	SendGrid
Storage	Firebase / AWS S3
7. 🚀 MVP Roadmap
Phase 1 – Core Platform (Weeks 1–4)
Landing Page + Auth (login/signup)
Dashboard home layout
Clients & Projects CRUD
AI Design Generator (basic text + image)
Phase 2 – Business Tools (Weeks 5–8)
Product sourcing
Finance tracking
Marketing Assistant
Phase 3 – Automation Layer (Weeks 9–12)
Calendar integrations
AI insights engine
Notification & automation workflows
8. 🧭 UX Design Notes
Minimalist UI: neutral colors, lots of white space, design-focused aesthetic.
Card-based dashboard layout
AI actions appear as contextual “suggestions”
Include dark mode (designers love it)
Each module should be collapsible / modular for scale.
9. 📢 Marketing Funnel Integration
Public Landing Page with:
Hero section: “Run your design studio like a 10-person team — powered by AI.”
Demo of AI Moodboard Generator
Free sign-up CTA → Dashboard trial
Built with Next.js and connected to app auth.
Newsletter capture form (for launch waitlist)
10. ✅ Success Metrics (Post-MVP)
Metric	Target
Avg. Session Duration	> 6 min
Monthly Active Users	5,000
Conversion Rate (Free → Pro)	15%
AI Feature Usage / Month	70% of users
Retention Rate (30d)	65%
Would you like me to now create the product architecture diagram and folder structure plan (so Cursor can scaffold the entire app — frontend, backend, and APIs)?
That’ll include file hierarchy, API routes, and data flow between modules.
