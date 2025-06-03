#import all tables here (This is WRONG AND WILL CAUSE CIRCULAR IMPORTS)
# from app.models import user
# from app.models import client
# from app.models import job
# from app.models import freelancer
# from app.models import Proposal


#IF THERE IS AN APP.MODELS
# from . import freelancer
# from . import job
# from . import proposal
# from . import hired_proposal
# from .review import Review

from models.user import User
from models.client import Client
from models.freelancer import Freelancer
from models.job import Job

from models.proposal import Proposal
from models.hired_proposal import HiredProposal

from models.project import Project
from models.freelancer_project import freelancer_project


from models.review import Review


