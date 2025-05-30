import sys  #they enable us to import files outside cli/
import os

#fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database.session import sessionLocal
from models.client import Client
from models.job import Job

def create_job():
  db = sessionLocal() #creates a temporary connection to the database

  try:

    #list existing clients
    clients = db.query(Client).all()
    if not clients:
      print("No clients found. create clients first")
      return
    
    print("Available Clients:")
    for client in clients:
      print(f"{client.id}, {client.user.full_name} ({client.user.username})")


    client_id = int(input("Enter the ID of the client creating the job: "))
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:    #defensive programming
      print("Invalid client ID")
      return
    
    #job input
    title = input("Enter job title")
    description = input("Enter job description: ")
    budget = float(input("Enter job budget: "))

    job = Job(
      title = title,
      description = description,
      budget = budget,
      client = client  #setting client id automatically
    )

    db.add(job)
    db.commit()
    print(f"job {title} created successfully for client '{client}'")

#error handling incase anything goes wrong eg invalid input, DB error....
  except Exception as e:     
    db.rollback()
    print("Error creating the job:", e)


# close the db connection even if there was an error
  finally:
    db.close()

    #only run create_job if the script is run directly, not imported from another file

if __name__ == "__main__":
  create_job()
