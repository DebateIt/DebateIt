from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from .. import crud, schemas
from sklearn.metrics.pairwise import cosine_similarity
import numpy

from .. import crud, dependencies


router = APIRouter(prefix="/nlp")
model = SentenceTransformer("bert-base-nli-mean-tokens")


@router.post("/sentence_sim")
def sentence_sim(
    payload: schemas.SentSim, db: Session = Depends(dependencies.get_db)
) -> str:
    topics = crud.getAllTopics(db)
    sentence_embeddings = model.encode(topics)
    new_emb = model.encode([payload.new_topic])
    sims = cosine_similarity(new_emb, sentence_embeddings)
    highest = numpy.argmax(sims)
    # print(sims.shape)
    if sims[0, highest] < 0.8:
        return None
    else:
        return topics[highest]
