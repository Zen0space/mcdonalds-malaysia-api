# McDonald's Malaysia Frontend

A modern React/Next.js frontend application that provides an interactive map interface and intelligent chatbot for finding McDonald's outlets in Malaysia.

## 🚀 Features

- **Interactive Map** with Leaflet.js showing all McDonald's outlets
- **Location-based Search** with GPS integration
- **Intelligent Chatbot** powered by Gemini 2.5 Flash
- **Real-time Location Detection** with automatic permission handling
- **Beautiful UI/UX** with McDonald's brand colors and modern design
- **Responsive Design** optimized for desktop and mobile
- **Intersection Analysis** showing overlapping outlet coverage areas
- **Advanced Filtering** by features, operating hours, and distance

## 📋 Prerequisites

- **Node.js 18+** (Recommended: Node.js 20+)
- **npm** or **yarn** package manager
- **Modern Web Browser** with geolocation support
- **Backend API** running (see backend README)

## 🛠️ Installation

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd geolocation-mcdscraper/frontend
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Frontend Environment Setup
Create a `.env.local` file in the frontend directory:
```bash
# Copy the example environment file
cp env.example .env.local
```

Edit `.env.local` with your configuration (usually no changes needed):
```env
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Map Configuration (optional)
NEXT_PUBLIC_MAP_CENTER_LAT=3.1570
NEXT_PUBLIC_MAP_CENTER_LNG=101.7123
NEXT_PUBLIC_MAP_ZOOM=11
```

**Note**: Main environment variables (Gemini API key, database config) are configured in the project root directory. See the [main README](../README.md) for complete environment setup instructions.

## 🚀 Quick Start

### 1. Start Development Server
```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

### 2. Access the Application
- **Application**: http://localhost:3000
- **Map Interface**: Interactive map with all outlets
- **Chatbot**: Click the floating chat button

### 3. Build for Production
```bash
# Build the application
npm run build

# Start production server
npm start
```

## 🗂️ Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js 13+ App Router
│   │   ├── globals.css         # Global styles
│   │   ├── layout.tsx          # Root layout component
│   │   └── page.tsx            # Main page component
│   ├── components/             # React components
│   │   ├── chat/               # Chatbot components
│   │   │   ├── ChatHeader.tsx          # Chat header with location
│   │   │   ├── ChatInput.tsx           # Message input with Enter support
│   │   │   ├── ChatMessages.tsx        # Message display container
│   │   │   ├── ChatPanel.tsx           # Main chat panel
│   │   │   ├── FloatingChatbot.tsx     # Floating chat button
│   │   │   ├── LocationCard.tsx        # McDonald's outlet cards
│   │   │   ├── MessageBubble.tsx       # Individual message bubbles
│   │   │   └── TypingIndicator.tsx     # Chat typing animation
│   │   ├── ErrorBoundary.tsx   # Error handling component
│   │   ├── IntersectionLegend.tsx      # Map legend component
│   │   ├── LoadingSpinner.tsx  # Loading animation
│   │   ├── LocationButton.tsx  # GPS location button
│   │   ├── Map.tsx             # Interactive Leaflet map
│   │   └── MapControls.tsx     # Map control panel
│   ├── hooks/                  # Custom React hooks
│   │   ├── useChatSession.ts   # Chat session management
│   │   └── useGeolocation.ts   # GPS location handling
│   ├── services/               # API and external services
│   │   └── chatApi.ts          # Backend API communication
│   ├── types/                  # TypeScript type definitions
│   │   ├── chat.ts             # Chat-related types
│   │   └── index.ts            # Common types
│   └── utils/                  # Utility functions
│       ├── distance.ts         # Distance calculations
│       ├── logger.ts           # Logging utilities
│       └── outletParser.ts     # McDonald's data parsing
├── public/                     # Static assets
├── package.json               # Dependencies and scripts
├── next.config.js             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind CSS configuration
└── env.example                # Environment template
```

## 🎨 Key Components

### **Interactive Map (`Map.tsx`)**
- **Leaflet.js Integration**: High-performance mapping
- **Custom Markers**: McDonald's branded markers with hover effects
- **Radius Visualization**: 5KM coverage circles
- **Intersection Analysis**: Overlapping outlet detection
- **Click Interactions**: Select outlets for detailed view

### **Intelligent Chatbot (`chat/`)**
- **FloatingChatbot**: Always-accessible chat interface
- **LocationCard**: Beautiful outlet information cards
- **Auto-location**: Automatic GPS detection and usage
- **Real-time Responses**: Powered by Gemini 2.5 Flash
- **Enter to Send**: Modern chat UX with keyboard shortcuts

### **Location Services (`hooks/useGeolocation.ts`)**
- **GPS Integration**: Browser geolocation API
- **Permission Handling**: Graceful permission requests
- **Error Management**: User-friendly error messages
- **Auto-detection**: Automatic location for chat queries

### **Chat Session Management (`hooks/useChatSession.ts`)**
- **Session Persistence**: Maintain chat history
- **Location Integration**: Automatic location sharing
- **Message Management**: Send, receive, and display messages
- **Error Handling**: Robust error recovery

## 🔧 Configuration

### Frontend Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `http://localhost:8000` | Yes |
| `NEXT_PUBLIC_MAP_CENTER_LAT` | Default map center latitude | `3.1570` | No |
| `NEXT_PUBLIC_MAP_CENTER_LNG` | Default map center longitude | `101.7123` | No |
| `NEXT_PUBLIC_MAP_ZOOM` | Default map zoom level | `11` | No |
| `NEXT_PUBLIC_APP_NAME` | Application name | `McDonald's Malaysia Map` | No |
| `NEXT_PUBLIC_APP_DESCRIPTION` | App description for SEO | - | No |
| `NODE_ENV` | Environment mode | `development` | No |

### Map Configuration

The map is configured for Kuala Lumpur, Malaysia by default:
- **Center**: KLCC coordinates (3.1570, 101.7123)
- **Zoom**: City-level view (11)
- **Tiles**: CartoDB Voyager for clean appearance
- **Markers**: Custom McDonald's branded icons

### Chat Configuration

- **Auto-location**: Enabled by default
- **Session Management**: Automatic session creation
- **Message History**: Persisted during session
- **Enter to Send**: Enabled for better UX

## 🎨 Styling and Theming

### Tailwind CSS
The application uses Tailwind CSS for styling with custom McDonald's branding:

```css
/* Custom McDonald's colors */
.bg-mcd-red { background-color: #DA291C; }
.text-mcd-red { color: #DA291C; }
.bg-mcd-yellow { background-color: #FFC72C; }
```

### Component Styling
- **Clean Design**: Modern, minimal interface
- **Brand Colors**: Official McDonald's red and yellow
- **Responsive**: Mobile-first responsive design
- **Accessibility**: WCAG compliant color contrasts

## 🧪 Testing and Development

### Development Scripts
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
npm run lint:check

# Code formatting
npm run format
npm run format:check

# Bundle analysis
npm run analyze
```

### Manual Testing

#### 1. Map Functionality
- Load the application at http://localhost:3000
- Verify all McDonald's markers appear
- Test marker clicks and popups
- Check radius circles toggle
- Test outlet selection and clearing

#### 2. Location Services
- Allow location permission when prompted
- Verify automatic location detection
- Test manual location button
- Check location integration with chat

#### 3. Chatbot Functionality
- Open the floating chat interface
- Test message sending with Enter key
- Verify location-based queries work
- Check outlet card display in chat responses
- Test Waze button functionality

#### 4. Responsive Design
- Test on different screen sizes
- Verify mobile responsiveness
- Check touch interactions on mobile
- Test landscape/portrait orientations

## 🚨 Troubleshooting

### Common Issues

#### 1. Map Not Loading
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify environment variables
cat .env.local

# Check console for errors
# Open browser DevTools > Console
```

#### 2. Location Permission Issues
- **Chrome**: Settings > Privacy > Location
- **Firefox**: Settings > Privacy & Security > Permissions
- **Safari**: Preferences > Websites > Location
- **Edge**: Settings > Site permissions > Location

#### 3. Chat Not Working
```bash
# Verify backend API is running
curl http://localhost:8000/api/chat/sessions

# Check environment variables
echo $NEXT_PUBLIC_API_BASE_URL

# Check browser console for errors
```

#### 4. Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npm run type-check
```

### Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Fully Supported |
| Firefox | 88+ | ✅ Fully Supported |
| Safari | 14+ | ✅ Fully Supported |
| Edge | 90+ | ✅ Fully Supported |
| Mobile Safari | iOS 14+ | ✅ Fully Supported |
| Chrome Mobile | Android 90+ | ✅ Fully Supported |

### Performance Optimization

#### 1. Bundle Size
```bash
# Analyze bundle size
npm run analyze

# Check for large dependencies
npx bundle-analyzer .next/static/chunks/*.js
```

#### 2. Map Performance
- **Marker Clustering**: Automatically handled for large datasets
- **Lazy Loading**: Components loaded on demand
- **Memory Management**: Proper cleanup of map instances

#### 3. Chat Performance
- **Message Batching**: Efficient message rendering
- **Session Management**: Optimized state updates
- **API Caching**: Intelligent response caching

## 🔄 Development Workflow

### 1. Local Development
```bash
# Start backend (in backend directory)
cd ../backend
python main.py

# Start frontend (in frontend directory)
cd ../frontend
npm run dev
```

### 2. Adding New Features

#### New Chat Features
1. Add components in `src/components/chat/`
2. Update chat types in `src/types/chat.ts`
3. Extend chat service in `src/hooks/useChatSession.ts`

#### New Map Features
1. Extend `src/components/Map.tsx`
2. Add controls in `src/components/MapControls.tsx`
3. Update types in `src/types/index.ts`

#### New API Integration
1. Add service functions in `src/services/`
2. Create custom hooks in `src/hooks/`
3. Update TypeScript types

### 3. Code Quality
```bash
# Format code
npm run format

# Check linting
npm run lint

# Type checking
npm run type-check

# Run all checks
npm run lint && npm run type-check && npm run build
```

## 🚀 Production Deployment

### Build Optimization
```bash
# Production build
npm run build

# Start production server
npm start

# Or export static files
npm run build && npm run export
```

### Environment Variables for Production
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com
NEXT_PUBLIC_MAP_CENTER_LAT=3.1570
NEXT_PUBLIC_MAP_CENTER_LNG=101.7123
```

### Deployment Options

#### 1. Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### 2. Netlify
```bash
# Build command: npm run build
# Publish directory: out (if using export)
```

#### 3. Docker
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

## 📱 Mobile Experience

### Progressive Web App (PWA)
- **Installable**: Can be installed as a mobile app
- **Offline Capable**: Basic functionality works offline
- **Fast Loading**: Optimized for mobile networks
- **Native Feel**: App-like experience on mobile devices

### Mobile-Specific Features
- **Touch Gestures**: Optimized touch interactions
- **Responsive Design**: Adapts to all screen sizes
- **Location Services**: GPS integration for mobile
- **Performance**: Optimized for mobile devices

## 📊 Analytics and Monitoring

### Performance Monitoring
```bash
# Lighthouse audit
npm install -g lighthouse
lighthouse http://localhost:3000

# Core Web Vitals
# Check in browser DevTools > Lighthouse
```

### Error Monitoring
- **Error Boundary**: Catches and displays React errors
- **Console Logging**: Structured logging for debugging
- **User Feedback**: Error messages guide user actions

## 📞 Support

### Getting Help
1. **Check Console**: Browser DevTools for error messages
2. **Verify Backend**: Ensure backend API is running
3. **Main README**: See [project root README](../README.md) for main environment setup
4. **Check Environment**: Verify `.env.local` configuration
5. **Test Location**: Ensure location permissions are granted

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Test thoroughly: `npm run lint && npm run type-check && npm run build`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Enjoy exploring McDonald's outlets! 🍟🗺️** 