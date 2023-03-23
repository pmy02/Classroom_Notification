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
    printf("데이터베이스 행의 개수를 입력하세요: ");
    scanf("%d",&N);

    if(N){
        for(int i=0;i<N;i++)
            cin>>Database[i].lecture>>Database[i].name>>Database[i].time>>Database[i].location;

        sort(Database,Database+N,cmp);

        printf("현재 시간을 입력하세요: ");
        scanf("%d",&cur_time);

        printf("운영할 시간을 입력하세요: ");
        scanf("%d",&cnt_hour);

        int start=0;
        while(cnt_hour){
            int cnt=0;
            while(cnt<1){ /// 1초를 1시간으로 가정함.
                Sleep(1000);
                cnt++;
            }

            for(int i=0;i<100;i++) printf("-");
            printf("\n현재 시각: %d:00\n",cur_time);

            if(cur_time>Database[N-1].time) printf("\n수업이 없습니다.");
            else{
                printf("\n강의명\t 교수\t 강의시간    강의실\n");

                for(int i=start;i<N;i++)
                    if(Database[i].time>=cur_time){
                        cout<<Database[i].lecture<<'\t'<<Database[i].name<<'\t';
                        cout<<"  "<<Database[i].time<<":00"<<'\t'<<"     "<<Database[i].location<<'\n';
                    }
                    else if(i>start) start=i;
            }
            printf("\n");

            cur_time++;
            if(cur_time==24){ /// 하루가 넘어가면
                cur_time%=24;
                start=0;
            }

            cnt_hour--;
        }
    }
    else printf("오늘은 수업이 없습니다.");

    return 0;
}
