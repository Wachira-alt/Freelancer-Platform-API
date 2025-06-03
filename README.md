# Freelancer Platform API

A CLI-based Freelancer Platform API implemented using Python, SQLAlchemy ORM, and SQLite (or your preferred database).  
This project simulates a real-world freelance job marketplace backend, including users, clients, freelancers, jobs, proposals, hired proposals, projects, and reviews.

---
## Features

- Create and manage Users, Clients, and Freelancers
- Post Jobs and submit Proposals
- Manage Hired Proposals and convert them into Projects
- Assign Freelancers to Projects (many-to-many relationship)
- Leave Reviews from Clients to Freelancers
- Fully relational database support with SQLAlchemy ORM
- SQLite database backend for easy local development
- Designed for step-by-step CLI-driven workflows

---

## Technologies

- Python 3.9+  
- SQLAlchemy ORM  
- SQLite (default; easily configurable for other DBs)  
- CLI input handling  

---

## Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/freelancer-platform-api.git
   cd freelancer-platform-api

2. Create and activate a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Initialize the database (create tables):

## Usage
Run the CLI application and follow prompts:

python main.py

Available CLI commands:
create_user - Create new client or freelancer user

- post_job - Client posts a job

- submit_proposal - Freelancer submits a proposal for a job

- start_project - Start a project from a hired proposal

- leave_review - Client leaves a review for a freelancer

- You can integrate the CLI commands in a main interactive loop or call individually.

## Project Structure
.
├── app/                   # Application models
│   ├── __init__.py
│   ├── client.py
│   ├── freelancer.py
│   ├── hired_proposal.py
│   ├── job.py
│   ├── proposal.py
│   ├── project.py
│   ├── review.py
│   ├── user.py
│   └── freelancer_project.py    # association table
├── cli/                   # CLI commands and interface
│   └── cli.py
├── database/              # Database setup
│   ├── base.py            # Base model and metadata
│   └── session.py         # Database session and engine
├── migrations/            # Database migration scripts
├── seeds/                 # Seed data scripts/files
├── app.db                 # SQLite database file
├── config.py              # Configuration (e.g., DB URL, settings)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

## Database Models & Relationships

- User (one-to-one) Client or Freelancer

- Client (one-to-many) Jobs

- Job (one-to-many) Proposals

- Proposal (many-to-one) Freelancer and Job

- Hired Proposal (one-to-one) Job and Proposal

- Project (one-to-one) Job, (many-to-many) Freelancers

- Review (many-to-one) Client and Freelancer





## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, features, or improvements.