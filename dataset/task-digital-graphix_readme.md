# Task Digital Graphix

## Project Overview

Task Digital Graphix is a Next.js-based web application designed to showcase a digital agency's portfolio and services. This repository contains the source code for the application's React components, styles, and configuration files.

## Features

- **Responsive Design**: The application is built with a responsive design, ensuring a seamless user experience across various devices and screen sizes.
- **Customizable Components**: The repository includes a set of reusable React components, allowing for easy customization and extension of the application's functionality.
- **Internationalization Support**: The application is designed to support internationalization, enabling easy translation and localization of content.
- **SEO Optimization**: The repository includes best practices for SEO optimization, ensuring the application's content is easily discoverable by search engines.

## Tech Stack

- **Frontend**: Next.js (TypeScript)
- **State Management**: No external state management library used (relying on React Context API)
- **Styles**: Tailwind CSS (configured using PostCSS)
- **Build Tools**: Webpack, Babel
- **Testing Framework**: Jest
- **Type Checking**: TypeScript

## Architecture

The repository is organized into the following folders:

- **components**: Contains reusable React components for the application.
- **styles**: Holds global CSS styles and configuration files for Tailwind CSS.
- **pages**: Includes the main application page and other custom pages.
- **utils**: Contains utility functions and types used throughout the application.

### File Structure

```markdown
task-digital-graphix/
components/
BlogSection.tsx
CtaBanner.tsx
HelpSection.tsx
Hero.tsx
ProcessSection.tsx
ServicesSection.tsx
TestimonialSection.tsx
WhySection.tsx
globals.css
layout.tsx
next-env.d.ts
package-lock.json
package.json
page.tsx
tsconfig.json
```

### Installation and Setup

To set up the application, navigate to the repository root and run the following commands:

```bash
npm install
npm run build
npm run start
```

This will install the required dependencies, build the application, and start the development server.