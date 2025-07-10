**labelimg报错IndexError: list index out of range**
> 原因：如1.jpg，属于类别1，但是labels中的class.txt文件中不存在类别1
> 检查是否删除了classes.txt文件，如果已删除，则需要重新建立并且给出类别classes