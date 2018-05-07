class Student(object):
    def __init__(self,name,score):
        self._name = name
        self._score = score
    @property
    def score(self): 
        return self._score
    @score.setter 
    def score(self,score):  
        if not isinstance(score,int):
            raise ValueError("invalid score!!!")
        if score < 0 or score > 100:
            raise ValueError("score must be between [0,100]!!!") 
        self._score = score
    @property
    def name(self): 
        return self._name

s1 = Student("Lily", 90)
#s1.name = "Luly"
s1.score = 100
