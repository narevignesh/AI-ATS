﻿# AI-ATS Resume System - Frontend

## 🚀 Overview
A modern, responsive React-based frontend for the AI-ATS Resume System, featuring a beautiful UI with advanced resume parsing, ATS scoring, AI-powered suggestions, and comprehensive user management.

## 🧰 Tech Stack
- **Framework:** React 18.3.1 with Vite 5.4.1
- **Styling:** Tailwind CSS 3.4.11 with shadcn/ui components
- **Routing:** React Router DOM 7.6.2
- **State Management:** React Query (TanStack Query) 5.56.2
- **Charts:** Chart.js 4.5.0 with React Chart.js 2
- **HTTP Client:** Axios 1.10.0
- **Forms:** React Hook Form 7.53.0 with Zod validation
- **UI Components:** Radix UI primitives with custom styling
- **Animations:** Tailwind CSS animations and Framer Motion
- **Notifications:** React Toastify 11.0.5 and Sonner 1.5.0

## 📁 Project Structure
```
frontend/app/
├── public/
│   ├── favicon.ico
│   ├── placeholder.svg
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── Admin/
│   │   │   └── AdminDashboard.jsx      # Admin dashboard component
│   │   ├── Auth/
│   │   │   ├── Login.jsx               # Login form
│   │   │   ├── Register.jsx            # Registration form
│   │   │   ├── ForgotPassword.jsx      # Forgot password form
│   │   │   ├── OTPVerification.jsx     # OTP verification
│   │   │   └── ResetPassword.jsx       # Password reset form
│   │   ├── Resume/
│   │   │   └── Upload.jsx              # Resume upload component
│   │   ├── ATS/
│   │   │   └── ATSScore.jsx            # ATS scoring component
│   │   ├── Suggestions/
│   │   │   └── Improve.jsx             # AI suggestions component
│   │   └── ui/                         # shadcn/ui components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── input.tsx
│   │       ├── dialog.tsx
│   │       ├── toast.tsx
│   │       └── ... (50+ components)
│   ├── pages/
│   │   ├── Landing.jsx                 # Landing page
│   │   ├── Dashboard.jsx               # User dashboard
│   │   ├── Index.tsx                   # App entry point
│   │   └── NotFound.tsx                # 404 page
│   ├── services/
│   │   └── api.js                      # API service functions
│   ├── hooks/
│   │   ├── use-mobile.tsx              # Mobile detection hook
│   │   └── use-toast.ts                # Toast notification hook
│   ├── lib/                            # Utility libraries
│   ├── App.jsx                         # Main app component
│   ├── App.css                         # App styles
│   ├── index.css                       # Global styles
│   └── main.jsx                        # App entry point
├── package.json                        # Dependencies and scripts
├── vite.config.ts                      # Vite configuration
├── tailwind.config.ts                  # Tailwind CSS configuration
├── tsconfig.json                       # TypeScript configuration
└── components.json                     # shadcn/ui configuration
```

## ⚙️ Installation & Setup

### 1. Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Backend server running (see backend README)

### 2. Environment Setup
```bash
# Navigate to frontend directory
cd frontend/app

# Install dependencies
npm install
# or
yarn install
# or
bun install
```

### 3. Environment Configuration
Create `.env` file in the frontend/app directory:
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api

# Optional: Analytics and monitoring
VITE_APP_ENV=development
```

### 4. Run the Application
```bash
# Development mode
npm run dev
# or
yarn dev
# or
bun dev
```

The application will start at `http://localhost:8080`

## 🎨 UI Components

### Core Components

#### Authentication Components
- **Login.jsx** - User login with email/password
- **Register.jsx** - User registration with OTP verification
- **ForgotPassword.jsx** - Password reset flow
- **OTPVerification.jsx** - OTP input and validation
- **ResetPassword.jsx** - New password setup

#### Resume Management
- **Upload.jsx** - Drag & drop resume upload
- File validation and preview
- Progress indicators
- Error handling

#### ATS Scoring
- **ATSScore.jsx** - ATS score visualization
- Interactive charts with Chart.js
- Score breakdown display
- Missing keywords highlighting

#### AI Suggestions
- **Improve.jsx** - AI-powered resume improvements
- Section-wise suggestions
- Copy-to-clipboard functionality
- Interactive keyword suggestions

#### Admin Dashboard
- **AdminDashboard.jsx** - Comprehensive admin interface
- User management
- Resume analytics
- Activity monitoring

### UI Component Library (shadcn/ui)
The project uses 50+ pre-built components:
- **Layout:** Card, Container, Grid, Stack
- **Forms:** Input, Textarea, Select, Checkbox, Radio
- **Navigation:** Button, Link, Breadcrumb, Menu
- **Feedback:** Toast, Alert, Progress, Skeleton
- **Data Display:** Table, Badge, Avatar, Tooltip
- **Overlay:** Dialog, Modal, Popover, Drawer

## 🔌 API Integration

### Service Layer (`services/api.js`)
```javascript
// Authentication
export const register = (data) => API.post('/signup/', data);
export const login = (data) => API.post('/login/', data);
export const verifyOtp = (data) => API.post('/verify-otp/', data);
export const forgotPassword = (data) => API.post('/forgot-password/', data);

// Resume Management
export const uploadResume = (formData) => API.post('/upload-resume/', formData);
export const parseResume = (data) => API.post('/parse-resume/', data);

// ATS Scoring
export const getATSScore = (data) => API.post('/get-ats-score/', data);

// AI Suggestions
export const getSuggestions = (data) => API.post('/get-suggestions/', data);

// Admin Functions
export const getAllUsers = () => API.get('/admin/users/');
export const getAllResumes = () => API.get('/admin/resumes/');
export const deleteUser = (id) => API.delete(`/admin/delete-user/${id}`);

// User Activity
export const getUserActivity = () => API.get('/user-activity/');
```

### HTTP Client Configuration
```javascript
const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  headers: { 'Content-Type': 'application/json' }
});

// JWT Token Interceptor
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## 🎯 Key Features

### 1. User Authentication
- **Secure Login/Register** with JWT tokens
- **OTP Verification** via email
- **Password Reset** with email OTP
- **Token Management** with automatic refresh
- **Protected Routes** with role-based access

### 2. Resume Management
- **Drag & Drop Upload** for PDF/DOCX files
- **File Validation** with size and type checks
- **Progress Indicators** for upload status
- **Resume Parsing** with structured data extraction
- **Preview Functionality** for uploaded files

### 3. ATS Scoring System
- **Real-time Scoring** with visual feedback
- **Interactive Charts** showing score breakdown
- **Keyword Analysis** with missing keywords
- **Skill Matching** with percentage indicators
- **Score History** tracking

### 4. AI-Powered Suggestions
- **Section-wise Improvements** for resume
- **Context-aware Suggestions** based on job description
- **Copy-to-clipboard** functionality
- **Interactive Keywords** with click-to-add
- **Professional Tone** enhancement

### 5. Admin Dashboard
- **User Management** with CRUD operations
- **Resume Analytics** with detailed statistics
- **Activity Monitoring** with real-time updates
- **Data Export** functionality
- **System Health** monitoring

### 6. User Dashboard
- **Activity Tracking** with recent actions
- **Statistics Overview** with charts
- **Quick Actions** for common tasks
- **Profile Management** with settings

## 🎨 Styling & Design

### Tailwind CSS Configuration
```javascript
// tailwind.config.ts
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... more color definitions
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### CSS Variables for Theming
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  /* ... more variables */
}
```

## 📱 Responsive Design

### Mobile-First Approach
- **Breakpoints:** sm (640px), md (768px), lg (1024px), xl (1280px)
- **Touch-friendly** interface elements
- **Optimized layouts** for different screen sizes
- **Progressive enhancement** for larger screens

### Component Responsiveness
```javascript
// Example responsive component
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card className="p-4 md:p-6">
    <CardHeader>
      <CardTitle className="text-lg md:text-xl">Title</CardTitle>
    </CardHeader>
    <CardContent className="text-sm md:text-base">
      Content here
    </CardContent>
  </Card>
</div>
```

## 🔧 Development Tools

### Vite Configuration
```typescript
// vite.config.ts
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 8080,
  },
  plugins: [
    react(),
    mode === 'development' && componentTagger(),
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
```

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
