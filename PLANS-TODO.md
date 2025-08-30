# BearBlog to Personal CMS Transformation Plan

## Overview
Transform BearBlog from a multi-tenant blogging platform into a personal CMS that can be deployed by a single user, similar to WordPress. The goal is to create a self-hostable, single-user blogging platform.

## Current State Analysis
BearBlog is currently a hosted blogging platform with:
- Multi-user/multi-blog support
- Complex review and moderation system
- Heroku-based deployment
- Subdomain and custom domain routing
- Advanced analytics and tracking
- Staff/admin tools
- Discovery and search features
- Email subscription system
- User upgrade/subscription system

## Transformation Strategy
Convert the platform into a personal CMS by:
1. Removing multi-user functionality
2. Simplifying to single blog per installation
3. Removing platform-specific features (staff tools, discovery, etc.)
4. Adding self-deployment capabilities
5. Keeping core blogging functionality intact

## Detailed Transformation Steps

### Phase 1: Core Architecture Changes

#### 1.1 Remove Multi-User Authentication System
- Remove Django allauth integration
- Remove User and UserSettings models
- Remove authentication-related middleware
- Remove login/signup functionality
- Add optional admin authentication for personal use
- Remove user-related context processors

#### 1.2 Simplify Blog Model
- Remove user foreign key relationship
- Remove subdomain and domain fields
- Remove review/moderation fields (dodgy_score, reviewed, flagged, etc.)
- Remove upgrade-related fields
- Remove analytics tracking fields
- Keep core blog configuration (title, content, styles, etc.)
- Make blog a singleton model or remove entirely (embed in settings)

#### 1.3 Simplify Post Model
- Remove blog foreign key (single blog assumption)
- Remove discovery-related fields (make_discoverable, score, upvotes)
- Remove analytics fields (hits, shadow_votes)
- Keep core post functionality (title, content, publish status, etc.)
- Remove complex scoring algorithms

#### 1.4 Remove Review and Moderation System
- Remove PersistentStore model
- Remove all staff/admin views
- Remove dodgy content detection
- Remove flagging functionality
- Remove bulk review tools

### Phase 2: Views and Templates

#### 2.1 Simplify Blog Views
- Remove subdomain/custom domain routing logic
- Simplify home() view to single blog
- Remove multi-blog resolution functions
- Update post() view for single blog context

#### 2.2 Remove Staff/Admin Dashboard
- Delete staff.py views entirely
- Remove staff templates
- Remove staff URLs
- Remove admin passport functionality

#### 2.3 Simplify Dashboard
- Remove blog selection/listing
- Remove multi-blog management
- Simplify to single blog editing
- Remove upgrade/subscription features
- Keep core content management (posts, pages, media, styles)

#### 2.4 Remove Discovery Features
- Delete discover.py views
- Remove discover templates
- Remove search functionality
- Remove feed discovery

### Phase 3: Configuration and Deployment

#### 3.1 Remove Heroku-Specific Configuration
- Remove judoscale integration
- Remove Heroku Postgres configuration
- Remove environment variable dependencies
- Add local SQLite default configuration
- Remove Cloudflare integration
- Remove staging server configuration

#### 3.2 Add Self-Hosting Capabilities
- Create setup/installation script
- Add Docker configuration
- Add docker-compose.yml for easy deployment
- Create configuration file for blog settings
- Add database initialization scripts

#### 3.3 Simplify Settings
- Remove complex environment variables
- Add sensible defaults for personal use
- Simplify email configuration (optional)
- Remove Sentry integration
- Remove performance monitoring

### Phase 4: Dependencies and Features

#### 4.1 Clean Dependencies
- Remove allauth
- Remove judoscale
- Remove sentry-sdk
- Remove geoip2
- Remove psycopg2 (PostgreSQL specific)
- Keep core dependencies (Django, Pillow, mistune, etc.)
- Add any new dependencies needed for self-hosting

#### 4.2 Simplify Email System
- Remove complex subscription management
- Keep basic email functionality (optional)
- Remove Mailgun integration
- Add SMTP configuration for personal email

#### 4.3 Remove Analytics Complexity
- Remove Hit and Upvote models
- Remove analytics views
- Remove public analytics
- Remove complex tracking middleware
- Keep simple post statistics if needed

### Phase 5: Database and Migration

#### 5.1 Create Migration Scripts
- Generate new migrations for simplified models
- Create data migration scripts for existing data
- Add database initialization fixtures
- Create upgrade path documentation

#### 5.2 Update Templates
- Remove multi-blog template logic
- Update navigation and links
- Simplify dashboard templates
- Update base templates for single blog
- Add installation/setup templates

### Phase 6: Documentation and Testing

#### 6.1 Create Installation Documentation
- Comprehensive README with installation steps
- Configuration guide
- Deployment options (Docker, manual)
- Troubleshooting guide

#### 6.2 Add Configuration System
- Create config file for blog settings
- Add admin interface for settings
- Create setup wizard for first-time configuration

#### 6.3 Testing and Validation
- Test core blogging functionality
- Test media upload
- Test theme customization
- Test deployment scenarios
- Validate data migration

## Implementation Priority

### High Priority (Core Functionality)
1. Remove multi-user authentication
2. Simplify Blog and Post models
3. Remove staff/admin functionality
4. Simplify routing and views
5. Add Docker support
6. Create setup script

### Medium Priority (User Experience)
1. Remove discovery features
2. Simplify analytics
3. Clean dependencies
4. Update templates
5. Add configuration system

### Low Priority (Polish)
1. Remove complex email features
2. Add comprehensive documentation
3. Create migration scripts
4. Test deployment scenarios
5. Performance optimization

## File Changes Summary

### Files to Modify
- `blogs/models.py` - Major simplification
- `blogs/views/` - Remove staff, discovery, simplify blog/dashboard
- `blogs/urls.py` - Remove complex routing
- `conf/settings.py` - Simplify configuration
- `templates/` - Update for single blog
- `requirements.txt` - Clean dependencies

### Files to Remove
- `blogs/views/staff.py`
- `blogs/views/discover.py`
- `templates/staff/`
- `templates/discover.html`
- `architecture.md` (replace with personal CMS docs)
- Heroku-specific files (Procfile, etc.)

### Files to Add
- `setup.py` or installation script
- `docker-compose.yml`
- `Dockerfile`
- `config.json` or similar configuration file
- `INSTALL.md` or comprehensive installation guide
- Migration scripts

## Success Criteria
1. Single blog can be installed and configured
2. Core blogging functionality works (posts, pages, media)
3. Theme customization works
4. Easy deployment options (Docker/manual)
5. Clean, documented codebase
6. No platform-specific dependencies
7. Personal use optimized

## Timeline Estimate
- Phase 1: 2-3 days (core architecture)
- Phase 2: 2-3 days (views and templates)
- Phase 3: 1-2 days (configuration and deployment)
- Phase 4: 1 day (dependencies and features)
- Phase 5: 1-2 days (database and migration)
- Phase 6: 1-2 days (documentation and testing)

Total: 8-13 days for complete transformation
