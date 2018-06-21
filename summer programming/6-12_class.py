# i = 0
# while i < 10:
#     print(i,end=" ")
#     i += 1
# print()
#
# i = 0
# while True:
#     print(i, end=' ')
#     if i >= 9:
#         break
#     i += 1
# # print()
#
# for i in range(10):
#     print(i, end = ' ')
# print()

while True:
    try:
        a = float(input('give me a number.'))
        b = float(input('give me another number.'))
        print('the sum is', a+b)
        break
    except ValueError:
        print('You entered something terrible')
    except KeyboardInterrupt:
        print('you must be sick of this program')
        break

# print('the sum is', a+b)
