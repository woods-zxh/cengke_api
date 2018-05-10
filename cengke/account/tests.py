# from django.test import TestCase
#
# # Create your tests here.
#
# time1 = "周二:1-13周,每1周;11-13节"
#
# time2 = "周二:1-13周,每1周;11-13节,1区,5-404"
#
# time = {}
# def cut_time(time):
#     # 第一步切片
#
#     day_in_week=time.split(':',1)[0][1:]
#
#     start_end_week = time.split(':',1)[1].split(',',1)[0]
#
#     gap = time.split(':',1)[1].split(',',1)[1].split(';')[0][1::-2]
#
#     time2= time.split(':',1)[1].split(',',1)[1].split(';')[1]
#
#     start_end_time = time2.split(',',1)[0]
#     start_week = start_end_week.split("-", 1)[0]
#     end_week = start_end_week.split("-", 1)[1][:-1]
#     start_time = start_end_time.split("-", 1)[0]
#     end_time = start_end_time.split("-", 1)[1][:-1]
#
#     if len(time) > 24:
#             area = time2.split(',', 1)[1].split(',', 1)[0][:-1]
#             building_room = time2.split(',', 1)[1].split(',', 1)[1]
#             building = building_room.split("-",1)[0]
#             room = building_room.split("-",1)[1]
#     else:
#             area = 0
#             building = 0
#             room = 0
#
#     time_infor = {
#         "day_in_week": day_in_week,
#         "start_week": start_week,
#         "end_week": end_week,
#         "area": area,
#         "building": building,
#         "room": room,
#         "start_time": start_time,
#         "end_time": end_time,
#         "gap": gap,
#     }
#
#     # print(day_in_week)
#     # print(start_end_week)
#     # print(start_week)
#     # print(end_week)
#     # print(gap)
#     # print(start_end_time)
#     # print(start_time)
#     # print(end_time)
#     # print(area)
#     #
#     # print(building)
#     # print(room)
#     return time_infor
#

#
# cut_time(time2)
#
#
# dict = {"1":123,"2":123}
#
# # for key in dict:
# #     print(type(key))
# PATTERN = {u'〇': 0,
#            u'一': 1,
#            u'二': 2,
#            u'三': 3,
#            u'四': 4,
#            u'五': 5,
#            u'六': 6,
#            u'七': 7,
#            u'八': 8,
#            u'九': 9, }
#
# print(PATTERN['一'])
# # college=5?academic=21?subject=656
for x in range(0,4):
    print(x)
#
# 210.42.121.241/servlet/Svlt_QueryPlanLsn?csrftoken=b8af1004-17c2-3705-9711-68c52c1d17d4?college=5?academic=21?subject=656
#
#
# d8c1c033-6317-389c-a19a-a621d7220c21
#
# 5549139e-7f9e-3409-9db4-5d1527e4649c
