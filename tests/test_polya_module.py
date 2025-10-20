import numpy as np
from src.polya import PolyaSequenceModel, build_prefix, continue_urn_once, sample_prior_once

def test_shapes_and_bounds():
    model = PolyaSequenceModel(alpha=3.0, base="uniform", rng=np.random.default_rng(0))
    pref = build_prefix(20, model)
    assert len(pref) == 20 and all(0<=x<=1 for x in pref)
    cont = continue_urn_once(pref, model, 200)
    assert len(cont) == 200 and min(cont) >= 0 and max(cont) <= 1
    prior = sample_prior_once(50, model)
    assert len(prior) == 50
