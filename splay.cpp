#include <bits/stdc++.h>
using namespace std;


struct Node {
    int key;
    Node *l, *r, *p;
    Node(int k): key(k), l(nullptr), r(nullptr), p(nullptr) {}
};

void rotate(Node* x) {
    Node* p = x->p;
    Node* g = p->p;
    if (p->l == x) {
        p->l = x->r;
        if (x->r) x->r->p = p;
        x->r = p;
    } else {
        p->r = x->l;
        if (x->l) x->l->p = p;
        x->l = p;
    }
    p->p = x;
    x->p = g;
    if (g) {
        if (g->l == p) g->l = x;
        else g->r = x;
    }
}

void splay(Node*& root, Node* x) {
    while (x->p) {
        Node* p = x->p;
        Node* g = p->p;
        if (!g) rotate(x);
        else if ((g->l==p) == (p->l==x)) { rotate(p); rotate(x); }
        else { rotate(x); rotate(x); }
    }
    root = x;
}

Node* bst_insert(Node* root, int key) {
    if (!root) return new Node(key);
    Node* cur = root, *p = nullptr;
    while (cur) {
        p = cur;
        if (key < cur->key) cur = cur->l;
        else if (key > cur->key) cur = cur->r;
        else { splay(root, cur); return root; }
    }
    Node* node = new Node(key);
    node->p = p;
    if (key < p->key) p->l = node;
    else p->r = node;
    splay(root, node);
    return root;
}

Node* bst_search(Node* root, int key) {
    Node* cur = root;
    Node* last = nullptr;
    while (cur) {
        last = cur;
        if (key < cur->key) cur = cur->l;
        else if (key > cur->key) cur = cur->r;
        else { splay(root, cur); return root; }
    }
    if (last) splay(root, last);
    return root;
}

Node* erase(Node* root, int key) {
    if (!root) return nullptr;
    root = bst_search(root, key);
    if (root->key != key) return root;
    Node* L = root->l;
    Node* R = root->r;
    if (L) L->p = nullptr;
    if (R) R->p = nullptr;
    delete root;
    if (!L) return R;
    Node* m = L;
    while (m->r) m = m->r;
    splay(L, m);
    L->r = R;
    if (R) R->p = L;
    return L;
}

bool search(Node*& root, int x) {
    root = bst_search(root, x);
    return root && root->key == x;
}

int pred(Node*& root, int x) {
    root = bst_search(root, x);
    if (!root) return INT_MIN;
    if (root->key <= x) return root->key;
    Node* p = root->l;
    if (!p) return INT_MIN;
    while (p->r) p = p->r;
    return p->key;
}

int succ(Node*& root, int x) {
    root = bst_search(root, x);
    if (!root) return INT_MAX;
    if (root->key >= x) return root->key;
    Node* s = root->r;
    if (!s) return INT_MAX;
    while (s->l) s = s->l;
    return s->key;
}

void range_query(Node* root, int lo, int hi, vector<int>& out) {
    if (!root) return;
    if (root->key > lo) range_query(root->l, lo, hi, out);
    if (root->key >= lo && root->key <= hi) out.push_back(root->key);
    if (root->key < hi) range_query(root->r, lo, hi, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int Q;
    cin >> Q;
    Node* root = nullptr;
    while (Q--) {
        int t; cin >> t;
        if (t == 1) { int X; cin >> X; root = bst_insert(root, X); }
        else if (t == 2) { int X; cin >> X; root = erase(root, X); }
        else if (t == 3) { int X; cin >> X; cout << search(root, X) << '\n'; }
        else if (t == 4) { int X; cin >> X; cout << pred(root, X) << '\n'; }
        else if (t == 5) { int X; cin >> X; cout << succ(root, X) << '\n'; }
        else if (t == 6) {
            int X, Y; cin >> X >> Y;
            vector<int> res;
            range_query(root, X, Y, res);
            for (int i = 0; i < (int)res.size(); ++i)
                cout << res[i] << (i+1<res.size()?' ':'\n');
            if (res.empty()) cout << '\n';
        }
    }
    return 0;
}
