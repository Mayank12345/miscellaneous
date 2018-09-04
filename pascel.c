#include<stdio.h>
void fun(int);
int fact(int q);
int main()
{
	int b;
	printf("how many level of pascal table you want to print? ");
	scanf("%d",&b);
		fun(b);
	return 0;
}
void fun(int n)
{	
	static int r=0,flag=0;
	int factorial=0,t=0;
	while(t<=n)
	{
		factorial=fact(n)/(fact(t)*fact(n-t));
		if(flag==1)
		{
		printf("%d ",factorial);
		}
		t++;
	}
	
		flag=1;
	t=r;
	printf("\n");
	while(r<=n)
		fun(r++);
}
int fact(int q)
{
	if(q==0)
		return 1;
	return q*fact(q-1);
}
