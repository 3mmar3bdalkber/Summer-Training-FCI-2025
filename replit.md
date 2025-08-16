# Overview

This is an Arabic e-commerce web application built with Flask that provides a product catalog and browsing experience. The application displays products in Arabic with RTL (right-to-left) layout support, featuring product listings, detailed views, search and filtering capabilities. The store focuses on electronics and accessories with a clean, modern interface optimized for Arabic-speaking users.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask's built-in rendering
- **UI Framework**: Bootstrap 5 RTL for responsive Arabic layout
- **Styling**: Custom CSS with Arabic font support (Cairo font family)
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript for interactive features and animations
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

## Backend Architecture
- **Web Framework**: Flask with modular route organization
- **Application Structure**: Single-file app configuration with separated route handlers
- **Data Layer**: In-memory Python dictionaries for product storage
- **Session Management**: Flask sessions with configurable secret key
- **Template Rendering**: Server-side rendering with Jinja2

## Data Storage
- **Storage Type**: In-memory data structures (Python dictionaries)
- **Product Schema**: Structured product data with fields for id, name, description, price, category, image, featured status, and stock availability
- **Data Access**: Direct dictionary manipulation with helper functions for CRUD operations

## Route Structure
- **Homepage**: Hero section with featured products display
- **Product Listing**: Filterable and searchable product catalog with category navigation
- **Product Details**: Individual product pages with related product suggestions
- **Navigation**: Breadcrumb support and active state management

## Internationalization
- **Language**: Arabic as primary language with RTL text direction
- **Layout**: Right-to-left layout support throughout the application
- **Typography**: Arabic-optimized fonts and text rendering

# External Dependencies

## Frontend Libraries
- **Bootstrap 5 RTL**: Responsive CSS framework with Arabic layout support
- **Font Awesome 6.4.0**: Icon library for UI elements
- **Google Fonts**: Cairo font family for Arabic text rendering

## Backend Dependencies
- **Flask**: Python web framework for application server
- **Jinja2**: Template engine (included with Flask)

## Development Tools
- **Static Assets**: CSS and JavaScript files served through Flask's static file handling
- **Environment Variables**: Configuration through environment variables for sensitive data like session secrets

## Placeholder Services
- **Image Hosting**: Currently using placeholder.com for product images
- **No Database**: Application uses in-memory storage, ready for database integration