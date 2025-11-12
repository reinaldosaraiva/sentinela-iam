# Sentinela UI

A modern, Next.js-based web interface for the Sentinela Identity and Access Management (IAM) system. Inspired by Permit.io, this interface provides comprehensive policy management, user administration, and authorization monitoring capabilities.

## 🚀 Features

### Core Functionality
- **Policy Management**: Create, edit, and test Cedar-based authorization policies
- **User Management**: Manage users, groups, and access permissions
- **Dashboard**: Real-time monitoring and analytics
- **Audit Logs**: Comprehensive authorization tracking
- **Interactive Testing**: Test policies with real-time feedback

### Technical Features
- **Modern Stack**: Next.js 14, TypeScript, Tailwind CSS
- **Responsive Design**: Mobile-first, accessible interface
- **Real-time Updates**: Live policy validation and testing
- **Professional UI**: Clean, intuitive interface similar to Permit.io

## 📁 Project Structure

```
sentinela-ui/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx           # Dashboard page
│   │   ├── policies/          # Policy management
│   │   ├── users/             # User management
│   │   ├── audit/             # Audit logs
│   │   └── settings/          # System settings
│   ├── components/            # Reusable React components
│   │   ├── Sidebar.tsx        # Navigation sidebar
│   │   ├── Header.tsx         # Page header with search
│   │   ├── Dashboard.tsx      # Main dashboard component
│   │   ├── PolicyEditor.tsx   # Cedar policy editor
│   │   └── UserManagement.tsx # User management interface
│   ├── lib/                   # Utility libraries
│   │   ├── api.ts            # API client with authentication
│   │   └── utils.ts          # Helper functions
│   └── globals.css            # Global styles and Tailwind
├── package.json               # Dependencies and scripts
├── tailwind.config.js         # Tailwind CSS configuration
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Sentinela backend services running

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local` with your backend URLs:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_POLICY_API_URL=http://localhost:8001
   NEXT_PUBLIC_BUSINESS_API_URL=http://localhost:8002
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🎯 Usage

### Dashboard
- **Overview**: System metrics and health status
- **Recent Activity**: Latest authorization requests and policy changes
- **Quick Actions**: Fast access to common tasks
- **Analytics**: Policy performance and user activity insights

### Policy Management
- **Policy Editor**: Monaco-based Cedar policy editor with syntax highlighting
- **Real-time Validation**: Instant policy syntax checking
- **Policy Testing**: Interactive testing with sample scenarios
- **Version Control**: Policy history and rollback capabilities

### User Management
- **User Administration**: Create, edit, and manage user accounts
- **Group Management**: Organize users into functional groups
- **Access Control**: Assign policies and permissions
- **Bulk Operations**: Mass user updates and imports

### Audit & Monitoring
- **Authorization Logs**: Complete audit trail of all access decisions
- **Performance Metrics**: Response times and success rates
- **Compliance Reports**: Generate compliance and audit reports
- **Real-time Monitoring**: Live dashboard of system activity

## 🔧 Configuration

### API Integration
The UI integrates with three main backend services:

1. **Policy API** (`http://localhost:8001`): Policy CRUD operations
2. **Business API** (`http://localhost:8002`): Authorization decisions
3. **Mock Keycloak** (`http://localhost:8080`): User authentication

### Authentication
- JWT-based authentication
- Automatic token refresh
- Role-based access control

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Modern icon library
- **Custom Components**: Reusable UI components
- **Responsive Design**: Mobile-first approach

## 🧪 Development

### Available Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript checks
```

### Component Development
- Use TypeScript for all components
- Follow React best practices
- Implement proper error boundaries
- Ensure accessibility compliance

### API Integration
- Use the centralized API client in `src/lib/api.ts`
- Handle authentication automatically
- Implement proper error handling
- Use React Query for data fetching (future enhancement)

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#3B82F6)
- **Success**: Green (#10B981)
- **Warning**: Orange (#F59E0B)
- **Error**: Red (#EF4444)
- **Neutral**: Gray shades (#6B7280, #9CA3AF, etc.)

### Typography
- **Font**: Inter (system font stack)
- **Headings**: Bold, with proper hierarchy
- **Body**: Regular weight, good readability
- **Code**: Monospace font for technical content

### Components
- **Buttons**: Multiple variants (primary, secondary, ghost)
- **Forms**: Consistent input styling
- **Cards**: Clean, bordered containers
- **Modals**: Overlay dialogs with proper focus management

## 🔐 Security Considerations

- **Input Validation**: All user inputs are validated
- **XSS Prevention**: Proper content sanitization
- **CSRF Protection**: Token-based CSRF protection
- **Authentication**: Secure JWT handling
- **Authorization**: Role-based access control

## 📊 Performance

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: Regular bundle size monitoring
- **Caching**: Proper caching strategies
- **Lazy Loading**: Components loaded on demand

## 🚀 Deployment

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_POLICY_API_URL`: Policy service URL
- `NEXT_PUBLIC_BUSINESS_API_URL`: Business API URL
- `NEXTAUTH_SECRET`: Authentication secret
- `NEXTAUTH_URL`: Application URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the Sentinela IAM system. See the main project license for details.

## 🔗 Related Projects

- **Sentinela Backend**: Core authorization services
- **Cedar Engine**: Policy evaluation engine
- **Mock Keycloak**: Authentication service
- **Policy API**: Policy management service

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API specifications