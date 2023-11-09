def funny(name="fun", last='not fun', **kwargs):
    print(name, last)


a = {'name': 'nah', 'ha': 'ha'}

funny(**a)