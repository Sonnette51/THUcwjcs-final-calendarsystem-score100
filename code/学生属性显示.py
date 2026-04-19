class Student:
    def __init__(self, name, age, type):
        self.name = name
        self.age = age
        self.type = type

    def get_property(self, prop_name):
        if prop_name == "Name":
            return self.name
        elif prop_name == "Age":
            return str(self.age)
        elif prop_name == "Type":
            return self.type
        else:
            return self._get_extra_property(prop_name)

    def _get_extra_property(self, prop_name):
        return "none"


class Undergraduate(Student):
    def __init__(self, name, age, type, specialty):
        super().__init__(name, age, type)
        self.specialty = specialty

    def _get_extra_property(self, prop_name):
        if prop_name == "Specialty":
            return self.specialty
        return "none"

class Graduate(Student):
    def __init__(self, name, age, type, direction):
        super().__init__(name, age, type)
        self.direction = direction

    def _get_extra_property(self, prop_name):
        if prop_name == "Direction":
            return self.direction
        return "none"

N = int(input())
student_records = {}
    
for i in range(N):
    input_data=input().split()
    name = input_data[0]
    age = int(input_data[1])
    type_str = input_data[2]
    extra_info = input_data[3]
        
    if type_str == "Undergraduate":
        student = Undergraduate(name, age, type_str, extra_info)
    elif type_str == "Graduate":
        student = Graduate(name, age, type_str, extra_info)

    student_records[name] = student

        
M = int(input())

for i in range(M):
    input_data=input().split()
    query_name = input_data[0]
    query_property = input_data[1]
    
    if query_name not in student_records:
        print("none")
        continue
            
    student_obj = student_records[query_name]
        
    result = student_obj.get_property(query_property)
    print(result)
