#include<bits/stdc++.h>
#include<windows.h>
using namespace std;


struct Data
{
    string lecture;
    string name;
    int time;
    string location;
}Database[1000];

int N,cur_time,cnt_hour;


bool cmp(Data &p,Data &q)
{
    if(p.time==q.time) return p.lecture<q.lecture;
    return p.time<q.time;
}


int main()
{
    freopen("input.txt","r",stdin);
    printf("�����ͺ��̽� ���� ������ �Է��ϼ���: ");
    scanf("%d",&N);

    if(N){
        for(int i=0;i<N;i++)
            cin>>Database[i].lecture>>Database[i].name>>Database[i].time>>Database[i].location;

        sort(Database,Database+N,cmp);

        printf("���� �ð��� �Է��ϼ���: ");
        scanf("%d",&cur_time);

        printf("��� �ð��� �Է��ϼ���: ");
        scanf("%d",&cnt_hour);

        int start=0;
        while(cnt_hour){
            int cnt=0;
            while(cnt<1){ /// 1�ʸ� 1�ð����� ������.
                Sleep(1000);
                cnt++;
            }

            for(int i=0;i<100;i++) printf("-");
            printf("\n���� �ð�: %d:00\n",cur_time);

            if(cur_time>Database[N-1].time) printf("\n������ �����ϴ�.");
            else{
                printf("\n���Ǹ�\t ����\t ���ǽð�    ���ǽ�\n");

                for(int i=start;i<N;i++)
                    if(Database[i].time>=cur_time){
                        cout<<Database[i].lecture<<'\t'<<Database[i].name<<'\t';
                        cout<<"  "<<Database[i].time<<":00"<<'\t'<<"     "<<Database[i].location<<'\n';
                    }
                    else if(i>start) start=i;
            }
            printf("\n");

            cur_time++;
            if(cur_time==24){ /// �Ϸ簡 �Ѿ��
                cur_time%=24;
                start=0;
            }

            cnt_hour--;
        }
    }
    else printf("������ ������ �����ϴ�.");

    return 0;
}
