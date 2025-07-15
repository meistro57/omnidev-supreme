# OmniDev Supreme Frontend

The unified web interface for the OmniDev Supreme AI development platform.

## Features

- **Monaco Editor Integration**: VS Code-style editor with syntax highlighting
- **Real-time Agent Dashboard**: Monitor all 29 integrated agents
- **Project Management**: Multi-project workspace support
- **Memory Explorer**: Search and visualize the knowledge graph
- **Task Management**: Create, assign, and monitor AI tasks
- **WebSocket Integration**: Real-time updates and communication

## Technology Stack

- **React 18** with TypeScript
- **Redux Toolkit** for state management
- **Monaco Editor** for code editing
- **Tailwind CSS** for styling
- **Vite** for build tooling
- **Socket.io** for real-time communication

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Architecture

- **Components**: Reusable UI components
- **Pages**: Route-based page components
- **Store**: Redux state management
- **Utils**: Shared utilities and helpers
- **Types**: TypeScript type definitions

## Monaco Editor Features

- Syntax highlighting for 20+ languages
- IntelliSense and autocomplete
- Multi-cursor editing
- Keyboard shortcuts
- Theme customization
- Real-time collaboration (coming soon)

## API Integration

The frontend communicates with the backend via:
- REST API for standard operations
- WebSocket for real-time updates
- GraphQL for complex queries (coming soon)

## Contributing

1. Follow the existing code style
2. Add TypeScript types for new features
3. Test components thoroughly
4. Update documentation as needed