import parsivar

class DocNormalizer():
    
    def __init__(self):
        self.normalizer = parsivar.Normalizer(date_normalizing_needed=True,
                                              pinglish_conversion_needed=True,
                                              statistical_space_correction=False)
        self.tokenizer = parsivar.Tokenizer()
        self.stemmer = parsivar.FindStems()
        
    def normalize(self, text):
        transformed = text
        transformed = self.normalizer.normalize(transformed)
        transformed = self.stemmer.convert_to_stem(transformed)
        return transformed
    
    def query_tokenizer(self, query):
        return self.tokenizer.tokenize_words(self.normalize(query))