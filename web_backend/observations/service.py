from .models import Observation
from db import SessionDep

def create_observation(session: SessionDep, observation: Observation) -> Observation:
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation
