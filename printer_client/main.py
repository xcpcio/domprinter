import os
import time
import requests
import json
import typst
import subprocess

import constants

HEADERS = {'content-type': 'application/json'}

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = os.path.join(CUR_DIR, "output")

BASE_URL = os.getenv(
    "BASE_URL", "http://username:password@localhost:8080/print-task")


def fetch():
    local_url = BASE_URL + "?TaskState=1&LimitTaskNum=32"
    resp = requests.get(local_url, headers=HEADERS, verify=False, timeout=10)

    if resp.status_code != 200:
        raise Exception(
            "fetch error. [status_code={}]".format(resp.status_code))

    return json.loads(resp.text)


def done(task_id):
    resp = requests.patch(
        BASE_URL, {"TaskState": 2, "PrintTaskIDList": [task_id]}, verify=False)

    if resp.status_code != 200:
        raise Exception(
            "done error. [task_id={}] [status_code={}]".format(task_id, resp.status_code))

    return resp


def ensure_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def handle_print_task(task):
    try:
        submit_time = task["SubmitTime"]
        user_name = task["UserName"]
        team_name = task["TeamName"]
        team_id = task["TeamID"]
        location = task["Location"]
        language = task["Language"]
        # language = "plaintext"
        filename = task["FileName"]
        source_code = task["SourceCode"]
        print_task_id = task["PrintTaskID"]
        task_state = task["TaskState"]

        if len(team_name) == 0:
            team_name = "无"

        if len(location) == 0:
            location = "无"

        print("handle print task. [print_task_id={}] [task_state={}] [submit_time={}] [user_name={}] [team_name={}] [team_id={}] [location={}] [language={}] [filename={}]".format(
            print_task_id, task_state, submit_time, user_name, team_name, team_id, location, language, filename))

        build_dir = os.path.join(OUTPUT_PATH, str(print_task_id))
        ensure_dir(build_dir)

        typst_path = os.path.join(build_dir, "main.typst")
        pdf_path = os.path.join(build_dir, "main.pdf")
        code_file_name = "main.{}".format(language)
        code_file_path = os.path.join(build_dir, code_file_name)
        with open(code_file_path, "w") as f:
            f.write(source_code)

        header = """座位：{}
队伍：{}
提交时间：{}

""".format(location, team_name, submit_time)

        with open(typst_path, "w") as f:
            f.write(constants.TYPST_CONFIG %
                    (print_task_id, team_name, location, filename, language, code_file_name, header))

        typst.compile(typst_path, output=pdf_path)

        # cmd = "lp -o charset=UTF-8 -o print-quality=5 -P 1-16 {}".format(
        #     pdf_path)
        # subprocess.run(cmd, shell=True)

        # done(print_task_id)
    except Exception as e:
        print("handle print task error. [error={}]".format(e))


def init():
    ensure_dir(OUTPUT_PATH)


def main():
    init()

    # while True:
    #     try:
    #         r = fetch()
    #         r = r["PrintTaskList"]
    #         for task in r:
    #             handle_print_task(task)
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         time.sleep(1)

    # submit_time = task["SubmitTime"]
    # user_name = task["UserName"]
    # team_name = task["TeamName"]
    # team_id = task["TeamID"]
    # location = task["Location"]
    # language = task["Language"]
    # # language = "plaintext"
    # filename = task["FileName"]
    # source_code = task["SourceCode"]
    # print_task_id = task["PrintTaskID"]
    # task_state = task["TaskState"]

    task = {
        "SubmitTime": "",
        "UserName": "",
        "TeamName": "",
        "TeamID": "",
        "Location": "",
        "Language": "cpp",
        "FileName": "",
        "SourceCode":
        """//这回只花了114514min就打完了。
//真好。记得多手造几组。ACM拍什么拍。
#pragma GCC optimize("Ofast")
#pragma GCC target("popcnt","sse3","sse2","sse","avx","sse4","sse4.1","sse4.2","ssse3","f16c","fma","avx2","xop","fma4")
#pragma GCC optimize("inline","fast-math","unroll-loops","no-stack-protector")
#include "bits/stdc++.h"
#include <immintrin.h>
using namespace std;
template<class T1, class T2> istream &operator>>(istream &cin, pair<T1, T2> &a) { return cin>>a.first>>a.second; }
template<class T1> istream &operator>>(istream &cin, vector<T1> &a) { for (auto &x:a) cin>>x; return cin; }
template<class T1> istream &operator>>(istream &cin, valarray<T1> &a) { for (auto &x:a) cin>>x; return cin; }
template<class T1, class T2> ostream &operator<<(ostream &cout, const pair<T1, T2> &a) { return cout<<a.first<<' '<<a.second; }
template<class T1, class T2> ostream &operator<<(ostream &cout, const vector<pair<T1, T2>> &a) { for (auto &x:a) cout<<x<<'\n'; return cout; }
template<class T1> ostream &operator<<(ostream &cout, const vector<T1> &a) { int n=a.size(); if (!n) return cout; cout<<a[0]; for (int i=1; i<n; i++) cout<<' '<<a[i]; return cout; }
template<class T1> ostream &operator<<(ostream &cout, const valarray<T1> &a) { int n=a.size(); if (!n) return cout; cout<<a[0]; for (int i=1; i<n; i++) cout<<' '<<a[i]; return cout; }
template<class T1> ostream &operator<<(ostream &cout, const vector<valarray<T1>> &a) { int n=a.size(); if (!n) return cout; cout<<a[0]; for (int i=1; i<n; i++) cout<<'\n'<<a[i]; return cout; }
template<class T1> ostream &operator<<(ostream &cout, const vector<vector<T1>> &a) { int n=a.size(); if (!n) return cout; cout<<a[0]; for (int i=1; i<n; i++) cout<<'\n'<<a[i]; return cout; }
template<class T1, class T2> bool cmin(T1 &x, const T2 &y) { if (y<x) { x=y; return 1; } return 0; }
template<class T1, class T2> bool cmax(T1 &x, const T2 &y) { if (x<y) { x=y; return 1; } return 0; }
template<class T1> vector<T1> range(T1 l, T1 r, T1 step=1) { assert(step>0); int n=(r-l+step-1)/step, i; vector<T1> res(n); for (i=0; i<n; i++) res[i]=l+step*i; return res; }
template<class T1> basic_string<T1> operator*(const basic_string<T1> &s, int m) { auto r=s; m*=s.size(); r.resize(m); for (int i=s.size(); i<m; i++) r[i]=r[i-s.size()]; return r; }
#if !defined(ONLINE_JUDGE)&&defined(LOCAL)
#include "my_header\debug.h"
#else
#define dbg(...) ;
#define dbgn(...) ;
#endif
typedef unsigned ui;
typedef long double db;
typedef unsigned long long ll;
#define all(x) (x).begin(),(x).end()
const int B=1792, N=1e6;
const int Len=(B/64)+(B%64!=0);
const int m63=(1<<6)-1;
struct my_bit
{
	// ll v[Len];
	__m256i V[Len/4];
	void reset()
	{
		V[0]=_mm256_set_epi64x(0, 0, 0, 0);
		V[1]=_mm256_set_epi64x(0, 0, 0, 0);
		V[2]=_mm256_set_epi64x(0, 0, 0, 0);
		V[3]=_mm256_set_epi64x(0, 0, 0, 0);
		V[4]=_mm256_set_epi64x(0, 0, 0, 0);
		V[5]=_mm256_set_epi64x(0, 0, 0, 0);
		V[6]=_mm256_set_epi64x(0, 0, 0, 0);
	}
	void set(int u)
	{
		switch (u>>6&3)
		{
		case 0:
			V[u>>8]|=_mm256_set_epi64x(1ull<<(u&63), 0, 0, 0);
			break;
		case 1:
			V[u>>8]|=_mm256_set_epi64x(0, 1ull<<(u&63), 0, 0);
			break;
		case 2:
			V[u>>8]|=_mm256_set_epi64x(0, 0, 1ull<<(u&63), 0);
			break;
		case 3:
			V[u>>8]|=_mm256_set_epi64x(0, 0, 0, 1ull<<(u&63));
			break;
		}
			// v[u>>6]|=(1ull<<(u&63));
	}
	void operator |= (const my_bit &B)
	{
		V[0]|=B.V[0];
		V[1]|=B.V[1];
		V[2]|=B.V[2];
		V[3]|=B.V[3];
		V[4]|=B.V[4];
		V[5]|=B.V[5];
		V[6]|=B.V[6];
		// V[7]|=B.V[7];
		// V[8]|=B.V[8];
		// V[9]|=B.V[9];
		// V[10]|=B.V[10];
		// V[11]|=B.V[11];
		// V[12]|=B.V[12];
		// V[13]|=B.V[13];
		// V[14]|=B.V[14];
		// V[15]|=B.V[15];
		// V[16]|=B.V[16];
		// V[17]|=B.V[17];
		// V[18]|=B.V[18];
		// V[19]|=B.V[19];
		// V[20]|=B.V[20];
		// V[21]|=B.V[21];
		// V[22]|=B.V[22];
		// V[23]|=B.V[23];
	}
	int count()
	{
		return
			__builtin_popcountll(((ll *)&(V[0]))[0])+__builtin_popcountll(((ll *)&(V[0]))[1])
			+__builtin_popcountll(((ll *)&(V[0]))[2])+__builtin_popcountll(((ll *)&(V[0]))[3])
			+__builtin_popcountll(((ll *)&(V[1]))[0])+__builtin_popcountll(((ll *)&(V[1]))[1])
			+__builtin_popcountll(((ll *)&(V[1]))[2])+__builtin_popcountll(((ll *)&(V[1]))[3])
			+__builtin_popcountll(((ll *)&(V[2]))[0])+__builtin_popcountll(((ll *)&(V[2]))[1])
			+__builtin_popcountll(((ll *)&(V[2]))[2])+__builtin_popcountll(((ll *)&(V[2]))[3])
			+__builtin_popcountll(((ll *)&(V[3]))[0])+__builtin_popcountll(((ll *)&(V[3]))[1])
			+__builtin_popcountll(((ll *)&(V[3]))[2])+__builtin_popcountll(((ll *)&(V[3]))[3])
			+__builtin_popcountll(((ll *)&(V[4]))[0])+__builtin_popcountll(((ll *)&(V[4]))[1])
			+__builtin_popcountll(((ll *)&(V[4]))[2])+__builtin_popcountll(((ll *)&(V[4]))[3])
			+__builtin_popcountll(((ll *)&(V[5]))[0])+__builtin_popcountll(((ll *)&(V[5]))[1])
			+__builtin_popcountll(((ll *)&(V[5]))[2])+__builtin_popcountll(((ll *)&(V[5]))[3])
			+__builtin_popcountll(((ll *)&(V[6]))[0])+__builtin_popcountll(((ll *)&(V[6]))[1])
			+__builtin_popcountll(((ll *)&(V[6]))[2])+__builtin_popcountll(((ll *)&(V[6]))[3]);
		// int ans=0;
		// return __builtin_popcountll(v[0])
		// 	+__builtin_popcountll(v[1])
		// 	+__builtin_popcountll(v[2])
		// 	+__builtin_popcountll(v[3])
		// 	+__builtin_popcountll(v[4])
		// 	+__builtin_popcountll(v[5])
		// 	+__builtin_popcountll(v[6])
		// 	+__builtin_popcountll(v[7])
		// 	+__builtin_popcountll(v[8])
		// 	+__builtin_popcountll(v[9])
		// 	+__builtin_popcountll(v[10])
		// 	+__builtin_popcountll(v[11])
		// 	+__builtin_popcountll(v[12])
		// 	+__builtin_popcountll(v[13])
		// 	+__builtin_popcountll(v[14])
		// 	+__builtin_popcountll(v[15])
		// 	+__builtin_popcountll(v[16])
		// 	+__builtin_popcountll(v[17])
		// 	+__builtin_popcountll(v[18])
		// 	+__builtin_popcountll(v[19])
		// 	+__builtin_popcountll(v[20])
		// 	+__builtin_popcountll(v[21])
		// 	+__builtin_popcountll(v[22])
		// 	+__builtin_popcountll(v[23]);
			// return ans;
	}
}r[N];
int ans[N], cnt[N], tr[N], mn[N], cur[N], L[N], R[N], e[N+1];
pair<int, int> eg[N];
class fast_iostream
{
private:
	const int MAXBF=1<<21; FILE *inf, *ouf;
	char *inbuf, *inst, *ined;
	char *oubuf, *oust, *oued;
	inline void _flush() { fwrite(oubuf, 1, oued-oust, ouf); }
	inline char _getchar()
	{
		if (inst==ined) inst=inbuf, ined=inbuf+fread(inbuf, 1, MAXBF, inf);
		return inst==ined?EOF:*inst++;
	}
	inline void _putchar(char c)
	{
		if (oued==oust+MAXBF) _flush(), oued=oubuf;
		*oued++=c;
	}
public:
	fast_iostream(FILE *_inf=stdin, FILE *_ouf=stdout)
		:inbuf(new char[MAXBF]), inf(_inf), inst(inbuf), ined(inbuf),
		oubuf(new char[MAXBF]), ouf(_ouf), oust(oubuf), oued(oubuf)
	{ }
	~fast_iostream() { _flush(); delete inbuf; delete oubuf; }
	template <typename Int>
	fast_iostream &operator >> (Int &n)
	{
		static char c;
		while ((c=_getchar())<'0'||c>'9'); n=c-'0';
		while ((c=_getchar())>='0'&&c<='9') n=n*10+c-'0';
		return *this;
	}
	template <typename Int>
	fast_iostream &operator << (Int   n)
	{
		static char S[20]; int t=0;
		do { S[t++]='0'+n%10, n/=10; } while (n);
		for (int i=0; i<t; ++i) _putchar(S[t-i-1]);
		return *this;
	}
	fast_iostream &operator << (char  c) { _putchar(c);    return *this; }
	fast_iostream &operator << (const char *s)
	{
		for (int i=0; s[i]; ++i) _putchar(s[i]); return *this;
	}
}fio;//unsigned
int main()
{
	register int n, m, i, j, k, flg, id, cc, v;
	fio>>n>>m;
	memset(mn, 0x3f, sizeof mn);
	for (i=0; i<m; i++)
	{
		int u, v;
		fio>>u>>v; --u; --v;
		eg[i]={u, v};
		cmin(mn[v], u);
	}
	sort(eg, eg+m);
	m=unique(eg, eg+m)-eg;
	for (i=j=0; i<n; i++)
	{
		L[i]=R[i]=j;
		while (j<m&&eg[j].first==i) e[j++]=eg[j].second;
	}
	memcpy(cur, mn, min(j+B, n)*sizeof cur[0]);
	e[j]=-1;
	for (j=0; j<n; j+=B)
	{
		int sz=0;
		for (i=j; i<n&&i<j+B; i++)
		{
			r[i].set(i-j), tr[i]=i;
		}
		for (--i; i>=j; --i)
		{
			while (eg[R[i]].first==i&&e[R[i]]<j+B) ++R[i];
			flg=0, id=0;
			for (k=L[i]; k<R[i]; ++k) if (cnt[e[k]]) r[i]|=r[e[k]], ++flg, id=e[k];
			if (flg<=1)
			{
				ans[i]+=(cnt[i]=1+flg*cnt[id]);
				continue;
			}
			ans[i]+=(cnt[i]=r[i].count());
		}
		for (; i>=0; --i)
		{
			while (eg[R[i]].first==i&&e[R[i]]<j+B) ++R[i];
			cnt[i]=0;
			cc=0;
			for (k=L[i]; k<R[i]; k++) if (cnt[e[k]]&&++cc==2) break;
			if (cc==1)
			{
				for (k=L[i]; k<R[i]; k++) if (cnt[e[k]])
				{
					cnt[i]=cnt[e[k]];
					tr[i]=tr[e[k]];
					cmin(cur[tr[i]], cur[i]);
					break;
				}
			}
			else if (cc>=2)
			{
				id=i;
				for (k=L[i]; k<R[i]; k++) if (cnt[e[k]]&&cur[tr[e[k]]]==i) { id=e[k]; break; }
				if (id==i)
				{
					tr[i]=i;
					for (k=L[i]; k<R[i]; k++) if (cnt[e[k]]) break;
					r[i]=r[tr[e[k]]];
					for (++k; k<R[i]; k++)
					{
						v=e[k];
						if (cnt[v]) r[i]|=r[tr[v]];
					}
					cnt[i]=r[i].count();
				}
				else
				{
					tr[i]=tr[id];
					for (k=L[i]; k<R[i]; k++)
					{
						v=e[k];
						if (v!=id&&cnt[v]) r[tr[i]]|=r[tr[v]];
					}
					cnt[i]=r[tr[i]].count();
					cmin(cur[tr[i]], cur[i]);
				}
			}
			ans[i]+=cnt[i];
		}
	}
	for (i=0; i<n; i++) fio<<ans[i]<<' ';
}
""",
        "PrintTaskID": "81",
        "TaskState": "",
    }

    handle_print_task(task)


if __name__ == "__main__":
    main()
