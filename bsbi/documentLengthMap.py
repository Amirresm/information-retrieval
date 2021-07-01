class DocumentLengthMap:

    def __init__(self):
       self.table = dict()
    
    def __len__(self):
        return len(self.table)

    def __getitem__(self, doc_id):
       if doc_id in self.table:
            return self.table[doc_id]
       else:
            raise LookupError("there no document with id %s", doc_id)

    def add(self, doc_id, length):
        self.table[doc_id] = length
    
    def get_average_length(self):
       total_length = 0
       for doc_length in self.table.values():
            total_length += doc_length
      
       average = total_length / len(self.table)
       return average