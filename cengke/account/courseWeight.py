from course.models import AllCourses

def makeCourseWeight():
    for course in AllCourses.objects.all():

        if(course.type == "艺术与欣赏类"):
            course.art = 1.0
            print(course.art)
        elif(course.type == "交流与写作类"):
            course.communication = 1.0
        elif(course.type == "人文与社会类" ):
            course.society = 1.0
        elif(course.type == "中国与全球类"):
            course.internation  =1.0
        elif(course.type == "研究与领导类"):
            course.leader = 1.0
        elif(course.type =="自然与工程类"):
            course.science = 1.0
        elif(course.type == "数学与推理类"):
            course.logic = 1.0
        else:
            course.others =1.0
        course.save()