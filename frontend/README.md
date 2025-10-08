# 🎨 AI Studio Frontend - Next.js + TypeScript + Tailwind CSS

Modern, production-ready frontend for AI Studio built with Next.js 14, TypeScript, React, and Tailwind CSS.

## 🛠️ Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls
- **Zustand** - State management
- **React Hot Toast** - Notifications
- **Lucide React** - Beautiful icons
- **date-fns** - Date utilities

## 📦 Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure environment variables:**
```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 🚀 Development

Run the development server:
```bash
npm run dev
```

The app will be available at [http://localhost:3000](http://localhost:3000)

## 🏗️ Build for Production

Build the production bundle:
```bash
npm run build
```

Start the production server:
```bash
npm run start
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout with providers
│   │   ├── page.tsx            # Landing page
│   │   ├── globals.css         # Global styles
│   │   ├── auth/              # Authentication pages
│   │   │   ├── login/         # Login page
│   │   │   └── signup/        # Signup page
│   │   └── dashboard/         # Dashboard pages (protected)
│   │       ├── layout.tsx     # Dashboard layout
│   │       └── page.tsx       # Dashboard home
│   ├── components/            # Reusable React components
│   │   ├── ui/               # UI components (buttons, cards, etc.)
│   │   └── dashboard/        # Dashboard-specific components
│   ├── lib/                  # Utilities and configurations
│   │   ├── api.ts           # API client with axios
│   │   ├── store.ts         # Zustand state management
│   │   └── utils.ts         # Utility functions
│   └── types/               # TypeScript type definitions
│       └── index.ts         # All type definitions
├── public/                  # Static assets
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
├── next.config.js          # Next.js configuration
└── package.json            # Dependencies and scripts
```

## 🎨 Key Features

### Landing Page
- Modern, responsive design
- Feature showcase
- Pricing tiers
- Smooth animations

### Authentication
- Login with JWT
- Signup with validation
- Password visibility toggle
- Error handling with toast notifications

### Dashboard
- Protected routes
- Sidebar navigation
- Real-time statistics
- AI insights
- Multiple modules:
  - Clients management
  - Projects & tasks
  - AI Design Generator
  - Product sourcing
  - Finance & invoicing
  - Marketing assistant
  - Calendar & events

## 🔧 Configuration

### Tailwind CSS
Custom theme configured in `tailwind.config.ts`:
- Primary color palette (indigo)
- Custom animations
- Extended utilities
- Forms plugin

### TypeScript
Strict type checking enabled with path aliases:
- `@/*` → `src/*`
- `@/components/*` → `src/components/*`
- `@/lib/*` → `src/lib/*`

### API Integration
All API calls go through `/lib/api.ts`:
- Automatic JWT token attachment
- Error handling with interceptors
- Type-safe requests and responses

## 🔐 Authentication Flow

1. User submits login/signup form
2. API client sends request to Flask backend
3. JWT token received and stored in localStorage
4. User state updated in Zustand store
5. Protected routes check authentication
6. Redirect to dashboard on success

## 🎯 State Management

Using Zustand for global state:
- `useAuthStore` - User authentication state
- `useUIStore` - UI state (sidebar, modals)
- `useLoadingStore` - Loading states

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript checker

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Flask backend URL | `http://localhost:5000` |
| `NEXT_PUBLIC_APP_URL` | Frontend URL | `http://localhost:3000` |

## 🚦 Running with Backend

1. **Start Flask backend** (from project root):
```bash
cd backend
python app.py
```
Backend runs on: `http://localhost:5000`

2. **Start Next.js frontend** (in separate terminal):
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

## 📱 Responsive Design

The app is fully responsive with breakpoints:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🎨 Styling Conventions

Using Tailwind CSS with custom utility classes:
- `.btn` - Button base styles
- `.card` - Card container
- `.input` - Form input fields
- `.badge` - Status badges

## 🔍 Type Safety

All components, functions, and API calls are fully typed:
- Interfaces in `/src/types/index.ts`
- Type-safe API client
- Props validation with TypeScript

## 🚀 Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy automatically

### Manual Deployment
```bash
npm run build
npm run start
```

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand Guide](https://docs.pmnd.rs/zustand)

## 🤝 Integration with Backend

The frontend connects to the Flask backend via:
1. API calls to `http://localhost:5000/api`
2. JWT authentication in headers
3. Automatic token refresh
4. Error handling and redirects

All API endpoints are type-safe and documented in `/src/lib/api.ts`.

## ⚡ Performance

- Server-side rendering (SSR) with Next.js
- Automatic code splitting
- Image optimization
- Lazy loading components
- Efficient state management

## 🐛 Troubleshooting

**Port 3000 already in use:**
```bash
npm run dev -- -p 3001
```

**API connection issues:**
- Check Flask backend is running on port 5000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in Flask backend

**Build errors:**
```bash
rm -rf .next
npm run build
```

---

Built with ❤️ using Next.js, TypeScript, and Tailwind CSS

