# E-COMMERCE SHOP (PrestaShop & Docker)

## Project Overview
This is an e-commerce project based on PrestaShop, integrated with automation tools (Scraping, QA) using Docker and WSL2.

## Team and Roles:  
| Member | Description  |
| ---- | --- |
| Karolina Glaza | DevOps: Git	Infrastructure, Repository, Coordination |
| Amila Amarasekara | Backend Developer:	API, Products, Payments, Carriers |
| Martyna Borkowska | Frontend Developer: UI, UX, Theming |
| Bartosz Lewczuk | Scraper:	Data Extraction, Data Cleaning |
| Taras Szulakiewicz | Tester:	Selenium, Tests|

## Environment Setup
The development environment has been pre-configured and exported as a .tar file under the distribution name 'Shop'. The database (MariaDB) is already installed. Prerequisites:
1. Docker Desktop installed and running.
2. WSL2 (Windows Subsystem for Linux 2) enabled.
3. The 'Shop' distribution must be imported from the .tar file.

Launch Steps:
Start WSL: Open Windows PowerShell and enter the Linux environment:
```bash
wsl -d Shop
```
Start Servers: In the Linux terminal, navigate to the config folder and run the containers:
```bash
cd ~/Shop/config_files_and_scripts
docker compose up -d
```
## Access Points:
### Store: 
http://localhost:8080

### Admin Panel: 
http://localhost:8080/[admin-folder-name] 

- [admin-folder-name]  is in store_source_code directory

NOTE: The environment is configured to run on HTTP. SSL enforcement was disabled in the database during setup.

## Directory Structure
| Folder | Description  |
| ---- | --- |
| tore_source_code | Full PrestaShop source code (PHP, Templates, Themes) |
| scraping_tool_source_code | Python scraping scripts and virtual environment |
| automatic_tests_source_code | Automated test scripts (Selenium) |
| scraping_results | Output files from the scraper |
| config_files_and_scripts | TDocker infrastructure files (docker-compose.yml) |

## Workflow and Branching

The project uses a **main** branch for releases and an **develop** branch for feature development.

### Main Branches:
- **`main`**: Production-ready version. Must always be stable. Merges from `develop` only.
- **`develop`**: Primary Integration Branch. All feature work is merged here for testing before release.

### Feature Branches:
Work must be done on branches created from `develop` and merged back into `develop`.

| Task Type | Prefix |
| :--- | :--- |
| **Frontend** | `feat/ui`|
| **Backend** | `feat/api`|
| **Scraping** | `feat/scrap`|
| **QA/Testing** | `feat/test`|
| **DevOps/Config** | `config`|



All code must be merged into `develop` via a Pull Request. Merges to `main` are only made after testing, during team meetings.
