#include <iostream>
#include <vector>
#include <cstring>
#include <fstream>

using std::cout;
using std::cin;
using std::vector;
using std::strlen;
using std::pair;
using std::ifstream;

ifstream f("date.in");

char matrice[100][100], cuv[101];
int n, start, final = 4, oldStart;
bool ok = 1;

int main() {
  cin >> cuv;
  cin >> n;
  cin >> start;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      f >> matrice[i][j];
    }
  }
  
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      cout << matrice[i][j] << " ";
    }
    cout << '\n';
  }

  int m = strlen(cuv);
  for (int i = 0; i < m && ok; ++i) {
    char currentChr = cuv[i];
    oldStart = start;
    for (int j = 0; j < n; ++j) {
      if (matrice[oldStart][j] == currentChr) {
        start = j;
      }
    }
    cout << start << " " << currentChr << '\n';
    if (oldStart == start) ok = 0;

  }
  cout << '\n';
  if (start != final) ok = 0;
  if (ok) cout << "ok";
  else cout << "nu";
}