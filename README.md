# E-Commerce Shop – Project Stage II (Docker Swarm Deployment)

## Project Overview
The project focuses on deploying a PrestaShop-based e-commerce platform onto a production Docker Swarm cluster. It integrates automated data initialization, external database connectivity, Google Analytics tracking, and a full CI/CD pipeline. The shop is inspired by [MOP SERWIS](https://mopserwis.pl/).

## Team & Responsibilities

| Member | Role | Key Deliverables (Stage II) |
|--------|------|----------------------------|
| Karolina Glaza | DevOps & Lead | Infrastructure, Git Repository, Deployment, CI/CD Pipeline, Resource limiting, Cache config |
| Bartosz Lewczuk | Data Architect | Data Extraction, Data Cleaning, Google Analytics integration (Destination & Banner Events |
| Martyna Borkowska | Frontend Dev | UI/UX, Theming ) |
| Amila Amarasekara | Backend Dev | API, Products, Payments, Carriers |
| Taras Shuliakevych | QA / Tester |  Selenium, Automated Tests, Selenium automation on Swarm, Acceptance testing |

## Key Technical Features

### 1. Infrastructure & Deployment (Docker Swarm)

- **Containerization**: Custom `Dockerfile` and `docker-compose.yml` optimized for a student cluster environment
- **Swarm Stack**: Deployed as a single stack following strict naming conventions and port mapping
- **Resource Management**: Strict limits applied per service (vCore and RAM) to ensure cluster stability
- **External Database**: Integration with a shared cluster database server

### 2. Automation & CI/CD

- **Automated Pipeline**: GitHub Actions/GitLab CI configured to build and push images to a public registry upon every `push` to the `main` branch
- **Database Auto-Initialization**: Custom scripts ensure the store is fully populated with products and settings immediately upon startup

### 3. Analytics & Performance

- **Google Analytics (GA4)**: Full integration tracking store history, order values, and user behavior
- **Conversion Goals**:
  - **Destination**: Successful user registration
  - **Event**: Banner interaction and "Add to Cart" for promotional products
- **Performance**: Server-side caching enabled to meet high-performance requirements

### 4. Quality Assurance

- **Automated Testing**: Selenium scripts updated to verify core functionalities (cart, registration, checkout) directly on the Swarm production environment

## Setup & Launch

### Local Development (WSL2) (Stage 1)

1. Ensure Docker Desktop and WSL2 are running
2. Navigate to `config_files_and_scripts`
3. Run `docker-compose up -d`
4. Access via `https://localhost:8443`

### Production (Cluster)

- The stack is managed via `docker stack deploy`
- Images are pulled from the public registry (configured in the CI/CD pipeline)

