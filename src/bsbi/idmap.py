class IdMap:
    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []
        
    def __len__(self):
        return len(self.id_to_str)
        
    def _get_str(self, i):
        return self.id_to_str[i]
        
    def _get_id(self, s):
        id = self.str_to_id.get(s)
        if id != None:
            return id
        index = len(self.id_to_str)
        self.id_to_str.append(s)
        self.str_to_id[s] = index
        return index
            
    def __getitem__(self, key):
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError
        
    def get(self, s):
        return self.str_to_id.get(s)
    
if __name__ == '__main__':
    testIdMap = IdMap()
    assert testIdMap['a'] == 0, "Unable to add a new string to the IdMap"
    assert testIdMap['bcd'] == 1, "Unable to add a new string to the IdMap"
    assert testIdMap['a'] == 0, "Unable to retrieve the id of an existing string"
    assert testIdMap[1] == 'bcd', "Unable to retrive the string corresponding to a\
                                    given id"
    try:
        testIdMap[2]
    except IndexError as e:
        assert True, "Doesn't throw an IndexError for out of range numeric ids"
    assert len(testIdMap) == 2