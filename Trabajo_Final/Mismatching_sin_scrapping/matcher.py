# -----------------------------------------------------------
# Código para identificar y clasificar matching/mismatching
# -----------------------------------------------------------

from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def match_education_to_job(edu_row, job_row, threshold=0.7):
    sim = similarity(edu_row["title_norm"], job_row["title_norm"])
    return sim >= threshold, sim
