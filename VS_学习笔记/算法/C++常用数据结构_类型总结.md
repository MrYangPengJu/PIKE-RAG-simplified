## array数组
> &emsp;&emsp;内存空间为连续的一段地址，适用于提前已知所要存储的数据类型和数量、进行大量的查、改操作，不适用于含有大量交换、删除、增加数据的操作，该容器**无法动态改变大小**，所以说提前已知存储数据类型和数量。以下代码介绍了数组的初始化、赋值、遍历、获取大小、获取特定位置数据的方法。

```C++
#include<iostream>
#include<array>  // 头文件
using namespace std;

int main()
{
    array<int,10> myArray;  // 使用方法：array<类型,数量>

    for(int i=0;i<10;i++)  // 进行赋值
        myArray[i]=i;

    cout<<"遍历数据"<<endl;
    for(auto it = myArray.begin();it!=myArray.end();it++)
        cout<<*it<<'\t';

    cout<<"获取数组大小"<<endl;
    cout<<myArray.size()<<endl;
    
    cout<<"获得指定位置的值"<<endl;
    cout<<myArray[3]<<endl;
    return 0;
}

```

## queue队列
> &emsp;&emsp;该容器内存结构最好为链式结构，最知名的特点是先进先出，能动态调整大小，适用于包含大量增、删操作的情况，但不适用于含有大量查找操作的数据。以下代码介绍了队列初始化、赋值、弹出操作。

```C++
#include<iostream>
#include<queue>  // 头文件
using namespace std;
int main()
{
    queue<int> myQueue;  // 初始化
    for(int i=0;i<10;i++)
        myQueue.push(i);  // 添加数据

    while(!myQueue.empty())
    {
        cout<<myQueue.front()<<endl;  // 获取头部数据
        myQueue.pop();  // 弹出头部数据
    }
    return 0;
}

```
## deque 双向队列（double-ended queue）
> &emsp;&emsp;deque可以在队列的两端进行元素的插入和删除操作。deque的特点是可以在队列的两端进行元素的操作，并且可以高效地在队列的任意位置进行元素的插入和删除操作。常用方法如下：
```C++
push_back()//在队列的尾部插入元素。
emplace_front()//与push_front()的作用一样 
push_front()//在队列的头部插入元素。
emplace_back()//与push_back()的作用一样 
pop_back()//删除队列尾部的元素。
pop_front()//删除队列头部的元素。
back()//返回队列尾部元素的引用。
front()//返回队列头部元素的引用。
clear()//清空队列中的所有元素。
empty()//判断队列是否为空。
size()//返回队列中元素的个数。
begin()//返回头位置的迭代器
end()//返回尾+1位置的迭代器
rbegin()//返回逆头位置的迭代器 
rend()//返回逆尾-1位置的迭代器 
insert()//在指定位置插入元素 
erase()//在指定位置删除元素 
#include<iostream>
#include<deque>
using namespace std;
int main()
{
	deque<int> d; //定义一个数据类型为int的deque
	d.push_back(1); //向队列中加入元素1 
	d.push_back(2); //向队列中加入元素2
	d.push_back(3); //向队列中加入元素3
	d.push_back(4); //向队列中加入元素4
	cout<<"双端队列中现在的元素为："<<endl;
	for(int i=0;i<d.size();i++)
	{
		cout<<d[i]<<" ";
	}
	cout<<endl;
	d.pop_front();
	cout<<"弹出队首元素后，双端队列中现在的元素为："<<endl;
	for(int i=0;i<d.size();i++)
	{
		cout<<d[i]<<" ";
	}
	cout<<endl;
	d.pop_back();
	cout<<"弹出队尾元素后，双端队列中现在的元素为："<<endl;
	for(int i=0;i<d.size();i++)
	{
		cout<<d[i]<<" ";
	}
	cout<<endl;
	d.push_back(6);
	cout<<"在队尾添加元素6后，双端队列中现在的元素为："<<endl;
	for(int i=0;i<d.size();i++)
	{
		cout<<d[i]<<" ";
	}
	cout<<endl;
	d.push_front(8);
	cout<<"在队首添加元素8后，双端队列中现在的元素为："<<endl;
	for(int i=0;i<d.size();i++)
	{
		cout<<d[i]<<" ";
	}
}

```

## stack 栈
> &emsp;&emsp;栈在内存上可为连续或者链式，于队列相反的是它为先进后出，适用于压栈出栈操作，如可用于图的遍历、递归函数的改写等，以下代码介绍了栈的创始化、压栈、出栈等操作。
```C++
#include<iostream>
#include<stack>  // 头文件
using namespace std;
int main()
{
    stack<int> myStack;  // 初始化

    for(int i=0;i<10;i++)
        myStack.push(i);  // 压栈

    while(!myStack.empty())
    {
        cout<<myStack.top()<<endl;  // 取栈顶元素
        myStack.pop();  // 弹出栈顶元素
    }

    return 0;
}

```

## list 链表
> &emsp;&emsp;链表在内存结构上为链式结构，也就决定它可以动态增加，适用于包含大量增加、删除的应用，但不适用于包含大量查询的操作，图片介绍了链表的创建、添加数据、删除数据、获取数据等操作。

```C++
#include<iostream>
#include<list>  // 头文件
using namespace std;
int main()
{
    // 数组创建链表形式
    int num[] = {1,2,3,4,5};
    list<int> myList(num,num+sizeof(num)/sizeof(int));
    // list<A> listname(first, last);
    
    // 其他定义方法
    // list<A> listname;
    // list<A> listname(size);
    // list<A> listname(size,value);
    // list<A> listname(elselist);
    

    // 插入到指针所在位置前面
    auto it = myList.begin();
    for(int i=0;i<5;i++)
        myList.insert(it,i);

    // 遍历链表
    for(auto it = myList.begin();it!=myList.end();it++)
        cout<<*it<<'\t'<<endl;

    return 0;

}
```

## map
> &emsp;&emsp;map为关联式容器，提供一对一服务，每个关键字在容器中只能出现一次，适用于一对一服务。

```C++
#include<iostream>
#include<map>  // 头文件
using namespace std;
int main()
{
    map<char, int> myMap;  // 初始化
    myMap['a'] = 1;  // 赋值
    myMap.insert(pair<char,int>('b',2));  // 插入
    myMap.erase('a');  // 删除
    auto it = myMap.find('b');  // 查找
    cout<< it->first << '\t' << it->second <<endl;  // 获取key以及value

    return 0;
}

```

## set 集合
> &emsp;&emsp;set集合最大的特点是里面的元素按序排列不重复，图片演示集合初始化、插入、删除、查找等操作。
```C++
#include<iostream>
#include<set>  // 头文件
using namespace std;
int main()
{
    // 数组方式初始化
    int num[]={1,2,3,4,5};
    // num+sizeof(num/sizeof(int))计算元素个数
    set<int> mySet(num, num+sizeof(num/sizeof(int)));

    mySet.insert(6);  // 插入
    mySet.erase(2);  // 删除
    auto it = mySet.find(3);  // 查找

    cout<<*it<<endl;

    return 0;
}

```


## vector向量
> &emsp;&emsp;vector向量和array不同，它可以根据数据的大小而进行自动调整，图片仅展示初始化、插入、删除等操作。

```C++
#include<iostream>
#include<vector>  // 头文件
using namespace std;
int main()
{
    vector<int> myVector;出每个元素的初值为1
        // vector<int> a(b); //用b向量来创建a向量，整体复制性赋值
    // vector<int> a(10); //定义了10个整型元素的向量（尖括号中为元素类型名，它可以是任何合法的数据类型），但没有给出初值，其值是不确定的。
    // vector<int> a(10,1); //定义了10个整型元素的向量,且给出每个元素的初值为1
    // vector<int> a(b); //用b向量来创建a向量，整体复制性赋值
    // vector<int> a(b.begin(),b.begin+3); //定义了a值为b中第0个到第2个（共3个）元素
    // int b[7]={1,2,3,4,5,9,8};
    // vector<int> a(b,b+7); //从数组中获得初值

    // 压入
    for(int i=0;i<10;i++)
        myVector.push_back(i);

    // 遍历
    for(auto it = myVector.begin();it!=myVector.end();it++)
        cout<<*it<<endl;

    cout<<"获取数组大小"<<endl;
    cout<<myVector.size()<<endl;
    
    cout<<"获得指定位置的值"<<endl;
    cout<<myVector[3]<<endl;

    return 0;
}

// ------------------------------------------------------------------
//vector常用方法
    a.assign(b.begin(), b.begin()+3); //b为向量，将b的0~2个元素构成的向量赋给a
    a.assign(4,2); //向a分配4个元素，且每个元素为2（覆盖曾经的值）
    a.back(); //返回a的最后一个元素
    a.front(); //返回a的第一个元素
    a[i]; //返回a的第i个元素，当且仅当a[i]存在2013-12-07
    a.clear(); //清空a中的元素
    a.empty(); //判断a是否为空，空则返回ture,不空则返回false
    a.pop_back(); //删除a向量的最后一个元素
    a.erase(a.begin()+1,a.begin()+3); //删除a中第1个（从第0个算起）到第2个元素，也就是说删除的元素从a.begin()+1算起（包括它）一直到a.begin()+         3（不包括它）
    a.push_back(5); //在a的最后一个向量后插入一个元素，其值为5
    a.insert(a.begin()+1,5); //在a的第1个元素（从第0个算起）的位置插入数值5，如a为1,2,3,4，插入元素后为1,5,2,3,4
    a.insert(a.begin()+1,3,5); //在a的第1个元素（从第0个算起）的位置插入3个数，其值都为5
    a.insert(a.begin()+1,b+3,b+6); //b为数组，在a的第1个元素（从第0个算起）的位置插入b的第3个元素到第5个元素（不包括b+6），如b为1,2,3,4,5,9,8         ，插入元素后为1,4,5,9,2,3,4,5,9,8
    a.size(); //返回a中元素的个数；
    a.capacity(); //返回a在内存中总共可以容纳的元素个数
    a.resize(10); //将a的现有元素个数调至10个，多则删，少则补，其值随机
    a.resize(10,2); //将a的现有元素个数调至10个，多则删，少则补，其值为2
    a.reserve(100); //将a的容量（capacity）扩充至100，也就是说现在测试a.capacity();的时候返回值是100.这种操作只有在需要给a添加大量数据的时候才         显得有意义，因为这将避免内存多次容量扩充操作（当a的容量不足时电脑会自动扩容，当然这必然降低性能） 
    a.swap(b); //b为向量，将a中的元素和b中的元素进行整体性交换
    a == b; //b为向量，向量的比较操作还有!=,>=,<=,>,<
```


## string
> string的构造函数如下
```C++
string str：生成空字符串

string s(str)：生成字符串为str的复制品

string s(str, strbegin,strlen)：将字符串str中从下标strbegin开始、长度为strlen的部分作为字符串初值

string s(cstr, char_len)：以C_string类型cstr的前char_len个字符串作为字符串s的初值

string s(num ,c)：生成num个c字符的字符串

string s(str, stridx)：将字符串str中从下标stridx开始到字符串结束的位置作为字符串初值

eg:
    string str1;               //生成空字符串
    string str2("123456789");  //生成"1234456789"的复制品
    string str3("12345", 0, 3);//结果为"123"
    string str4("012345", 5);  //结果为"01234"
    string str5(5, '1');       //结果为"11111"
    string str6(str2, 2);      //结果为"3456789"
```
> string常用成员函数
```C++

1. size()和length()：返回string对象的字符个数，他们执行效果相同。

2. max_size()：返回string对象最多包含的字符数，超出会抛出length_error异常

3. capacity()：重新分配内存之前，string对象能包含的最大字符数

void test()
{
    string s("1234567");
    cout << "size=" << s.size() << endl;
    cout << "length=" << s.length() << endl;
    cout << "max_size=" << s.max_size() << endl;
    cout << "capacity=" << s.capacity() << endl;

}
```
> string字符串比较
```C++
1. C ++字符串支持常见的比较操作符（>,>=,<,<=,==,!=），甚至支持string与C-string的比较(如 str<”hello”)。 

在使用>,>=,<,<=这些操作符的时候是根据“当前字符特性”将字符按字典顺序进行逐一得 比较。字典排序靠前的字符小,
比较的顺序是从前向后比较，遇到不相等的字符就按这个位置上的两个字符的比较结果确定两个字符串的大小(前面减后面)
同时，string ("aaaa") <string("aaaaa")。    

2. 另一个功能强大的比较函数是成员函数compare()。他支持多参数处理，支持用索引值和长度定位子串来进行比较。 
  他返回一个整数来表示比较结果，返回值意义如下：0：相等 1：大于 -1：小于 (A的ASCII码是65，a的ASCII码是97)

void test()
{
    // (A的ASCII码是65，a的ASCII码是97)
    // 前面减去后面的ASCII码，>0返回1，<0返回-1，相同返回0
    string A("aBcd");
    string B("Abcd");
    string C("123456");
    string D("123dfg");

    // "aBcd" 和 "Abcd"比较------ a > A
    cout << "A.compare(B)：" << A.compare(B)<< endl;                          // 结果：1

    // "cd" 和 "Abcd"比较------- c > A
    cout << "A.compare(2, 3, B):" <<A.compare(2, 3, B)<< endl;                // 结果：1

    // "cd" 和 "cd"比较 
    cout << "A.compare(2, 3, B, 2, 3):" << A.compare(2, 3, B, 2, 3) << endl;  // 结果：0

    // 由结果看出来：0表示下标，3表示长度
    // "123" 和 "123"比较 
    cout << "C.compare(0, 3, D, 0, 3)" <<C.compare(0, 3, D, 0, 3) << endl;    // 结果：0

}
```
> string的插入：push_back() 和 insert()
```C++
void  test4()
{
    string s1;

    // 尾插一个字符
    s1.push_back('a');
    s1.push_back('b');
    s1.push_back('c');
    cout<<"s1:"<<s1<<endl; // s1:abc

    // insert(pos,char):在制定的位置pos前插入字符char
    s1.insert(s1.begin(),'1');
    cout<<"s1:"<<s1<<endl; // s1:1abc
}
```
> string拼接字符串：append() & + 操作符
```C++
void test5()
{
    // 方法一：append()
    string s1("abc");
    s1.append("def");
    cout<<"s1:"<<s1<<endl; // s1:abcdef

    // 方法二：+ 操作符
    string s2 = "abc";
    /*s2 += "def";*/
    string s3 = "def";
    s2 += s3.c_str();
    cout<<"s2:"<<s2<<endl; // s2:abcdef
}
```
> string的删除：erase()
```C++
    string s1 = "123456789";
    s1.erase(s1.begin()+1);              // 结果：13456789
    s1.erase(s1.begin()+1,s1.end()-2);   // 结果：189
    s1.erase(1,6);                       // 结果：189
```
> string的字符替换
```C++
1. string& replace(size_t pos, size_t n, const char *s);//将当前字符串从pos索引开始的n个字符，替换成字符串s
2. string& replace(size_t pos, size_t n, size_t n1, char c); //将当前字符串从pos索引开始的后n个字符，替换成n1个字符c
3. string& replace(iterator i1, iterator i2, const char* s);//将当前字符串[i1,i2)区间中的字符串替换为字符串s

void test()
{
    string s1("hello,world!");

    cout<<s1.size()<<endl;                     // 结果：12
    s1.replace(s1.size()-1 ,1 ,1,'.');           // 结果：hello,world.
    s1.replace(s1.size()-1 ,1 ,2,'.');           // 结果：hello,world..

    // 这里的6表示下标  5表示长度
    s1.replace(6,5,"girl");                    // 结果：hello,girl..
    s1.replace(6,0,"girl");                    // 结果：hello,girlgirl..
    // s1.begin(),s1.begin()+5 是左闭右开区间
    s1.replace(s1.begin(),s1.begin()+5,"boy"); // 结果：boy,girlgirl..
    cout<<s1<<endl;
}
```
> string的大小写转换：tolower()和toupper()函数
```C++
#include <iostream>
#include <string>
using namespace std;

int main()
{
    string s = "ABCDEFG";

    for( int i = 0; i < s.size(); i++ )
    {
        s[i] = tolower(s[i]);
    }

    cout<<s<<endl;
    return 0;
}
```
> string的查找：find
```C++
1. size_t find (constchar* s, size_t pos = 0) const;

  //在当前字符串的pos索引位置开始，查找子串s，返回找到的位置索引，

    -1表示查找不到子串

2. size_t find (charc, size_t pos = 0) const;

  //在当前字符串的pos索引位置开始，查找字符c，返回找到的位置索引，

    -1表示查找不到字符

3. size_t rfind (constchar* s, size_t pos = npos) const;

  //在当前字符串的pos索引位置开始，反向查找子串s，返回找到的位置索引，

    -1表示查找不到子串

4. size_t rfind (charc, size_t pos = npos) const;

  //在当前字符串的pos索引位置开始，反向查找字符c，返回找到的位置索引，-1表示查找不到字符

5. size_tfind_first_of (const char* s, size_t pos = 0) const;

  //在当前字符串的pos索引位置开始，查找子串s的字符，返回找到的位置索引，-1表示查找不到字符

6. size_tfind_first_not_of (const char* s, size_t pos = 0) const;

  //在当前字符串的pos索引位置开始，查找第一个不位于子串s的字符，返回找到的位置索引，-1表示查找不到字符

7. size_t find_last_of(const char* s, size_t pos = npos) const;

  //在当前字符串的pos索引位置开始，查找最后一个位于子串s的字符，返回找到的位置索引，-1表示查找不到字符

8. size_tfind_last_not_of (const char* s, size_t pos = npos) const;

 //在当前字符串的pos索引位置开始，查找最后一个不位于子串s的字符，返回找到的位置索引，-1表示查找不到子串

void test()
{
    string s("dog bird chicken bird cat");

    //字符串查找-----找到后返回首字母在字符串中的下标

    // 1. 查找一个字符串
    cout << s.find("chicken") << endl;        // 结果是：9

    // 2. 从下标为6开始找字符'i'，返回找到的第一个i的下标
    cout << s.find('i',6) << endl;            // 结果是：11

    // 3. 从字符串的末尾开始查找字符串，返回的还是首字母在字符串中的下标
    cout << s.rfind("chicken") << endl;       // 结果是：9

    // 4. 从字符串的末尾开始查找字符
    cout << s.rfind('i') << endl;             // 结果是：18-------因为是从末尾开始查找，所以返回第一次找到的字符

    // 5. 在该字符串中查找第一个属于字符串s的字符
    cout << s.find_first_of("13br98") << endl;  // 结果是：4---b

    // 6. 在该字符串中查找第一个不属于字符串s的字符------先匹配dog，然后bird匹配不到，所以打印4
    cout << s.find_first_not_of("hello dog 2006") << endl; // 结果是：4
    cout << s.find_first_not_of("dog bird 2006") << endl;  // 结果是：9

    // 7. 在该字符串最后中查找第一个属于字符串s的字符
    cout << s.find_last_of("13r98") << endl;               // 结果是：19

    // 8. 在该字符串最后中查找第一个不属于字符串s的字符------先匹配t--a---c，然后空格匹配不到，所以打印21
    cout << s.find_last_not_of("teac") << endl;            // 结果是：21

}
```
>  string的排序：sort(s.begin(),s.end())
```C++
#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

void test9()
{
    string s = "cdefba";
    sort(s.begin(),s.end());
    cout<<"s:"<<s<<endl;     // 结果：abcdef
}
```

> string的分割/截取字符串：strtok() & substr()
```C++
void test10()
{
    char str[] = "I,am,a,student; hello world!";

    const char *split = ",; !";
    char *p2 = strtok(str,split);
    while( p2 != NULL )
    {
        cout<<p2<<endl;
        p2 = strtok(NULL,split);
    }
}
void test11()
{
    string s1("0123456789");
    string s2 = s1.substr(2,5); // 结果：23456-----参数5表示：截取的字符串的长度
    cout<<s2<<endl;
}
```