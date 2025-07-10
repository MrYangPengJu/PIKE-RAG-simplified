### qsort
* 头文件：#include<stdlib.h>
* 参数：
  1. 数组名
  2. 元素个数（从前往后计算）
  3. 数组元素所占字节（int，double，char等所占字节）
  4. 排序原则（递增，递减，奇偶交叉等）
> int cmp(const void *a,const void *b) {
	return \*(int\*)a-\*(int\*)b;
}
qsort(num, n, sizeof(int), cmp);
* cmp函数(排序原则)
> 通过cmp返回的参数来确定排序规则，需要注意的是：cmp函数的参数需要以const void \*a,const void \*b的形式来定义，表示a和b的类型是未确定的，在return中进行强制类型转换为int型。\*(int\*)a-\*(int\*)b表示以递增顺序，若想以递减只需将a和b换位。
* 对于不同类型的数组排序，qsort函数的格式都是相同的，唯一不同在于cmp函数中的返回值类型。

```C++
// int 型
int cmp(const void *a,const void *b) {
	return *(int*)a-*(int*)b;
}

// 浮点型
int cmp(const void *a,const void *b) {
	return *(double*)a>*(double*)b?1:-1;
}
// 需要注意浮点数会存在精度损失的问题，
// 所以我们需要通过比较，来返回1或-1，以确定是增序还是降序。

// 结构体
struct node{
	int i;
	double j;
	char k;
};
int cmp(const void *a,const void *b) {
	return (*(node*)a).i-(*(node*)b).i;
}

// 若是要逐级比较，只需增加判断即可。
```

**以下是一个使用用例**
```C++
#include<stdio.h>
#include<stdlib.h>
int cmp(const void *a,const void *b) {
	return *(int*)a-*(int*)b;
}
int main() {
	int n,i;
	scanf("%d",&n);
	int time[n];
	for(i=0; i<n; i++) {
		scanf("%d",&time[i]);
	}
	qsort(time,n,sizeof(int),cmp);
	for(i=0;i<n;i++){
		printf("%d ",time[i]);
	}
	return 0;
}
```




