#include <bits/stdc++.h>
using namespace std;

struct Node {
    int key, priority;
    Node *l, *r;
    Node(int k): key(k), priority(rand()), l(nullptr), r(nullptr) {}
};

Node* rotate_right(Node* y) {
    Node* x = y->l;
    Node* B = x->r;
    x->r = y;
    y->l = B;
    return x;
}

Node* rotate_left(Node* x) {
    Node* y = x->r;
    Node* B = y->l;
    y->l = x;
    x->r = B;
    return y;
}

Node* insert(Node* root, int key) {
    if (!root) return new Node(key);
    if (key < root->key) {
        root->l = insert(root->l, key);
        if (root->l->priority > root->priority)
            root = rotate_right(root);
    } else if (key > root->key) {
        root->r = insert(root->r, key);
        if (root->r->priority > root->priority)
            root = rotate_left(root);
    }
    return root;
}

Node* erase(Node* root, int key) {
    if (!root) return nullptr;
    if (key < root->key) root->l = erase(root->l, key);
    else if (key > root->key) root->r = erase(root->r, key);
    else {
        if (!root->l || !root->r) {
            Node* t = root->l ? root->l : root->r;
            delete root;
            return t;
        }
        if (root->l->priority > root->r->priority) {
            root = rotate_right(root);
            root->r = erase(root->r, key);
        } else {
            root = rotate_left(root);
            root->l = erase(root->l, key);
        }
    }
    return root;
}

bool search(Node* root, int x) {
    while (root) {
        if (root->key == x) return true;
        root = x < root->key ? root->l : root->r;
    }
    return false;
}

int pred(Node* root, int x) {
    int ans = INT_MIN;
    while (root) {
        if (root->key <= x) { ans = root->key; root = root->r; }
        else root = root->l;
    }
    return ans;
}

int succ(Node* root, int x) {
    int ans = INT_MAX;
    while (root) {
        if (root->key >= x) { ans = root->key; root = root->l; }
        else root = root->r;
    }
    return ans;
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
        if (t == 1) { int X; cin >> X; root = insert(root, X); }
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
