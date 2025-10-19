import numpy as np
from src.dgps import sample_truth, cdf_truth, pdf_truth

def test_sample_truth_shape_and_center():
    n = 5000
    x = sample_truth(n, seed=123)
    assert x.shape == (n,)
    assert abs(x.mean()) < 0.1
    assert 0.8 < x.std(ddof=0) < 1.2

def test_cdf_pdf_at_zero():
    assert abs(cdf_truth(0.0) - 0.5) < 1e-12
    assert abs(pdf_truth(0.0) - (1.0/np.sqrt(2*np.pi))) < 1e-6
