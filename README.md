# Test-Driven To-Do List App

**Note:** This project is still under active development.

A Django-based to-do list application built using Test-Driven Development (TDD). The project combines unit and functional testing to guide design and implementation, and is containerised with Docker and deployed using Ansible for consistency across environments.

## Features

- Create and manage multiple to-do lists and items
- User authentication system
- Modular architecture using Django apps (`lists`, `accounts`)
- Unit tests for models, views, and forms
- Functional tests using Selenium for end-to-end validation
- Deployment automated via Ansible

## Technologies Used

- **Language & Framework**: Python, Django
- **Testing**: `unittest`, `Selenium`
- **Containerisation**: Docker
- **Deployment**: Ansible
- **Database**: SQLite (development)

## Directory Overview

```
src/
├── accounts/             # Handles user registration and login
├── lists/                # Core to-do list functionality and tests
├── functional_tests/     # Selenium-based functional tests
├── superlists/           # Django project settings and configuration
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS)
├── manage.py
infra/
├── deploy-playbook.yaml  # Ansible deployment playbook
├── env.j2                # Jinja2 environment config template
Dockerfile                # Docker image definition
```

## Live Demo

A live version of the app is available at:  
[http://superlists.dalesingh.co.uk](http://superlists.dalesingh.co.uk)
