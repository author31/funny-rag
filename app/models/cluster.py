from pydantic import BaseModel

class ClusterModel(BaseModel):
    hn_cluster_idx: int
    question: str