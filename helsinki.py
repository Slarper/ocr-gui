# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-zh")


en = """
China has expanded its share of global commercial services exports from 3 percent
in 200s to 5.4 percent in 2022, according to a report jointly released by
the World Bank Group and World Trade Organization earlier this week.
"""


ch  = pipe(en)

print(ch[0]['translation_text'])
