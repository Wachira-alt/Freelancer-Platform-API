#import all tables here (This is WRONG AND WILL CAUSE CIRCULAR IMPORTS)
# from app.models import user
# from app.models import client
# from app.models import job
# from app.models import freelancer
# from app.models import Proposal


from . import user
from . import client
from . import freelancer
from . import job
from . import proposal
from . import hired_proposal
from .review import Review

