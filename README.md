# 🎨 AI Studio for Interior Designers

A comprehensive SaaS platform that helps interior designers manage clients, projects, and design processes through a unified AI-powered dashboard.

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router and SSR
- **TypeScript** - Type-safe development
- **React** - UI component library
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls
- **Zustand** - Lightweight state management
- **React Hot Toast** - Beautiful toast notifications
- **Lucide React** - Icon library

### Backend
- **Python 3.9+** - Backend language
- **Flask** - Web framework
- **MySQL** - Relational database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **OpenAI API** - AI features (GPT-4 + DALL-E)
- **Bcrypt** - Password hashing

## 📁 Project Structure

```
DZN AI/
├── frontend/                    # Next.js frontend
│   ├── src/
│   │   ├── app/                # Next.js App Router pages
│   │   │   ├── page.tsx        # Landing page
│   │   │   ├── auth/           # Authentication pages
│   │   │   │   ├── login/      # Login page
│   │   │   │   └── signup/     # Signup page
│   │   │   └── dashboard/      # Dashboard pages (protected)
│   │   │       ├── layout.tsx  # Dashboard layout
│   │   │       └── page.tsx    # Dashboard home
│   │   ├── components/         # React components
│   │   ├── lib/               # Utilities & API client
│   │   │   ├── api.ts         # API client
│   │   │   ├── store.ts       # State management
│   │   │   └── utils.ts       # Helper functions
│   │   └── types/             # TypeScript definitions
│   ├── package.json
│   └── README.md
│
├── backend/                    # Flask API
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration
│   ├── models/                # Database models
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── project.py
│   │   ├── design.py
│   │   └── ... (10 models total)
│   ├── routes/                # API endpoints
│   │   ├── auth_routes.py
│   │   ├── client_routes.py
│   │   ├── project_routes.py
│   │   ├── design_routes.py
│   │   └── ... (9 route files)
│   ├── services/              # Business logic
│   │   └── ai_service.py      # OpenAI integration
│   └── utils/                 # Helper utilities
│       ├── db.py
│       └── auth.py
│
├── database/                  # Database setup
│   └── schema.sql            # MySQL schema
│
├── requirements.txt          # Python dependencies
├── prd.md                    # Product requirements
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **MySQL 8.0+**
- **OpenAI API Key**

### 1. Clone & Setup

```bash
cd "DZN AI"
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup MySQL database
mysql -u root -p < database/schema.sql

# Create .env file in backend directory
cp backend/.env.example backend/.env

# Edit .env with your credentials:
# - Database credentials
# - JWT secret keys
# - OpenAI API key
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:5000
# NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
# From project root
python backend/app.py
```
Backend runs on: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
# From frontend directory
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

### 5. Access the Application

- **Landing Page**: http://localhost:3000
- **Login**: http://localhost:3000/auth/login
- **Signup**: http://localhost:3000/auth/signup
- **Dashboard**: http://localhost:3000/dashboard (after login)
- **API Docs**: http://localhost:5000/api/health

## 🎯 Core Features

### ✅ Implemented Features

1. **🏠 Dashboard Home**
   - Overview statistics
   - AI-powered insights
   - Recent activity
   - Quick actions

2. **👥 Client Management**
   - Client profiles with preferences
   - Contact information
   - Project tracking
   - AI sentiment analysis (API ready)

3. **🏗️ Project Manager**
   - Project lifecycle management
   - Task tracking
   - Budget monitoring
   - Timeline visualization
   - AI insights for delays

4. **🎨 AI Design Generator**
   - Generate moodboards with DALL-E
   - Color palette suggestions
   - Room design concepts
   - Product recommendations
   - GPT-4 descriptions

5. **🛋️ Product Sourcing**
   - Product catalog
   - Budget tracking
   - Purchase status
   - Search and filters

6. **💰 Finance Manager**
   - Invoice creation
   - Payment tracking
   - Financial summaries
   - Overdue alerts

7. **📣 Marketing Assistant**
   - AI content generation
   - Social media captions
   - Blog posts
   - Email templates
   - Post scheduling

8. **📅 Calendar & Events**
   - Event management
   - Meeting scheduling
   - Deadline tracking
   - Automated reminders

9. **🔐 Authentication**
   - JWT-based auth
   - Secure password hashing
   - Role-based access
   - Session management

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Flask Configuration
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ai_studio
DB_USER=root
DB_PASSWORD=your-password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📊 Database Schema

The application uses MySQL with 11 tables:
- `users` - Designer accounts
- `clients` - Client information
- `projects` - Design projects
- `tasks` - Project tasks
- `messages` - Client communications
- `designs` - AI-generated designs
- `products` - Product catalog
- `invoices` - Financial documents
- `marketing_content` - Marketing materials
- `calendar_events` - Scheduled events
- `activity_log` - User activity tracking

## 🎨 Frontend Architecture

### Pages
- `/` - Landing page
- `/auth/login` - Login page
- `/auth/signup` - Signup page
- `/dashboard` - Dashboard home (protected)
- `/dashboard/clients` - Clients management
- `/dashboard/projects` - Projects management
- `/dashboard/designs` - AI Design Generator
- `/dashboard/products` - Product sourcing
- `/dashboard/invoices` - Finance manager
- `/dashboard/marketing` - Marketing assistant
- `/dashboard/calendar` - Calendar & events

### State Management (Zustand)
- `useAuthStore` - User authentication
- `useUIStore` - UI state (sidebar, modals)
- `useLoadingStore` - Loading states

### API Client
All API calls go through `/lib/api.ts`:
- Automatic JWT token injection
- Error handling with interceptors
- Type-safe requests/responses
- Automatic logout on 401

## 🔐 Authentication Flow

1. User submits credentials
2. Backend validates and returns JWT
3. Token stored in localStorage
4. Token sent in Authorization header
5. Protected routes verify token
6. Automatic logout on expiration

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh token

### Dashboard
- `GET /api/dashboard/overview` - Dashboard stats
- `GET /api/dashboard/insights` - AI insights

### Clients
- `GET /api/clients` - List clients
- `POST /api/clients` - Create client
- `GET /api/clients/:id` - Get client
- `PUT /api/clients/:id` - Update client
- `DELETE /api/clients/:id` - Delete client

### Projects
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `GET /api/projects/:id` - Get project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project
- `POST /api/projects/:id/ai-insights` - Generate AI insights

### Designs
- `GET /api/designs` - List designs
- `POST /api/designs/generate` - Generate AI design
- `GET /api/designs/:id` - Get design
- `DELETE /api/designs/:id` - Delete design

*...and more (40+ endpoints total)*

## 💰 Subscription Tiers

### Free Plan (£0/month)
- 2 projects
- 5 AI generations/month
- Client management
- Basic invoicing

### Pro Plan (£29/month)
- Unlimited projects
- Unlimited AI generations
- Marketing tools
- Product sourcing AI
- Priority support

### Agency Plan (£79/month)
- Everything in Pro
- Team collaboration
- Advanced analytics
- Custom branding
- API access

## 🚀 Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy automatically

### Backend (Render/Railway)
1. Connect GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Start command: `gunicorn backend.app:app`

## 🧪 Testing

### Backend
```bash
pytest backend/tests/
```

### Frontend
```bash
cd frontend
npm run test
```

## 📝 Development Workflow

1. **Backend Development**
   - Edit Python files in `backend/`
   - Flask auto-reloads on changes
   - Test endpoints with Postman/curl

2. **Frontend Development**
   - Edit TypeScript/React files in `frontend/src/`
   - Next.js hot-reloads on changes
   - Check browser console for errors

3. **Database Changes**
   - Update `database/schema.sql`
   - Create migration scripts
   - Test with sample data

## 🐛 Troubleshooting

**Backend won't start:**
- Check MySQL is running
- Verify database credentials in .env
- Ensure all Python dependencies installed

**Frontend won't connect to API:**
- Check `NEXT_PUBLIC_API_URL` in .env.local
- Verify backend is running on port 5000
- Check CORS settings in Flask

**Database errors:**
- Run schema.sql to create tables
- Check MySQL user permissions
- Verify database name matches .env

## 📚 Documentation

- [Frontend README](frontend/README.md) - Detailed frontend docs
- [PRD](prd.md) - Product requirements
- [API Documentation](docs/api.md) - API reference (coming soon)

## 🤝 Contributing

This is a private project. For questions or support, contact the development team.

## 📄 License

Proprietary - All rights reserved

## 🎉 Next Steps

1. **Setup Environment** - Follow quick start guide
2. **Test Features** - Try all dashboard modules
3. **Add Your OpenAI Key** - Enable AI features
4. **Create Test Data** - Add clients and projects
5. **Generate Designs** - Try AI design generator
6. **Customize** - Adapt to your needs

## 💡 Tips

- Use Chrome DevTools for debugging
- Check browser console for errors
- Monitor Flask logs for backend issues
- Use React DevTools for component inspection
- Test API endpoints with Postman

---

**Built with ❤️ using Next.js, TypeScript, Tailwind CSS, Flask, and OpenAI**

For support: support@aistudio.design
